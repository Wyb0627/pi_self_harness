"""Full-candidate container boundary; never executes evolved Pi on the host."""

from __future__ import annotations

import dataclasses
import json
import os
import stat
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Protocol, Sequence

from .paired_executor import (
    ArtifactObservation,
    ArtifactRunner,
    ExecutionRequest,
)
from .schemas import (
    ContainerIsolationError,
    ValidationError,
    canonical_json_bytes,
    hash_json,
    require_sha256,
    sha256_bytes,
    source_tree_hash,
)
from .state import atomic_json, atomic_write, freeze_file_once


MODEL_PROXY_REQUEST_SCHEMA = {
    "schema_version": 1,
    "fields": {
        "execution_identity_hash": "sha256",
        "model_id": "string",
        "model_revision": "string",
        "messages": "non_empty_array",
        "max_output_tokens": "positive_integer",
    },
}
MODEL_PROXY_REQUEST_SCHEMA_HASH = hash_json(MODEL_PROXY_REQUEST_SCHEMA)


@dataclass(frozen=True, slots=True)
class ContainerPolicy:
    schema_version: int
    runtime: str
    network_mode: str
    user: str
    read_only_root: bool
    cap_drop_all: bool
    no_new_privileges: bool
    pids_limit: int
    memory_limit: str
    cpu_limit: str
    tmpfs_size: str
    seccomp_profile_path: str
    seccomp_profile_hash: str
    max_output_file_bytes: int
    max_output_total_bytes: int

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValidationError("Container policy schema_version must be 1")
        if self.runtime != "docker":
            raise ValidationError("Only the explicitly validated Docker runtime is supported")
        if self.network_mode != "none":
            raise ValidationError("Candidate container must use network_mode=none")
        if not all((self.read_only_root, self.cap_drop_all, self.no_new_privileges)):
            raise ValidationError(
                "Candidate container requires read-only root, cap-drop ALL, and no-new-privileges"
            )
        if self.user in {"", "0", "root"}:
            raise ValidationError("Candidate container must use a non-root user")
        if self.pids_limit <= 0:
            raise ValidationError("pids_limit must be positive")
        for name in ("memory_limit", "cpu_limit", "tmpfs_size"):
            if not getattr(self, name):
                raise ValidationError(f"{name} must be explicit")
        if not Path(self.seccomp_profile_path).is_absolute():
            raise ValidationError("seccomp_profile_path must be absolute")
        require_sha256(self.seccomp_profile_hash, "seccomp_profile_hash")
        if self.max_output_file_bytes <= 0:
            raise ValidationError("max_output_file_bytes must be positive")
        if self.max_output_total_bytes < self.max_output_file_bytes:
            raise ValidationError(
                "max_output_total_bytes must cover at least one output file"
            )

    @property
    def policy_hash(self) -> str:
        return hash_json(dataclasses.asdict(self))


@dataclass(frozen=True, slots=True)
class ModelProxyPolicy:
    schema_version: int
    socket_path: str
    model_id: str
    model_revision: str
    request_schema_hash: str
    max_input_tokens: int
    max_output_tokens: int

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValidationError("Model proxy policy schema_version must be 1")
        path = Path(self.socket_path)
        if not path.is_absolute():
            raise ValidationError("Model proxy socket_path must be absolute")
        if not self.model_id or not self.model_revision:
            raise ValidationError("Model proxy model ID and revision are required")
        if self.request_schema_hash != MODEL_PROXY_REQUEST_SCHEMA_HASH:
            raise ValidationError("Model proxy request schema hash is not the frozen contract")
        if min(self.max_input_tokens, self.max_output_tokens) <= 0:
            raise ValidationError("Model proxy token limits must be positive")

    def validate_request(
        self, payload: object, *, execution_identity_hash: str
    ) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise ContainerIsolationError("Model proxy request must be a JSON object")
        expected_fields = {
            "execution_identity_hash",
            "model_id",
            "model_revision",
            "messages",
            "max_output_tokens",
        }
        if set(payload) != expected_fields:
            raise ContainerIsolationError(
                f"Model proxy request fields must be exactly {sorted(expected_fields)}"
            )
        if payload["execution_identity_hash"] != execution_identity_hash:
            raise ContainerIsolationError("Model proxy execution identity mismatch")
        if payload["model_id"] != self.model_id:
            raise ContainerIsolationError("Model proxy model ID mismatch")
        if payload["model_revision"] != self.model_revision:
            raise ContainerIsolationError("Model proxy model revision mismatch")
        if not isinstance(payload["messages"], list) or not payload["messages"]:
            raise ContainerIsolationError("Model proxy messages must be a non-empty list")
        max_output_tokens = payload["max_output_tokens"]
        if (
            isinstance(max_output_tokens, bool)
            or not isinstance(max_output_tokens, int)
            or not 0 < max_output_tokens <= self.max_output_tokens
        ):
            raise ContainerIsolationError("Model proxy output-token request exceeds policy")
        return payload


