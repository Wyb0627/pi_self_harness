from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from freeze_dgm200_manifest import canonical_json, sha256_ids
from repair_slice_once import apply_edits, workspace_patch
from orchestrate_endpoint_200 import (
    aggregate_results,
    distribution,
    exact_mcnemar_p_value,
    inert_feedback_probe_patch,
    materialize_inputs,
    paired_bootstrap_interval,
    recovery_candidate_paths,
    wilson_interval,
)


class ManifestHelpersTest(unittest.TestCase):
    def test_canonical_json_is_order_independent(self) -> None:
        self.assertEqual(
            canonical_json({"b": 2, "a": 1}),
            canonical_json({"a": 1, "b": 2}),
        )

    def test_id_hash_includes_record_boundaries(self) -> None:
        self.assertNotEqual(sha256_ids(["ab", "c"]), sha256_ids(["a", "bc"]))

    def test_materialized_agent_input_contains_only_safe_fields_and_test_paths(
        self,
    ) -> None:
        row = {
            "instance_id": "repo__task-1",
            "repo": "owner/repo",
            "base_commit": "abc",
            "problem_statement": "fix it",
            "patch": "gold",
            "test_patch": (
                "diff --git a/pkg/tests/test_bug.py b/pkg/tests/test_bug.py\n"
                "--- a/pkg/tests/test_bug.py\n"
                "+++ b/pkg/tests/test_bug.py\n"
            ),
        }
        manifest = {"records": [{"record": row}]}
        with tempfile.TemporaryDirectory() as temporary:
            _, task_path = materialize_inputs(manifest, Path(temporary))
            task = json.loads(task_path.read_text())[0]
        self.assertNotIn("patch", task)
        self.assertNotIn("test_patch", task)
        self.assertEqual(task["forbidden_paths"], ["pkg/tests/test_bug.py"])


class RecoveryProtocolTest(unittest.TestCase):
    def test_inert_feedback_probe_is_a_valid_patch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            result = subprocess.run(
                ["git", "apply", "--check", "-"],
                cwd=repository,
                input=inert_feedback_probe_patch("repo__task-1"),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_candidate_paths_prefer_patch_then_recent_trace_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            first = workspace / "src" / "first.py"
            second = workspace / "src" / "second.py"
            test_file = workspace / "tests" / "test_first.py"
            for path in (first, second, test_file):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("")
            trace = workspace / "trace.jsonl"
            events = [
                {
                    "type": "tool_execution_start",
                    "args": {"path": str(first)},
                },
                {
                    "type": "tool_execution_start",
                    "args": {"path": str(test_file)},
                },
                {
                    "type": "tool_execution_start",
                    "args": {"path": "src/second.py"},
                },
            ]
            trace.write_text("".join(json.dumps(event) + "\n" for event in events))
            result = {
                "patch": (
                    "diff --git a/src/changed.py b/src/changed.py\n"
                    "--- a/src/changed.py\n"
                    "+++ b/src/changed.py\n"
                )
            }
            self.assertEqual(
                recovery_candidate_paths(result, trace, workspace),
                ["src/changed.py", "src/second.py", "src/first.py"],
            )

    def test_recovery_patch_preserves_untouched_baseline_files(self) -> None:
        repository = Path(tempfile.mkdtemp())
        try:
            subprocess.run(["git", "init", "--quiet"], cwd=repository, check=True)
            first = repository / "first.py"
            second = repository / "second.py"
            first.write_text("before\n")
            second.write_text("before\n")
            subprocess.run(["git", "add", "first.py", "second.py"], cwd=repository, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test@example.com",
                    "commit",
                    "--quiet",
                    "-m",
                    "base",
                ],
                cwd=repository,
                check=True,
            )
            first.write_text("baseline\n")
            second.write_text("repaired\n")
            patch = workspace_patch(repository)
            self.assertIn("diff --git a/first.py b/first.py", patch)
            self.assertIn("diff --git a/second.py b/second.py", patch)
        finally:
            shutil.rmtree(repository, ignore_errors=True)

    def test_failed_edit_validation_does_not_partially_modify_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            first = workspace / "first.py"
            second = workspace / "second.py"
            first.write_text("before\n")
            second.write_text("repeat\nrepeat\n")

            with self.assertRaisesRegex(ValueError, "found 2"):
                apply_edits(
                    workspace,
                    [
                        {"path": "first.py", "old": "before", "new": "after"},
                        {"path": "second.py", "old": "repeat", "new": "changed"},
                    ],
                )

            self.assertEqual(first.read_text(), "before\n")
            self.assertEqual(second.read_text(), "repeat\nrepeat\n")


