"""Adapt a buffered OpenAI-compatible endpoint to Chat Completions SSE."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def fetch_completion(
    upstream: str,
    body: dict,
    authorization: str,
    *,
    max_rate_limit_retries: int,
    rate_limit_wait_seconds: float,
    max_transient_retries: int = 5,
    transient_retry_base_seconds: float = 5.0,
    transient_retry_max_seconds: float = 60.0,
) -> dict:
    rate_limit_retries = 0
    transient_retries = 0
    while True:
        request = urllib.request.Request(
            f"{upstream}/chat/completions",
            data=json.dumps(body).encode(),
            headers={
                "Authorization": authorization,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=600) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as error:
            if error.code == 429 and rate_limit_retries < max_rate_limit_retries:
                rate_limit_retries += 1
                retry_after = error.headers.get("Retry-After") if error.headers else None
                try:
                    requested_wait = float(retry_after) if retry_after else 0.0
                except ValueError:
                    requested_wait = 0.0
                wait_seconds = max(rate_limit_wait_seconds, requested_wait)
                error.read()
                print(
                    f"Upstream rate limited request; retrying in {wait_seconds:g}s "
                    f"({rate_limit_retries}/{max_rate_limit_retries}).",
                    file=sys.stderr,
                    flush=True,
                )
                time.sleep(wait_seconds)
                continue
            if error.code in {408, 409} or error.code >= 500:
                if transient_retries < max_transient_retries:
                    transient_retries += 1
                    wait_seconds = min(
                        transient_retry_base_seconds * 2 ** (transient_retries - 1),
                        transient_retry_max_seconds,
                    )
                    error.read()
                    print(
                        f"Upstream HTTP {error.code}; retrying in {wait_seconds:g}s "
                        f"({transient_retries}/{max_transient_retries}).",
                        file=sys.stderr,
                        flush=True,
                    )
                    time.sleep(wait_seconds)
                    continue
                raise
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
            if transient_retries >= max_transient_retries:
                raise
            transient_retries += 1
            wait_seconds = min(
                transient_retry_base_seconds * 2 ** (transient_retries - 1),
                transient_retry_max_seconds,
            )
            print(
                f"Upstream connection failed; retrying in {wait_seconds:g}s "
                f"({transient_retries}/{max_transient_retries}): {error}",
                file=sys.stderr,
                flush=True,
            )
            time.sleep(wait_seconds)


def response_events(payload: dict) -> list[dict]:
    events = []
    for choice in payload.get("choices", []):
        message = choice.get("message", {})
        delta = {"role": message.get("role", "assistant")}
        for key in ("content", "reasoning_content", "tool_calls"):
            if message.get(key) is not None:
                delta[key] = message[key]
        events.append(
            {
                "id": payload.get("id"),
                "object": "chat.completion.chunk",
                "created": payload.get("created"),
                "model": payload.get("model"),
                "choices": [
                    {
                        "index": choice.get("index", 0),
                        "delta": delta,
                        "finish_reason": choice.get("finish_reason"),
                    }
                ],
            }
        )
    if payload.get("usage") is not None:
        events.append(
            {
                "id": payload.get("id"),
                "object": "chat.completion.chunk",
                "created": payload.get("created"),
                "model": payload.get("model"),
                "choices": [],
                "usage": payload["usage"],
            }
        )
    return events


class ProxyHandler(BaseHTTPRequestHandler):
    upstream = ""
    max_rate_limit_retries = 3
    rate_limit_wait_seconds = 65.0
    max_transient_retries = 5
    transient_retry_base_seconds = 5.0
    transient_retry_max_seconds = 60.0

    def do_POST(self) -> None:
        if not self.path.endswith("/chat/completions"):
            self.send_error(404)
            return

        try:
            body = json.loads(self.rfile.read(int(self.headers.get("content-length", "0"))))
            wants_stream = bool(body.pop("stream", False))
            body.pop("stream_options", None)
            payload = fetch_completion(
                self.upstream,
                body,
                self.headers.get("authorization", ""),
                max_rate_limit_retries=self.max_rate_limit_retries,
                rate_limit_wait_seconds=self.rate_limit_wait_seconds,
                max_transient_retries=self.max_transient_retries,
                transient_retry_base_seconds=self.transient_retry_base_seconds,
                transient_retry_max_seconds=self.transient_retry_max_seconds,
            )
        except urllib.error.HTTPError as error:
            self.send_response(error.code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(error.read())
            return
        except Exception as error:
            self.send_error(502, str(error))
            return

        if not wants_stream:
            encoded = json.dumps(payload).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        try:
            for event in response_events(payload):
                self.wfile.write(f"data: {json.dumps(event)}\n\n".encode())
            self.wfile.write(b"data: [DONE]\n\n")
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, _format: str, *_args: object) -> None:
        del _format, _args
        return


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--max-rate-limit-retries", type=int, default=3)
    parser.add_argument("--rate-limit-wait-seconds", type=float, default=65.0)
    parser.add_argument("--max-transient-retries", type=int, default=5)
    parser.add_argument("--transient-retry-base-seconds", type=float, default=5.0)
    parser.add_argument("--transient-retry-max-seconds", type=float, default=60.0)
    parser.add_argument(
        "--upstream",
        default="https://aicolate.tiktok-row.net/ai-gateway/openai/v1",
    )
    args = parser.parse_args()
    if args.max_rate_limit_retries < 0:
        parser.error("--max-rate-limit-retries must be non-negative")
    if args.rate_limit_wait_seconds < 0:
        parser.error("--rate-limit-wait-seconds must be non-negative")
    if args.max_transient_retries < 0:
        parser.error("--max-transient-retries must be non-negative")
    if args.transient_retry_base_seconds < 0:
        parser.error("--transient-retry-base-seconds must be non-negative")
    if args.transient_retry_max_seconds < 0:
        parser.error("--transient-retry-max-seconds must be non-negative")
    ProxyHandler.upstream = args.upstream.rstrip("/")
    ProxyHandler.max_rate_limit_retries = args.max_rate_limit_retries
    ProxyHandler.rate_limit_wait_seconds = args.rate_limit_wait_seconds
    ProxyHandler.max_transient_retries = args.max_transient_retries
    ProxyHandler.transient_retry_base_seconds = args.transient_retry_base_seconds
    ProxyHandler.transient_retry_max_seconds = args.transient_retry_max_seconds
    ThreadingHTTPServer((args.host, args.port), ProxyHandler).serve_forever()


if __name__ == "__main__":
    main()
