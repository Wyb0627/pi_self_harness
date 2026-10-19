from __future__ import annotations

import json
import os
import socket
import subprocess
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


class RecoveringCompletionHandler(BaseHTTPRequestHandler):
    attempts = 0
    attempts_lock = threading.Lock()
    failures_before_success = 2
    response_content = "The task is complete."
    tool_command: dict[str, object] | None = None

    def do_POST(self) -> None:
        self.rfile.read(int(self.headers.get("content-length", "0")))
        with self.attempts_lock:
            type(self).attempts += 1
            attempt = type(self).attempts
        if attempt == 1 and self.tool_command is not None:
            chunks = [
                {
                    "id": "chatcmpl-tool",
                    "object": "chat.completion.chunk",
                    "created": 0,
                    "model": "fake-model",
                    "choices": [
                        {
                            "index": 0,
                            "delta": {
                                "role": "assistant",
                                "tool_calls": [
                                    {
                                        "index": 0,
                                        "id": "call_infinite",
                                        "type": "function",
                                        "function": {
                                            "name": "sandbox_bash",
                                            "arguments": json.dumps(
                                                self.tool_command
                                            ),
                                        },
                                    }
                                ],
                            },
                            "finish_reason": "tool_calls",
                        }
                    ],
                },
                {
                    "id": "chatcmpl-tool",
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
        elif attempt <= self.failures_before_success:
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.connection.close()
            return

        else:
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
        completed, result, events, _, _ = self.run_runner(
            failures_before_success=2
        )

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
        completed, result, events, _, _ = self.run_runner(
            failures_before_success=3
        )

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

    def test_high_output_command_timeout_forces_container_cleanup(self) -> None:
        completed, result, events, container_exists, elapsed = self.run_runner(
            failures_before_success=0,
            tool_command={
                "command": (
                    "while :; do "
                    "printf 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                    "xxxxxxxxxxxxxxxx\\n'; "
                    "done"
                ),
                "timeout": 1,
            },
            fake_docker=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertLess(elapsed, 8)
        self.assertFalse(container_exists)
        self.assertNotIn("providerError", result)
        tool_results = [
            event["result"]
            for event in events
            if event["type"] == "tool_execution_end"
        ]
        self.assertEqual(len(tool_results), 1)
        self.assertTrue(tool_results[0]["details"]["timedOut"])
        self.assertLessEqual(len(tool_results[0]["content"][0]["text"]), 100_100)

    def run_runner(
        self,
        *,
        failures_before_success: int,
        tool_command: dict[str, object] | None = None,
        fake_docker: bool = False,
    ) -> tuple[
        subprocess.CompletedProcess[str],
        dict[str, object],
        list[dict[str, object]],
        bool,
        float,
    ]:
        RecoveringCompletionHandler.attempts = 0
        RecoveringCompletionHandler.failures_before_success = failures_before_success
        RecoveringCompletionHandler.response_content = "The task is complete."
        RecoveringCompletionHandler.tool_command = tool_command
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
            fake_docker_state = root / "fake-docker-state.json"
            fake_docker_bin = root / "bin"
            if fake_docker:
                fake_docker_bin.mkdir()
                fake_docker_path = fake_docker_bin / "docker"
                fake_docker_path.write_text(
                    """#!/usr/bin/env python3
import json
import os
from pathlib import Path
import signal
import subprocess
import sys

state = Path(os.environ["FAKE_DOCKER_STATE"])
if sys.argv[1] == "run":
    command = subprocess.Popen(
        ["/bin/bash", "-lc", sys.argv[-1]],
        stdout=sys.stdout,
        stderr=sys.stderr,
        start_new_session=True,
    )
    temporary = state.with_suffix(".tmp")
    temporary.write_text(json.dumps({"docker": os.getpid(), "command": command.pid}))
    temporary.replace(state)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    raise SystemExit(command.wait())
if sys.argv[1:3] == ["rm", "--force"]:
    data = json.loads(state.read_text())
    try:
        os.killpg(data["command"], signal.SIGKILL)
    except ProcessLookupError:
        pass
    try:
        os.kill(data["docker"], signal.SIGKILL)
    except ProcessLookupError:
        pass
    state.unlink(missing_ok=True)
    raise SystemExit(0)
raise SystemExit(2)
"""
                )
                fake_docker_path.chmod(0o755)
            environment = {
                **os.environ,
                "ROLLBACK_ENDPOINT_API_KEY": "test-key",
                "NO_PROXY": "127.0.0.1,localhost",
                "no_proxy": "127.0.0.1,localhost",
                **(
                    {
                        "FAKE_DOCKER_STATE": str(fake_docker_state),
                        "PATH": f"{fake_docker_bin}:{os.environ['PATH']}",
                    }
                    if fake_docker
                    else {}
                ),
            }
            command = [
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
            ]
            if fake_docker:
                command.extend(["--sandbox-image", "fake-image"])
            else:
                command.append("--no-shell")
            started = time.monotonic()
            completed = subprocess.run(
                command,
                cwd=REPO_ROOT,
                env=environment,
                capture_output=True,
                text=True,
                timeout=90,
                check=False,
            )
            elapsed = time.monotonic() - started

            result = json.loads(result_path.read_text())
            events = [
                json.loads(line)
                for line in trace_path.read_text().splitlines()
                if line
            ]
            return (
                completed,
                result,
                events,
                fake_docker_state.exists(),
                elapsed,
            )


if __name__ == "__main__":
    unittest.main()