class StatisticsTest(unittest.TestCase):
    def test_distribution_and_wilson_interval(self) -> None:
        self.assertEqual(distribution([1, 2, 3, 4])["median"], 2.5)
        interval = wilson_interval(100, 200)
        self.assertIsNotNone(interval)
        assert interval is not None
        self.assertLess(interval[0], 0.5)
        self.assertGreater(interval[1], 0.5)

    def test_paired_bootstrap_and_exact_mcnemar(self) -> None:
        original = [False] * 10 + [True] * 10
        recovery = [True] * 10 + [True] * 10
        interval = paired_bootstrap_interval(
            original,
            recovery,
            samples=2_000,
            seed=7,
        )
        self.assertIsNotNone(interval)
        assert interval is not None
        self.assertGreater(interval[0], 0)
        self.assertEqual(exact_mcnemar_p_value(0, 10), 0.00195312)

    def test_evaluator_errors_are_incomplete_and_repair_errors_are_attempts(
        self,
    ) -> None:
        manifest = {
            "name": "test",
            "ordering": {"instance_ids_sha256": "test"},
            "records": [
                {
                    "stage": "small",
                    "record": {"instance_id": "repo__task-1"},
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            task = output / "tasks" / "repo__task-1"
            (task / "original").mkdir(parents=True)
            (task / "recovery").mkdir(parents=True)
            (task / "original" / "result.json").write_text("{}")
            (task / "original" / "evaluation.json").write_text(
                json.dumps({"status": "evaluator_error", "resolved": False})
            )
            (task / "recovery" / "status.json").write_text(
                json.dumps({"status": "repair_error", "resolved": False})
            )
            summary = aggregate_results(manifest, "manifest", output)
        self.assertFalse(summary["complete"])
        self.assertEqual(summary["originalPiOneShot"]["completedTasks"], 0)
        self.assertEqual(summary["feedbackAssistedRfClm"]["repairAttempts"], 1)

    def test_repair_error_is_a_completed_failed_recovery_with_conservative_charge(
        self,
    ) -> None:
        manifest = {
            "name": "test",
            "ordering": {"instance_ids_sha256": "test"},
            "records": [
                {
                    "stage": "small",
                    "record": {"instance_id": "repo__task-1"},
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            task = output / "tasks" / "repo__task-1"
            (task / "original").mkdir(parents=True)
            (task / "recovery").mkdir(parents=True)
            (task / "original" / "result.json").write_text("{}")
            (task / "original" / "evaluation.json").write_text(
                json.dumps({"status": "empty_patch", "resolved": False})
            )
            (task / "recovery" / "result.json").write_text(
                json.dumps(
                    {
                        "status": "repair_error",
                        "tokenTelemetryAvailable": False,
                        "conservativeTokenCharge": 512_000,
                    }
                )
            )
            (task / "recovery" / "status.json").write_text(
                json.dumps({"status": "repair_error", "resolved": False})
            )
            (output / "run_config.json").write_text(
                json.dumps({"protocol": "original_and_feedback"})
            )
            summary = aggregate_results(manifest, "manifest", output)

        self.assertTrue(summary["complete"])
        self.assertEqual(summary["feedbackAssistedRfClm"]["completedTasks"], 1)
        self.assertEqual(summary["feedbackAssistedRfClm"]["repairAttempts"], 1)
        self.assertFalse(summary["tokenAccounting"]["telemetryComplete"])
        self.assertEqual(summary["tokenAccounting"]["budgetCountedTokens"], 512_000)


if __name__ == "__main__":
    unittest.main()
