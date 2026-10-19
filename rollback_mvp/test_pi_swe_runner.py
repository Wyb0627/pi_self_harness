from __future__ import annotations

import json
import os
import socket
import subprocess
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


class RecoveringCompletionHandler(BaseHTTPRequestHandler):
    attempts = 0
    attempts_lock = threading.Lock()
    failures_before_success = 2
    response_content = "The task is complete."

    def do_POST(self) -> None:
        self.rfile.read(int(self.headers.get("content-length", "0")))
        with self.attempts_lock:
            type(self).attempts += 1
            attempt = type(self).attempts
        if attempt <= self.failures_before_success:
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.connection.close()
            return

        chunks = [
            {
                "id": "chatcmpl-recovered",
                "object": "chat.completion.chunk",
                "created": 0,
                "model": "fake-model",
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "role": "assistant",
                            "content": self.response_content,
                        },
                        "finish_reason": "stop",
                    }
                ],
            },
            {
                "id": "chatcmpl-recovered",
                "object": "chat.completion.chunk",
                "created": 0,
                "model": "fake-model",
                "choices": [],
                "usage": {
                    "prompt_tokens": 1,
                    "completion_tokens": 1,
                    "total_tokens": 2,
                },
            },
        ]
        payload = "".join(
            f"data: {json.dumps(chunk)}\n\n" for chunk in chunks
        ) + "data: [DONE]\n\n"
        encoded = payload.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, _format: str, *args: object) -> None:
        del _format, args


class PiSweRunnerTest(unittest.TestCase):
    def test_recovered_provider_errors_do_not_fail_the_runner(self) -> None:
        completed, result, events = self.run_runner(failures_before_success=2)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(RecoveringCompletionHandler.attempts, 3)
        self.assertNotIn("providerError", result)
        stop_reasons = [
            event["message"]["stopReason"]
            for event in events
            if event["type"] == "message_end"
            and event["message"]["role"] == "assistant"
        ]
        self.assertEqual(stop_reasons.count("error"), 2)
        self.assertEqual(stop_reasons[-1], "stop")

    def test_runner_recovers_after_three_connection_failures(self) -> None:
        # A short provider outage must not invalidate an entire paid search.
        completed, result, events = self.run_runner(failures_before_success=3)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(RecoveringCompletionHandler.attempts, 4)
        self.assertNotIn("providerError", result)
        stop_reasons = [
            event["message"]["stopReason"]
            for event in events
            if event["type"] == "message_end"
            and event["message"]["role"] == "assistant"
        ]
        self.assertEqual(stop_reasons.count("error"), 3)
        self.assertEqual(stop_reasons[-1], "stop")

    def run_runner(
        self,
        *,
        failures_before_success: int,
    ) -> tuple[subprocess.CompletedProcess[str], dict[str, object], list[dict[str, object]]]:
        RecoveringCompletionHandler.attempts = 0
        RecoveringCompletionHandler.failures_before_success = failures_before_success
        RecoveringCompletionHandler.response_content = "The task is complete."
        server = ThreadingHTTPServer(("127.0.0.1", 0), RecoveringCompletionHandler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            agent_dir = root / "agent"
            workspace = root / "workspace"
            agent_dir.mkdir()
            workspace.mkdir()
            (agent_dir / "auth.json").write_text("[]\n")
            (agent_dir / "models-store.json").write_text("{}\n")
            (agent_dir / "models.json").write_text(
                json.dumps(
                    {
                        "providers": {
                            "fake": {
                                "baseUrl": (
                                    f"http://127.0.0.1:{server.server_port}/v1"
                                ),
                                "api": "openai-completions",
                                "apiKey": "$ROLLBACK_ENDPOINT_API_KEY",
                                "compat": {
                                    "maxTokensField": "max_tokens",
                                    "supportsDeveloperRole": False,
                                    "supportsReasoningEffort": False,
                                    "supportsUsageInStreaming": True,
                                },
                                "models": [
                                    {
                                        "id": "fake-model",
                                        "name": "Fake model",
                                        "reasoning": False,
                                        "input": ["text"],
                                        "contextWindow": 131072,
                                        "maxTokens": 4096,
                                        "cost": {
                                            "input": 0,
                                            "output": 0,
                                            "cacheRead": 0,
                                            "cacheWrite": 0,
                                        },
                                    }
                                ],
                            }
                        }
                    }
                )
                + "\n"
            )
            task_path = root / "tasks.json"
            task_path.write_text(
                json.dumps(
                    [
                        {
                            "instance_id": "fake__repo-1",
                            "problem_statement": "Inspect the repository and finish.",
                        }
                    ]
                )
                + "\n"
            )
            (workspace / "README.md").write_text("fixture\n")
            subprocess.run(["git", "init", "-q"], cwd=workspace, check=True)
            subprocess.run(
                ["git", "config", "user.email", "fixture@example.com"],
                cwd=workspace,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Fixture"],
                cwd=workspace,
                check=True,
            )
            subprocess.run(["git", "add", "README.md"], cwd=workspace, check=True)
            subprocess.run(
                ["git", "commit", "-q", "-m", "fixture"],
                cwd=workspace,
                check=True,
            )

            result_path = root / "result.json"
            trace_path = root / "trace.jsonl"
            environment = {
                **os.environ,
                "ROLLBACK_ENDPOINT_API_KEY": "test-key",
                "NO_PROXY": "127.0.0.1,localhost",
                "no_proxy": "127.0.0.1,localhost",
            }
            completed = subprocess.run(
                [
                    "node",
                    str(REPO_ROOT / "rollback_mvp" / "pi_swe_runner.mjs"),
                    "--agent-dir",
                    str(agent_dir),
                    "--instance-id",
                    "fake__repo-1",
                    "--output",
                    str(result_path),
                    "--task-file",
                    str(task_path),
                    "--trace",
                    str(trace_path),
                    "--workspace",
                    str(workspace),
                    "--no-shell",
                    "--max-output-tokens",
                    "65536",
                    "--max-total-tokens",
                    "512000",
                    "--timeout-seconds",
                    "60",
                    "--model-provider",
                    "fake",
                    "--model-id",
                    "fake-model",
                ],
                cwd=REPO_ROOT,
                env=environment,
                capture_output=True,
                text=True,
                timeout=90,
                check=False,
            )

            result = json.loads(result_path.read_text())
            events = [
                json.loads(line)
                for line in trace_path.read_text().splitlines()
                if line
            ]
            return completed, result, events


if __name__ == "__main__":
    unittest.main()