@dataclass(frozen=True, slots=True)
class ContainerMounts:
    candidate_source: str
    task_workspace: str
    public_task_input: str
    candidate_output: str
    model_proxy_socket: str


@dataclass(frozen=True, slots=True)
class ContainerInvocation:
    image_reference: str
    command: tuple[str, ...]
    environment: tuple[tuple[str, str], ...]
    mounts: ContainerMounts
    policy: ContainerPolicy
    timeout_seconds: int

    @property
    def invocation_hash(self) -> str:
        return hash_json(dataclasses.asdict(self))


@dataclass(frozen=True, slots=True)
class RuntimeResult:
    exit_code: int
    stdout: str
    stderr: str
    duration_seconds: float
    oom_killed: bool
    timed_out: bool
    resolved_image_digest: str


@dataclass(frozen=True, slots=True)
class IsolationAttestation:
    restricted_proxy_enforced: bool
    storage_quota_enforced: bool
    timeout_cleanup_enforced: bool
    fresh_workspace_enforced: bool

    def validate(self) -> None:
        if not all(dataclasses.asdict(self).values()):
            raise ContainerIsolationError(
                "Runtime cannot attest proxy, storage quota, timeout cleanup, and fresh workspace"
            )


class ContainerRuntime(Protocol):
    def attest(self, invocation: ContainerInvocation) -> IsolationAttestation: ...

    def verify(self, invocation: ContainerInvocation) -> None: ...

    def run(self, invocation: ContainerInvocation) -> RuntimeResult: ...


class ModelProxyBudgetLedger:
    """Append-only, controller-side accounting for a single execution identity."""

    def __init__(
        self, root: Path, policy: ModelProxyPolicy, execution_identity_hash: str
    ) -> None:
        require_sha256(execution_identity_hash, "execution_identity_hash")
        self.root = root
        self.policy = policy
        self.execution_identity_hash = execution_identity_hash
        self.input_tokens = 0
        self.output_tokens = 0
        for path in sorted(root.glob("*.json")):
            try:
                record = json.loads(path.read_text())
            except (OSError, json.JSONDecodeError) as error:
                raise ContainerIsolationError(f"Invalid model proxy ledger {path}: {error}") from error
            if record.get("execution_identity_hash") != execution_identity_hash:
                raise ContainerIsolationError("Model proxy ledger identity mismatch")
            self.input_tokens += record.get("input_tokens", -1)
            self.output_tokens += record.get("output_tokens", -1)
        if self.input_tokens < 0 or self.output_tokens < 0:
            raise ContainerIsolationError("Model proxy ledger contains invalid token counts")

    def reserve_request(self, payload: object, estimated_input_tokens: int) -> None:
        self.policy.validate_request(
            payload, execution_identity_hash=self.execution_identity_hash
        )
        if estimated_input_tokens <= 0:
            raise ContainerIsolationError("Proxy input-token estimate must be positive")
        if self.input_tokens + estimated_input_tokens > self.policy.max_input_tokens:
            raise ContainerIsolationError("Model proxy input-token budget exceeded")
        requested_output = payload["max_output_tokens"]
        if self.output_tokens + requested_output > self.policy.max_output_tokens:
            raise ContainerIsolationError("Model proxy output-token budget exceeded")

    def append_usage(
        self, *, input_tokens: int, output_tokens: int, response_hash: str
    ) -> None:
        require_sha256(response_hash, "response_hash")
        if input_tokens < 0 or output_tokens < 0:
            raise ContainerIsolationError("Model proxy usage cannot be negative")
        if self.input_tokens + input_tokens > self.policy.max_input_tokens:
            raise ContainerIsolationError("Model proxy reported input tokens exceed budget")
        if self.output_tokens + output_tokens > self.policy.max_output_tokens:
            raise ContainerIsolationError("Model proxy reported output tokens exceed budget")
        sequence = len(list(self.root.glob("*.json")))
        atomic_json(
            self.root / f"{sequence:06d}.json",
            {
                "sequence": sequence,
                "execution_identity_hash": self.execution_identity_hash,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "response_hash": response_hash,
            },
        )
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens


