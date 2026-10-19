from __future__ import annotations

import json
import os
import subprocess
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path

from rollback_mvp.test_pi_swe_runner import RecoveringCompletionHandler


REPO_ROOT = Path(__file__).resolve().parent.parent


class PiStrategyMutatorTest(unittest.TestCase):
    def test_recovers_after_three_connection_failures(self) -> None:
        RecoveringCompletionHandler.attempts = 0
        RecoveringCompletionHandler.failures_before_success = 3
        RecoveringCompletionHandler.response_content = json.dumps(
            {
                "mutation_summary": "Add a reusable verification step.",
                "strategy_patch": "## Verification\nValidate the focused change.",
                "tool": None,
                "depends_on": [],
                "probe_task_ids": [],
            }
        )
        server = ThreadingHTTPServer(("127.0.0.1", 0), RecoveringCompletionHandler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            agent_dir = root / "agent"
            agent_dir.mkdir()
            (agent_dir / "auth.json").write_text("[]\n")
            (agent_dir / "models-store.json").write_text("{}\n")
            (agent_dir / "models.json").write_text(
                json.dumps(
                    {
                        "providers": {
                            "fake": {
                                "baseUrl": f"http://127.0.0.1:{server.server_port}/v1",
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
            evidence_path = root / "evidence.json"
            evidence_path.write_text(
                json.dumps(
                    {
                        "parent_artifact_hash": "0" * 64,
                        "entry_task": {"instance_id": "fake__repo-1"},
                    }
                )
                + "\n"
            )
            result_path = root / "result.json"
            trace_path = root / "trace.jsonl"
            completed = subprocess.run(
                [
                    "node",
                    str(REPO_ROOT / "rollback_mvp" / "pi_strategy_mutator.mjs"),
                    "--agent-dir",
                    str(agent_dir),
                    "--evidence-file",
                    str(evidence_path),
                    "--output",
                    str(result_path),
                    "--trace",
                    str(trace_path),
                    "--max-output-tokens",
                    "8192",
                    "--max-total-tokens",
                    "32000",
                    "--timeout-seconds",
                    "60",
                    "--model-provider",
                    "fake",
                    "--model-id",
                    "fake-model",
                ],
                cwd=REPO_ROOT,
                env={
                    **os.environ,
                    "ROLLBACK_ENDPOINT_API_KEY": "test-key",
                    "NO_PROXY": "127.0.0.1,localhost",
                    "no_proxy": "127.0.0.1,localhost",
                },
                capture_output=True,
                text=True,
                timeout=90,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(RecoveringCompletionHandler.attempts, 4)
            result = json.loads(result_path.read_text())
            self.assertTrue(result["valid"])
            self.assertNotIn("providerError", result)
            events = [
                json.loads(line)
                for line in trace_path.read_text().splitlines()
                if line
            ]
            stop_reasons = [
                event["message"]["stopReason"]
                for event in events
                if event["type"] == "message_end"
                and event["message"]["role"] == "assistant"
            ]
            self.assertEqual(stop_reasons.count("error"), 3)
            self.assertEqual(stop_reasons[-1], "stop")


if __name__ == "__main__":
    unittest.main()
