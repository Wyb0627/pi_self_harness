from __future__ import annotations

import json
import tempfile
import unittest
import os
from pathlib import Path
from unittest.mock import patch

from .container_runner import (
    MODEL_PROXY_REQUEST_SCHEMA_HASH,
    ContainerIsolationError,
    ContainerMounts,
    ContainerPolicy,
    DockerCliRuntime,
    FakeContainerRuntime,
    FullCandidateContainerRunner,
    ModelProxyBudgetLedger,
    ModelProxyPolicy,
    RuntimeResult,
    build_invocation,
    hash_candidate_source,
)
from .paired_executor import (
    ArtifactObservation,
    ArtifactRef,
    ExecutionRequest,
    ExecutionSettings,
    ModelSettings,
)
from .schemas import sha256_bytes


HASH_A = "a" * 64
HASH_B = "b" * 64
HASH_C = "c" * 64
HASH_D = "d" * 64


class FakeOutsideEvaluator:
    def __init__(self) -> None:
        self.calls = []

    def evaluate(
        self,
        request,
        candidate_result_path,
        candidate_patch_path,
        trajectory_path,
        evidence_dir,
    ):
        self.calls.append(
            (
                request,
                candidate_result_path,
                candidate_patch_path,
                trajectory_path,
                evidence_dir,
            )
        )
        return ArtifactObservation(
            execution_identity_hash=request.identity_hash,
            status="completed",
            resolved=True,
            input_tokens=4,
            output_tokens=2,
            cost=0.01,
            latency_seconds=0.2,
            trajectory_hash=sha256_bytes(trajectory_path.read_bytes()),
            result_hash=sha256_bytes(candidate_result_path.read_bytes()),
            trajectory_artifact=trajectory_path.name,
            result_artifact=candidate_result_path.name,
            public_summary="outside evaluator result",
        )


class ContainerBoundaryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.seccomp = self.root / "seccomp.json"
        self.seccomp.write_text('{"defaultAction":"SCMP_ACT_ERRNO"}')
        self.policy = ContainerPolicy(
            schema_version=1,
            runtime="docker",
            network_mode="none",
            user="65532:65532",
            read_only_root=True,
            cap_drop_all=True,
            no_new_privileges=True,
            pids_limit=256,
            memory_limit="8g",
            cpu_limit="4",
            tmpfs_size="1g",
            seccomp_profile_path=str(self.seccomp),
            seccomp_profile_hash=sha256_bytes(self.seccomp.read_bytes()),
            max_output_file_bytes=1_000_000,
            max_output_total_bytes=2_000_000,
        )
        self.socket_path = self.root / "proxy.sock"
        self.socket_path.touch()
        self.socket_path = self.socket_path.resolve()
        self.proxy = ModelProxyPolicy(
            schema_version=1,
            socket_path=str(self.socket_path),
            model_id="fake-model",
            model_revision="fake-revision",
            request_schema_hash=MODEL_PROXY_REQUEST_SCHEMA_HASH,
            max_input_tokens=800,
            max_output_tokens=200,
        )
        for name in ("candidate", "workspace", "output", "control"):
            (self.root / name).mkdir()
        (self.root / "candidate" / "pi.mjs").write_text("export {};\n")
        candidate_hash = hash_candidate_source(self.root / "candidate")
        settings = ExecutionSettings(
            model=ModelSettings(
                provider="proxy",
                model_id="fake-model",
                model_revision="fake-revision",
                inference_settings=(("temperature", "0"),),
            ),
            timeout_seconds=60,
            token_budget=1000,
            retry_budget=0,
            tool_budget=20,
            runner_image="candidate",
            runner_image_digest=HASH_C,
            evaluator_image="evaluator",
            evaluator_image_digest=HASH_D,
            runner_revision="v1",
            evaluator_revision="v1",
            container_policy_hash=self.policy.policy_hash,
        )
        self.request = ExecutionRequest(
            task_instance_id="repo__task-1",
            task_repo="owner/repo",
            task_base_commit="commit",
            task_problem_statement="fix issue",
            artifact=ArtifactRef("parent", candidate_hash, str(self.root / "candidate")),
            parent_artifact_hash=candidate_hash,
            child_artifact_hash=HASH_B,
            dataset_manifest_hash=HASH_C,
            final_manifest_hash=HASH_D,
            settings=settings,
        )
        (self.root / "task.json").write_text(
            json.dumps(
                {
                    "instance_id": "repo__task-1",
                    "repo": "owner/repo",
                    "base_commit": "commit",
                    "problem_statement": "fix issue",
                }
            )
        )
        self.mounts = ContainerMounts(
            candidate_source=str(self.root / "candidate"),
            task_workspace=str(self.root / "workspace"),
            public_task_input=str(self.root / "task.json"),
            candidate_output=str(self.root / "output"),
            model_proxy_socket=str(self.socket_path),
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def invocation(self):
        with patch.object(Path, "is_socket", return_value=True):
            return build_invocation(
                request=self.request,
                image_repository="candidate",
                image_digest=HASH_C,
                entrypoint=("node", "/candidate/pi.mjs"),
                mounts=self.mounts,
                policy=self.policy,
                proxy_policy=self.proxy,
                immutable_control_roots=(self.root / "control",),
            )

    def test_invocation_is_digest_pinned_networkless_and_has_no_host_fallback(self) -> None:
        invocation = self.invocation()
        self.assertEqual(invocation.image_reference, f"candidate@sha256:{HASH_C}")
        command = DockerCliRuntime()._command(invocation)
        self.assertIn("none", command)
        self.assertIn("--read-only", command)
        self.assertIn("no-new-privileges", command)
        self.assertIn(f"seccomp={self.seccomp}", command)
        runtime = FakeContainerRuntime(
            RuntimeResult(0, "", "", 0.1, False, False, HASH_C),
            verification_error="daemon unavailable",
        )
        with self.assertRaisesRegex(ContainerIsolationError, "daemon unavailable"):
            runtime.run(invocation)

    def test_control_plane_overlap_and_proxy_identity_fail_closed(self) -> None:
        overlapping = ContainerMounts(
            candidate_source=str(self.root / "control"),
            task_workspace=self.mounts.task_workspace,
            public_task_input=self.mounts.public_task_input,
            candidate_output=self.mounts.candidate_output,
            model_proxy_socket=self.mounts.model_proxy_socket,
        )
        with self.assertRaisesRegex(ContainerIsolationError, "overlaps immutable"):
            with patch.object(Path, "is_socket", return_value=True):
                build_invocation(
                    request=self.request,
                    image_repository="candidate",
                    image_digest=HASH_C,
                    entrypoint=("node",),
                    mounts=overlapping,
                    policy=self.policy,
                    proxy_policy=self.proxy,
                    immutable_control_roots=(self.root / "control",),
                )
        with self.assertRaisesRegex(ContainerIsolationError, "identity mismatch"):
            self.proxy.validate_request(
                {
                    "execution_identity_hash": HASH_D,
                    "model_id": "fake-model",
                    "model_revision": "fake-revision",
                    "messages": [{"role": "user", "content": "x"}],
                    "max_output_tokens": 100,
                },
                execution_identity_hash=self.request.identity_hash,
            )

    def test_proxy_budget_ledger_and_external_evaluator_boundary(self) -> None:
        ledger = ModelProxyBudgetLedger(
            self.root / "ledger", self.proxy, self.request.identity_hash
        )
        proxy_request = {
            "execution_identity_hash": self.request.identity_hash,
            "model_id": "fake-model",
            "model_revision": "fake-revision",
            "messages": [{"role": "user", "content": "x"}],
            "max_output_tokens": 100,
        }
        ledger.reserve_request(proxy_request, estimated_input_tokens=10)
        ledger.append_usage(input_tokens=10, output_tokens=100, response_hash=HASH_D)
        proxy_request["max_output_tokens"] = 101
        with self.assertRaisesRegex(ContainerIsolationError, "output-token budget exceeded"):
            ledger.reserve_request(proxy_request, estimated_input_tokens=10)

        patch_content = b"diff --git a/a b/a\n"
        candidate_result = {
            "execution_identity_hash": self.request.identity_hash,
            "status": "completed",
            "input_tokens": 4,
            "output_tokens": 2,
            "cost": 0.01,
            "public_summary": "candidate completed",
            "patch_sha256": sha256_bytes(patch_content),
        }
        def write_outputs(_invocation):
            (self.root / "output" / "candidate-result.json").write_text(
                json.dumps(candidate_result)
            )
            (self.root / "output" / "candidate.patch").write_bytes(patch_content)
            (self.root / "output" / "trajectory.jsonl").write_text(
                '{"event":"done"}\n'
            )
        runtime = FakeContainerRuntime(
            RuntimeResult(0, "", "", 0.1, False, False, HASH_C),
            on_run=write_outputs,
        )
        evaluator = FakeOutsideEvaluator()
        runner = FullCandidateContainerRunner(
            runtime=runtime,
            image_repository="candidate",
            image_digest=HASH_C,
            entrypoint=("node", "/candidate/pi.mjs"),
            policy=self.policy,
            proxy_policy=self.proxy,
            immutable_control_roots=(self.root / "control",),
            mounts_factory=lambda _request: self.mounts,
            evaluator=evaluator,
            workspace_claim_root=self.root / "claims",
        )
        with patch.object(Path, "is_socket", return_value=True):
            observation = runner.run(self.request, self.root / "evidence")
        self.assertTrue(observation.resolved)
        self.assertEqual(len(runtime.invocations), 1)
        self.assertEqual(len(evaluator.calls), 1)

    def test_missing_outputs_do_not_trigger_host_execution(self) -> None:
        runtime = FakeContainerRuntime(
            RuntimeResult(0, "", "", 0.1, False, False, HASH_C)
        )
        runner = FullCandidateContainerRunner(
            runtime=runtime,
            image_repository="candidate",
            image_digest=HASH_C,
            entrypoint=("node", "/candidate/pi.mjs"),
            policy=self.policy,
            proxy_policy=self.proxy,
            immutable_control_roots=(self.root / "control",),
            mounts_factory=lambda _request: self.mounts,
            evaluator=FakeOutsideEvaluator(),
            workspace_claim_root=self.root / "claims",
        )
        with self.assertRaisesRegex(ContainerIsolationError, "open candidate output safely"):
            with patch.object(Path, "is_socket", return_value=True):
                runner.run(self.request, self.root / "evidence")
        self.assertEqual(len(runtime.invocations), 1)

    def test_output_symlink_and_workspace_reuse_fail_closed(self) -> None:
        target = self.root / "secret"
        target.write_text("host secret")

        def write_symlink(_invocation):
            os.symlink(target, self.root / "output" / "candidate-result.json")
            (self.root / "output" / "candidate.patch").write_text("patch")
            (self.root / "output" / "trajectory.jsonl").write_text("{}\n")

        runtime = FakeContainerRuntime(
            RuntimeResult(0, "", "", 0.1, False, False, HASH_C),
            on_run=write_symlink,
        )
        runner = FullCandidateContainerRunner(
            runtime=runtime,
            image_repository="candidate",
            image_digest=HASH_C,
            entrypoint=("node", "/candidate/pi.mjs"),
            policy=self.policy,
            proxy_policy=self.proxy,
            immutable_control_roots=(self.root / "control",),
            mounts_factory=lambda _request: self.mounts,
            evaluator=FakeOutsideEvaluator(),
            workspace_claim_root=self.root / "claims",
        )
        with self.assertRaisesRegex(ContainerIsolationError, "open candidate output safely"):
            with patch.object(Path, "is_socket", return_value=True):
                runner.run(self.request, self.root / "evidence")
        for item in (self.root / "output").iterdir():
            item.unlink()
        with self.assertRaisesRegex(ContainerIsolationError, "already used"):
            with patch.object(Path, "is_socket", return_value=True):
                runner.run(self.request, self.root / "evidence2")


if __name__ == "__main__":
    unittest.main()