class OutsideEvaluator(Protocol):
    def evaluate(
        self,
        request: ExecutionRequest,
        candidate_result_path: Path,
        candidate_patch_path: Path,
        trajectory_path: Path,
        evidence_dir: Path,
    ) -> ArtifactObservation: ...


def _overlaps(left: Path, right: Path) -> bool:
    return left == right or left in right.parents or right in left.parents


def read_regular_file_no_follow(path: Path, max_bytes: int) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ContainerIsolationError(f"Cannot open candidate output safely: {path}: {error}") from error
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ContainerIsolationError(f"Candidate output is not a regular file: {path}")
        if metadata.st_size > max_bytes:
            raise ContainerIsolationError(f"Candidate output exceeds size limit: {path}")
        content = os.read(descriptor, max_bytes + 1)
        if len(content) > max_bytes:
            raise ContainerIsolationError(f"Candidate output exceeds size limit: {path}")
        return content
    finally:
        os.close(descriptor)


def hash_candidate_source(path: Path) -> str:
    try:
        return source_tree_hash(path)
    except ValidationError as error:
        raise ContainerIsolationError(str(error)) from error


def build_invocation(
    *,
    request: ExecutionRequest,
    image_repository: str,
    image_digest: str,
    entrypoint: Sequence[str],
    mounts: ContainerMounts,
    policy: ContainerPolicy,
    proxy_policy: ModelProxyPolicy,
    immutable_control_roots: Sequence[Path],
) -> ContainerInvocation:
    require_sha256(image_digest, "image_digest")
    if request.settings.container_policy_hash != policy.policy_hash:
        raise ContainerIsolationError(
            "Execution identity container policy hash does not match invocation policy"
        )
    seccomp_path = Path(policy.seccomp_profile_path)
    if not seccomp_path.is_file():
        raise ContainerIsolationError(f"Seccomp profile is unavailable: {seccomp_path}")
    if sha256_bytes(seccomp_path.read_bytes()) != policy.seccomp_profile_hash:
        raise ContainerIsolationError("Seccomp profile hash does not match container policy")
    if request.settings.model.model_id != proxy_policy.model_id:
        raise ContainerIsolationError("Execution model does not match proxy policy")
    if request.settings.model.model_revision != proxy_policy.model_revision:
        raise ContainerIsolationError("Execution model revision does not match proxy policy")
    if (
        proxy_policy.max_input_tokens + proxy_policy.max_output_tokens
        != request.settings.token_budget
    ):
        raise ContainerIsolationError(
            "Model proxy token limits must exactly partition the execution token budget"
        )
    if not entrypoint or any(not item for item in entrypoint):
        raise ContainerIsolationError("Candidate entrypoint must be explicit")
    paths = {
        name: Path(value).resolve()
        for name, value in dataclasses.asdict(mounts).items()
    }
    socket = paths.pop("model_proxy_socket")
    for name, path in paths.items():
        if not path.exists():
            raise ContainerIsolationError(f"Required {name} path does not exist: {path}")
    if not socket.exists() or not socket.is_socket():
        raise ContainerIsolationError(f"Restricted model proxy socket is unavailable: {socket}")
    controls = [root.resolve() for root in immutable_control_roots]
    if not controls:
        raise ContainerIsolationError("immutable_control_roots must be non-empty")
    for name, path in paths.items():
        for control in controls:
            if _overlaps(path, control):
                raise ContainerIsolationError(
                    f"Candidate mount {name} overlaps immutable control-plane data: {control}"
                )
    if len(set(paths.values())) != len(paths):
        raise ContainerIsolationError("Candidate container mount sources must be distinct")
    path_items = list(paths.items())
    for index, (left_name, left_path) in enumerate(path_items):
        for right_name, right_path in path_items[index + 1 :]:
            if _overlaps(left_path, right_path):
                raise ContainerIsolationError(
                    f"Candidate mounts overlap: {left_name}={left_path}, "
                    f"{right_name}={right_path}"
                )
    if paths["candidate_source"] != Path(request.artifact.source_path).resolve():
        raise ContainerIsolationError(
            "Candidate source mount does not match the identity-bound artifact source"
        )
    if hash_candidate_source(paths["candidate_source"]) != request.artifact.artifact_hash:
        raise ContainerIsolationError(
            "Candidate source content hash does not match the artifact identity"
        )
    if image_digest != request.settings.runner_image_digest:
        raise ContainerIsolationError(
            "Candidate image digest does not match the execution identity"
        )
    try:
        public_input = json.loads(paths["public_task_input"].read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise ContainerIsolationError(f"Public task input is invalid: {error}") from error
    expected_public_input = {
        "instance_id": request.task_instance_id,
        "repo": request.task_repo,
        "base_commit": request.task_base_commit,
        "problem_statement": request.task_problem_statement,
    }
    if public_input != expected_public_input:
        raise ContainerIsolationError(
            "Public task input does not match the execution identity or contains extra fields"
        )
    environment = (
        ("ADAPTIVE_EVAL_EXECUTION_IDENTITY", request.identity_hash),
        ("ADAPTIVE_EVAL_MODEL_SOCKET", "/run/model-proxy/socket"),
        ("ADAPTIVE_EVAL_TASK_INPUT", "/input/task.json"),
        ("ADAPTIVE_EVAL_OUTPUT", "/output/candidate-result.json"),
    )
    return ContainerInvocation(
        image_reference=f"{image_repository}@sha256:{image_digest}",
        command=tuple(entrypoint),
        environment=environment,
        mounts=ContainerMounts(**{key: str(value) for key, value in paths.items()}, model_proxy_socket=str(socket)),
        policy=policy,
        timeout_seconds=request.settings.timeout_seconds,
    )


class DockerCliRuntime:
    """Strict Docker adapter. It has no host-process candidate fallback."""

    def __init__(self, docker_binary: str = "docker") -> None:
        if not docker_binary:
            raise ValidationError("docker_binary must be explicit")
        self.docker_binary = docker_binary

    def attest(self, invocation: ContainerInvocation) -> IsolationAttestation:
        raise ContainerIsolationError(
            "Docker CLI runtime lacks attested quota-backed mounts, restricted proxy "
            "enforcement, fresh workspaces, and timeout cleanup; refusing execution"
        )

    def verify(self, invocation: ContainerInvocation) -> None:
        try:
            version = subprocess.run(
                [self.docker_binary, "version", "--format", "{{.Server.Version}}"],
                text=True,
                capture_output=True,
                timeout=10,
                check=False,
                env={"PATH": os.environ.get("PATH", "")},
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise ContainerIsolationError(f"Docker runtime verification failed: {error}") from error
        if version.returncode != 0 or not version.stdout.strip():
            raise ContainerIsolationError(
                "Docker daemon is unavailable; full-candidate isolation cannot be claimed: "
                f"{version.stderr.strip()}"
            )
        inspect = subprocess.run(
            [
                self.docker_binary,
                "image",
                "inspect",
                invocation.image_reference,
                "--format",
                "{{json .RepoDigests}}",
            ],
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
            env={"PATH": os.environ.get("PATH", "")},
        )
        if inspect.returncode != 0 or invocation.image_reference not in inspect.stdout:
            raise ContainerIsolationError(
                "Digest-pinned candidate image is unavailable or does not match: "
                f"{inspect.stderr.strip()}"
            )

    def _command(self, invocation: ContainerInvocation) -> list[str]:
        mounts = invocation.mounts
        command = [
            self.docker_binary,
            "run",
            "--rm",
            "--network",
            "none",
            "--read-only",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "--security-opt",
            f"seccomp={invocation.policy.seccomp_profile_path}",
            "--user",
            invocation.policy.user,
            "--pids-limit",
            str(invocation.policy.pids_limit),
            "--memory",
            invocation.policy.memory_limit,
            "--cpus",
            invocation.policy.cpu_limit,
            "--tmpfs",
            f"/tmp:rw,noexec,nosuid,nodev,size={invocation.policy.tmpfs_size}",
            "--mount",
            f"type=bind,src={mounts.candidate_source},dst=/candidate,readonly",
            "--mount",
            f"type=bind,src={mounts.task_workspace},dst=/workspace",
            "--mount",
            f"type=bind,src={mounts.public_task_input},dst=/input/task.json,readonly",
            "--mount",
            f"type=bind,src={mounts.candidate_output},dst=/output",
            "--mount",
            f"type=bind,src={mounts.model_proxy_socket},dst=/run/model-proxy/socket",
            "--workdir",
            "/workspace",
        ]
        for key, value in invocation.environment:
            command.extend(("--env", f"{key}={value}"))
        return command + [invocation.image_reference, *invocation.command]

    def run(self, invocation: ContainerInvocation) -> RuntimeResult:
        self.verify(invocation)
        self.attest(invocation).validate()
        started = time.monotonic()
        try:
            result = subprocess.run(
                self._command(invocation),
                text=True,
                capture_output=True,
                timeout=invocation.timeout_seconds,
                check=False,
                env={"PATH": os.environ.get("PATH", "")},
            )
        except subprocess.TimeoutExpired as error:
            raise ContainerIsolationError(
                f"Candidate container exceeded timeout; no host fallback: {error}"
            ) from error
        duration = time.monotonic() - started
        return RuntimeResult(
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            duration_seconds=duration,
            oom_killed=False,
            timed_out=False,
            resolved_image_digest=invocation.image_reference.rsplit("sha256:", 1)[1],
        )


class FakeContainerRuntime:
    def __init__(
        self,
        result: RuntimeResult,
        *,
        verification_error: str = "",
        on_run: Callable[[ContainerInvocation], None] | None = None,
    ) -> None:
        self.result = result
        self.verification_error = verification_error
        self.invocations: list[ContainerInvocation] = []
        self.on_run = on_run

    def verify(self, invocation: ContainerInvocation) -> None:
        if self.verification_error:
            raise ContainerIsolationError(self.verification_error)

    def attest(self, invocation: ContainerInvocation) -> IsolationAttestation:
        return IsolationAttestation(True, True, True, True)

    def run(self, invocation: ContainerInvocation) -> RuntimeResult:
        self.verify(invocation)
        self.attest(invocation).validate()
        self.invocations.append(invocation)
        if self.on_run is not None:
            self.on_run(invocation)
        return self.result


class FullCandidateContainerRunner(ArtifactRunner):
    def __init__(
        self,
        *,
        runtime: ContainerRuntime,
        image_repository: str,
        image_digest: str,
        entrypoint: Sequence[str],
        policy: ContainerPolicy,
        proxy_policy: ModelProxyPolicy,
        immutable_control_roots: Sequence[Path],
        mounts_factory: Any,
        evaluator: OutsideEvaluator,
        workspace_claim_root: Path,
    ) -> None:
        self.runtime = runtime
        self.image_repository = image_repository
        self.image_digest = image_digest
        self.entrypoint = tuple(entrypoint)
        self.policy = policy
        self.proxy_policy = proxy_policy
        self.immutable_control_roots = tuple(immutable_control_roots)
        self.mounts_factory = mounts_factory
        self.evaluator = evaluator
        self.workspace_claim_root = workspace_claim_root

    def run(self, request: ExecutionRequest, evidence_dir: Path) -> ArtifactObservation:
        mounts = self.mounts_factory(request)
        invocation = build_invocation(
            request=request,
            image_repository=self.image_repository,
            image_digest=self.image_digest,
            entrypoint=self.entrypoint,
            mounts=mounts,
            policy=self.policy,
            proxy_policy=self.proxy_policy,
            immutable_control_roots=self.immutable_control_roots,
        )
        atomic_json(
            evidence_dir / "container-invocation.json",
            dataclasses.asdict(invocation) | {"invocation_hash": invocation.invocation_hash},
        )
        output_dir = Path(mounts.candidate_output)
        if any(output_dir.iterdir()):
            raise ContainerIsolationError(
                "Candidate output directory must be controller-created and empty"
            )
        workspace = Path(mounts.task_workspace).resolve()
        claim_path = self.workspace_claim_root / (
            sha256_bytes(str(workspace).encode()) + ".json"
        )
        if claim_path.exists():
            raise ContainerIsolationError("Task workspace was already used")
        freeze_file_once(
            claim_path,
            {
                "workspace": str(workspace),
                "execution_identity_hash": request.identity_hash,
            },
        )
        self.runtime.attest(invocation).validate()
        result = self.runtime.run(invocation)
        atomic_json(evidence_dir / "container-runtime-result.json", dataclasses.asdict(result))
        if result.timed_out or result.oom_killed or result.exit_code != 0:
            raise ContainerIsolationError(
                "Candidate container did not complete cleanly: "
                f"exit={result.exit_code}, timeout={result.timed_out}, oom={result.oom_killed}"
            )
        if result.resolved_image_digest != self.image_digest:
            raise ContainerIsolationError("Runtime resolved a different candidate image digest")
        output_path = output_dir / "candidate-result.json"
        patch_path = output_dir / "candidate.patch"
        trajectory_path = output_dir / "trajectory.jsonl"
        output_bytes = {
            path.name: read_regular_file_no_follow(
                path, self.policy.max_output_file_bytes
            )
            for path in (output_path, patch_path, trajectory_path)
        }
        if sum(map(len, output_bytes.values())) > self.policy.max_output_total_bytes:
            raise ContainerIsolationError("Candidate output exceeds aggregate size limit")
        try:
            payload = json.loads(output_bytes[output_path.name])
        except (UnicodeError, json.JSONDecodeError) as error:
            raise ContainerIsolationError(f"Candidate result is invalid: {error}") from error
        required = {
            "execution_identity_hash",
            "status",
            "input_tokens",
            "output_tokens",
            "cost",
            "public_summary",
            "patch_sha256",
        }
        if not isinstance(payload, dict) or set(payload) != required:
            raise ContainerIsolationError("Candidate result has the wrong schema")
        if payload["execution_identity_hash"] != request.identity_hash:
            raise ContainerIsolationError("Candidate result execution identity mismatch")
        require_sha256(payload["patch_sha256"], "patch_sha256")
        if sha256_bytes(output_bytes[patch_path.name]) != payload["patch_sha256"]:
            raise ContainerIsolationError("Candidate patch hash does not match result metadata")
        if payload["status"] != "completed":
            raise ContainerIsolationError("Candidate result status is incomplete")
        for field in ("input_tokens", "output_tokens"):
            if (
                isinstance(payload[field], bool)
                or not isinstance(payload[field], int)
                or payload[field] < 0
            ):
                raise ContainerIsolationError(f"Candidate result {field} is invalid")
        if (
            isinstance(payload["cost"], bool)
            or not isinstance(payload["cost"], (int, float))
            or payload["cost"] < 0
        ):
            raise ContainerIsolationError("Candidate result cost is invalid")
        if not isinstance(payload["public_summary"], str) or not payload["public_summary"]:
            raise ContainerIsolationError("Candidate result public_summary is invalid")
        persisted_result = evidence_dir / "candidate-result.json"
        persisted_patch = evidence_dir / "candidate.patch"
        persisted_trajectory = evidence_dir / "trajectory.jsonl"
        atomic_write(persisted_result, output_bytes[output_path.name])
        atomic_write(persisted_patch, output_bytes[patch_path.name])
        atomic_write(persisted_trajectory, output_bytes[trajectory_path.name])
        observation = self.evaluator.evaluate(
            request,
            persisted_result,
            persisted_patch,
            persisted_trajectory,
            evidence_dir,
        )
        if observation.execution_identity_hash != request.identity_hash:
            raise ContainerIsolationError("Outside evaluator returned the wrong identity")
        return observation
