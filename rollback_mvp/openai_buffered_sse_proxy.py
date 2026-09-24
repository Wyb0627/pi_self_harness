"""Adapt a buffered OpenAI-compatible endpoint to Chat Completions SSE."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


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

    def do_POST(self) -> None:
        if not self.path.endswith("/chat/completions"):
            self.send_error(404)
            return

        try:
            body = json.loads(self.rfile.read(int(self.headers.get("content-length", "0"))))
            wants_stream = bool(body.pop("stream", False))
            body.pop("stream_options", None)
            request = urllib.request.Request(
                f"{self.upstream}/chat/completions",
                data=json.dumps(body).encode(),
                headers={
                    "Authorization": self.headers.get("authorization", ""),
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=600) as response:
                payload = json.loads(response.read())
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
    parser.add_argument(
        "--upstream",
        default="https://aicolate.tiktok-row.net/ai-gateway/openai/v1",
    )
    args = parser.parse_args()
    ProxyHandler.upstream = args.upstream.rstrip("/")
    ThreadingHTTPServer((args.host, args.port), ProxyHandler).serve_forever()


if __name__ == "__main__":
    main()
