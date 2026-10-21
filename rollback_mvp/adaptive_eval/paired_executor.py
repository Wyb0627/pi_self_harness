"""Identity-bound paired execution with no incomplete-pair imputation."""

from __future__ import annotations

import dataclasses
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Protocol, Sequence, TypeVar

from .catalogue import require_task_ids
from .schemas import (
    CatalogueManifest,
    EXPECTED_DATASET_MANIFEST_SHA256,
    PairExecutionError,
    ValidationError,
    ExperimentConfig,
    canonical_json_bytes,
    hash_json,
    require_sha256,
    sha256_bytes,
)
from .state import atomic_json, atomic_write, freeze_file_once


T = TypeVar("T")
ProgressFactory = Callable[[Iterable[T], str, int], Iterable[T]]


def required_tqdm(items: Iterable[T], description: str, total: int) -> Iterable[T]:
    """Load tqdm at experiment time; absence is terminal, never a silent plain loop."""
    try:
        from tqdm import tqdm
    except ImportError as error:
        raise PairExecutionError(
            "tqdm is required for experimental execution but is not installed"
        ) from error
    return tqdm(items, desc=description, total=total, unit="pair")


@dataclass(frozen=True, slots=True)
class FrozenTaskPlan:
    schema_version: int
    dataset_manifest_hash: str
    catalogue_hash: str
    parent_artifact_hash: str
    child_artifact_hash: str
    pre_audit_task_ids: tuple[str, ...]
    audit_task_ids: tuple[str, ...]
    final_task_ids: tuple[str, ...]
    selection_manifest_hash: str
    config_hash: str

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValidationError("Frozen task plan schema_version must be 1")
        if not self.final_task_ids:
            raise ValidationError("Frozen task plan cannot be empty")
        if self.dataset_manifest_hash != EXPECTED_DATASET_MANIFEST_SHA256:
            raise ValidationError("Frozen task plan uses a non-DGM-200 dataset")
        for name in (
            "dataset_manifest_hash",
            "catalogue_hash",
            "parent_artifact_hash",
            "child_artifact_hash",
            "selection_manifest_hash",
            "config_hash",
        ):
            require_sha256(getattr(self, name), name)
        for name in ("pre_audit_task_ids", "audit_task_ids", "final_task_ids"):
            values = getattr(self, name)
            if len(values) != len(set(values)):
                raise ValidationError(f"{name} contains duplicates")
        if set(self.pre_audit_task_ids) & set(self.audit_task_ids):
            raise ValidationError("Pre-audit and audit task IDs overlap")
        if self.final_task_ids != self.pre_audit_task_ids + self.audit_task_ids:
            raise ValidationError("Final task IDs must be pre-audit IDs followed by audit IDs")

    @property
    def manifest_hash(self) -> str:
        """Hash of the immutable selection-manifest.json used by every artifact."""
        return self.selection_manifest_hash

    @property
    def plan_hash(self) -> str:
        return hash_json(dataclasses.asdict(self))


@dataclass(frozen=True, slots=True)
class ModelSettings:
    provider: str
    model_id: str
    model_revision: str
    inference_settings: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if not self.provider or not self.model_id or not self.model_revision:
            raise ValidationError("Model provider, ID, and revision are required")
        if len(self.inference_settings) != len(dict(self.inference_settings)):
            raise ValidationError("Duplicate model inference setting keys")


@dataclass(frozen=True, slots=True)
class ExecutionSettings:
    model: ModelSettings
    timeout_seconds: int
    token_budget: int
    retry_budget: int
    tool_budget: int
    runner_image: str
    runner_image_digest: str
    evaluator_image: str
    evaluator_image_digest: str
    runner_revision: str
    evaluator_revision: str
    container_policy_hash: str

    def __post_init__(self) -> None:
        if min(self.timeout_seconds, self.token_budget, self.tool_budget) <= 0:
            raise ValidationError("Execution time, token, and tool budgets must be positive")
        if self.retry_budget < 0:
            raise ValidationError("retry_budget cannot be negative")
        for name in (
            "runner_image",
            "evaluator_image",
            "runner_revision",
            "evaluator_revision",
        ):
            if not getattr(self, name):
                raise ValidationError(f"{name} must be non-empty")
        for name in (
            "runner_image_digest",
            "evaluator_image_digest",
            "container_policy_hash",
        ):
            require_sha256(getattr(self, name), name)


@dataclass(frozen=True, slots=True)
class ArtifactRef:
    role: str
    artifact_hash: str
    source_path: str

    def __post_init__(self) -> None:
        if self.role not in {"parent", "child", "counterfactual"}:
            raise ValidationError(f"Invalid artifact role: {self.role}")
        require_sha256(self.artifact_hash, "artifact_hash")
        if not self.source_path:
            raise ValidationError("Artifact source_path must be non-empty")


@dataclass(frozen=True, slots=True)
class ExecutionRequest:
    task_instance_id: str
    task_repo: str
    task_base_commit: str
    task_problem_statement: str
    artifact: ArtifactRef
    parent_artifact_hash: str
    child_artifact_hash: str
    dataset_manifest_hash: str
    final_manifest_hash: str
    settings: ExecutionSettings

    def __post_init__(self) -> None:
        for name in (
            "task_instance_id",
            "task_repo",
            "task_base_commit",
            "task_problem_statement",
        ):
            if not getattr(self, name):
                raise ValidationError(f"{name} must be non-empty")
        for name in (
            "parent_artifact_hash",
            "child_artifact_hash",
            "dataset_manifest_hash",
            "final_manifest_hash",
        ):
            require_sha256(getattr(self, name), name)
        expected = {
            "parent": self.parent_artifact_hash,
            "child": self.child_artifact_hash,
        }.get(self.artifact.role)
        if expected is not None and self.artifact.artifact_hash != expected:
            raise ValidationError(
                f"{self.artifact.role} artifact hash does not match paired identity"
            )

    @property
    def identity_payload(self) -> dict[str, Any]:
        return self.paired_identity_payload | {
            "artifact_role": self.artifact.role,
            "artifact_hash": self.artifact.artifact_hash,
        }

    @property
    def paired_identity_payload(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "task_instance_id": self.task_instance_id,
            "task_repo": self.task_repo,
            "task_base_commit": self.task_base_commit,
            "parent_artifact_hash": self.parent_artifact_hash,
            "child_artifact_hash": self.child_artifact_hash,
            "dataset_manifest_hash": self.dataset_manifest_hash,
            "final_manifest_hash": self.final_manifest_hash,
            "model": dataclasses.asdict(self.settings.model),
            "budgets": {
                "timeout_seconds": self.settings.timeout_seconds,
                "token_budget": self.settings.token_budget,
                "retry_budget": self.settings.retry_budget,
                "tool_budget": self.settings.tool_budget,
            },
            "runner": {
                "image": self.settings.runner_image,
                "image_digest": self.settings.runner_image_digest,
                "revision": self.settings.runner_revision,
            },
            "evaluator": {
                "image": self.settings.evaluator_image,
                "image_digest": self.settings.evaluator_image_digest,
                "revision": self.settings.evaluator_revision,
            },
            "container_policy_hash": self.settings.container_policy_hash,
        }

    @property
    def identity_hash(self) -> str:
        return hash_json(self.identity_payload)

    @property
    def paired_identity_hash(self) -> str:
        return hash_json(self.paired_identity_payload)


@dataclass(frozen=True, slots=True)
class ArtifactObservation:
    execution_identity_hash: str
    status: str
    resolved: bool
    input_tokens: int
    output_tokens: int
    cost: float
    latency_seconds: float
    trajectory_hash: str
    result_hash: str
    trajectory_artifact: str
    result_artifact: str
    public_summary: str

    def __post_init__(self) -> None:
        require_sha256(self.execution_identity_hash, "execution_identity_hash")
        require_sha256(self.trajectory_hash, "trajectory_hash")
        require_sha256(self.result_hash, "result_hash")
        for name in ("trajectory_artifact", "result_artifact"):
            value = Path(getattr(self, name))
            if value.is_absolute() or len(value.parts) != 1 or value.name in {"", ".", ".."}:
                raise PairExecutionError(f"{name} must be a single relative filename")
        if self.status != "completed":
            raise PairExecutionError(f"Artifact observation is incomplete: {self.status}")
        if any(
            not math.isfinite(value) or value < 0
            for value in (self.input_tokens, self.output_tokens, self.cost, self.latency_seconds)
        ):
            raise PairExecutionError("Observation telemetry cannot be negative")
        if not isinstance(self.resolved, bool) or not self.public_summary:
            raise PairExecutionError("Observation lacks resolved/public summary fields")


class ArtifactRunner(Protocol):
    def run(self, request: ExecutionRequest, evidence_dir: Path) -> ArtifactObservation: ...


@dataclass(frozen=True, slots=True)
class PairResult:
    task_instance_id: str
    final_manifest_hash: str
    parent_identity_hash: str
    child_identity_hash: str
    paired_identity_hash: str
    paired_identity_payload: dict[str, Any]
    parent: ArtifactObservation
    child: ArtifactObservation
    execution_order: tuple[str, str]
    pair_hash: str

    @property
    def delta(self) -> int:
        return int(self.child.resolved) - int(self.parent.resolved)


def pair_result_hash(value: Mapping[str, Any]) -> str:
    return sha256_bytes(canonical_json_bytes(value))


class PairedExecutor:
    def __init__(
        self,
        *,
        catalogue: CatalogueManifest,
        plan: FrozenTaskPlan,
        settings: ExecutionSettings,
        experiment_config: ExperimentConfig,
        selection_manifest_path: Path,
        runner: ArtifactRunner,
        output_root: Path,
        progress_factory: ProgressFactory = required_tqdm,
    ) -> None:
        require_task_ids(catalogue, plan.final_task_ids)
        if plan.dataset_manifest_hash != catalogue.dataset_manifest_hash:
            raise PairExecutionError("Frozen task plan uses a different dataset manifest")
        if plan.catalogue_hash != catalogue.catalogue_hash:
            raise PairExecutionError("Frozen task plan uses a different catalogue hash")
        if plan.config_hash != experiment_config.config_hash:
            raise PairExecutionError("Frozen task plan uses a different experiment config")
        if (
            settings.timeout_seconds != experiment_config.per_task_timeout_seconds
            or settings.token_budget != experiment_config.per_task_token_budget
            or settings.retry_budget != experiment_config.per_task_retry_budget
            or settings.tool_budget != experiment_config.per_task_tool_budget
        ):
            raise PairExecutionError(
                "Execution settings do not match frozen per-task experiment budgets"
            )
        try:
            selection_manifest = json.loads(selection_manifest_path.read_text())
        except (OSError, json.JSONDecodeError) as error:
            raise PairExecutionError(f"Cannot load selection manifest: {error}") from error
        if not isinstance(selection_manifest, dict):
            raise PairExecutionError("Selection manifest must be an object")
        declared_hash = selection_manifest.get("manifest_hash")
        unhashed_manifest = {
            key: value for key, value in selection_manifest.items() if key != "manifest_hash"
        }
        actual_hash = hash_json(unhashed_manifest)
        if declared_hash != actual_hash or actual_hash != plan.selection_manifest_hash:
            raise PairExecutionError("Selection manifest content/hash does not match frozen plan")
        expected_fields = {
            "dataset_manifest_hash": plan.dataset_manifest_hash,
            "catalogue_hash": plan.catalogue_hash,
            "parent_artifact_hash": plan.parent_artifact_hash,
            "child_artifact_hash": plan.child_artifact_hash,
            "config_hash": plan.config_hash,
            "final_task_ids": list(plan.final_task_ids),
            "pre_audit_task_ids": list(plan.pre_audit_task_ids),
            "audit_task_ids": list(plan.audit_task_ids),
        }
        for field, expected in expected_fields.items():
            if selection_manifest.get(field) != expected:
                raise PairExecutionError(f"Selection manifest {field} differs from frozen plan")
        self.catalogue = catalogue
        self.plan = plan
        self.settings = settings
        self.experiment_config = experiment_config
        self.runner = runner
        self.output_root = output_root
        self.progress_factory = progress_factory
        freeze_file_once(
            output_root / "frozen-task-plan.json",
            dataclasses.asdict(plan)
            | {
                "final_manifest_hash": plan.manifest_hash,
                "plan_hash": plan.plan_hash,
            },
        )

    def _request(self, task_id: str, artifact: ArtifactRef) -> ExecutionRequest:
        card = self.catalogue.by_id[task_id]
        return ExecutionRequest(
            task_instance_id=task_id,
            task_repo=card.repo,
            task_base_commit=card.base_commit,
            task_problem_statement=card.problem_statement,
            artifact=artifact,
            parent_artifact_hash=self.plan.parent_artifact_hash,
            child_artifact_hash=self.plan.child_artifact_hash,
            dataset_manifest_hash=self.plan.dataset_manifest_hash,
            final_manifest_hash=self.plan.manifest_hash,
            settings=self.settings,
        )

    def _load_or_run(self, request: ExecutionRequest, evidence_dir: Path) -> ArtifactObservation:
        request_payload = dataclasses.asdict(request) | {
            "execution_identity": request.identity_payload,
            "execution_identity_hash": request.identity_hash,
        }
        freeze_file_once(evidence_dir / "request.json", request_payload)
        observation_path = evidence_dir / "observation.json"
        if observation_path.exists():
            try:
                raw = json.loads(observation_path.read_text())
                observation = ArtifactObservation(**raw)
            except (OSError, json.JSONDecodeError, TypeError, PairExecutionError) as error:
                raise PairExecutionError(
                    f"Invalid cached observation at {observation_path}: {error}"
                ) from error
            if observation.execution_identity_hash != request.identity_hash:
                raise PairExecutionError("Cached observation execution identity mismatch")
            self._validate_observation_artifacts(observation, evidence_dir)
            return observation
        try:
            observation = self.runner.run(request, evidence_dir)
        except BaseException as error:
            atomic_json(
                evidence_dir / f"exception-{time.time_ns()}.json",
                {
                    "type": type(error).__name__,
                    "message": str(error),
                    "execution_identity_hash": request.identity_hash,
                },
            )
            raise
        if observation.execution_identity_hash != request.identity_hash:
            atomic_json(
                evidence_dir / "identity-mismatch.json",
                {
                    "expected": request.identity_hash,
                    "found": observation.execution_identity_hash,
                },
            )
            raise PairExecutionError("Artifact runner returned the wrong execution identity")
        self._validate_observation_artifacts(observation, evidence_dir)
        atomic_json(observation_path, dataclasses.asdict(observation))
        return observation

    @staticmethod
    def _validate_observation_artifacts(
        observation: ArtifactObservation, evidence_dir: Path
    ) -> None:
        expected = (
            (observation.trajectory_artifact, observation.trajectory_hash),
            (observation.result_artifact, observation.result_hash),
        )
        for filename, expected_hash in expected:
            path = evidence_dir / filename
            if path.is_symlink() or not path.is_file():
                raise PairExecutionError(f"Observation evidence file is missing/unsafe: {path}")
            if sha256_bytes(path.read_bytes()) != expected_hash:
                raise PairExecutionError(f"Observation evidence hash mismatch: {path}")

    def run_pairs(self, parent: ArtifactRef, child: ArtifactRef) -> tuple[PairResult, ...]:
        if parent.role != "parent" or child.role != "child":
            raise PairExecutionError("run_pairs requires parent and child artifact roles")
        results: list[PairResult] = []
        tasks = self.progress_factory(
            self.plan.final_task_ids, "paired adaptive evaluation", len(self.plan.final_task_ids)
        )
        for task_id in tasks:
            requests = {
                "parent": self._request(task_id, parent),
                "child": self._request(task_id, child),
            }
            order = (
                ("parent", "child")
                if int(sha256_bytes(f"{self.plan.manifest_hash}\0{task_id}".encode()), 16) % 2 == 0
                else ("child", "parent")
            )
            observations: dict[str, ArtifactObservation] = {}
            for role in order:
                observations[role] = self._load_or_run(
                    requests[role], self.output_root / "pairs" / task_id / role
                )
            payload = {
                "task_instance_id": task_id,
                "final_manifest_hash": self.plan.manifest_hash,
                "parent_identity_hash": requests["parent"].identity_hash,
                "child_identity_hash": requests["child"].identity_hash,
                "paired_identity_hash": requests["parent"].paired_identity_hash,
                "paired_identity_payload": requests["parent"].paired_identity_payload,
                "parent": dataclasses.asdict(observations["parent"]),
                "child": dataclasses.asdict(observations["child"]),
                "execution_order": order,
            }
            result = PairResult(
                task_instance_id=task_id,
                final_manifest_hash=self.plan.manifest_hash,
                parent_identity_hash=requests["parent"].identity_hash,
                child_identity_hash=requests["child"].identity_hash,
                paired_identity_hash=requests["parent"].paired_identity_hash,
                paired_identity_payload=requests["parent"].paired_identity_payload,
                parent=observations["parent"],
                child=observations["child"],
                execution_order=order,
                pair_hash=pair_result_hash(payload),
            )
            freeze_file_once(
                self.output_root / "pairs" / task_id / "pair-result.json",
                dataclasses.asdict(result),
            )
            results.append(result)
        return tuple(results)

    def run_counterfactual(
        self, artifact: ArtifactRef, plan: FrozenTaskPlan
    ) -> tuple[ArtifactObservation, ...]:
        if artifact.role != "counterfactual":
            raise PairExecutionError("Counterfactual execution requires counterfactual role")
        if plan != self.plan:
            raise PairExecutionError(
                "Counterfactual must use the identical frozen final task manifest"
            )
        observations: list[ArtifactObservation] = []
        tasks = self.progress_factory(
            plan.final_task_ids, "counterfactual adaptive evaluation", len(plan.final_task_ids)
        )
        for task_id in tasks:
            request = self._request(task_id, artifact)
            observations.append(
                self._load_or_run(
                    request,
                    self.output_root
                    / "counterfactuals"
                    / artifact.artifact_hash
                    / task_id,
                )
            )
        return tuple(observations)


class FakeArtifactRunner:
    def __init__(
        self, outcomes: Mapping[tuple[str, str], bool], *, identity_override: str | None = None
    ) -> None:
        self.outcomes = dict(outcomes)
        self.identity_override = identity_override
        self.requests: list[ExecutionRequest] = []

    def run(self, request: ExecutionRequest, evidence_dir: Path) -> ArtifactObservation:
        self.requests.append(request)
        key = (request.task_instance_id, request.artifact.role)
        if key not in self.outcomes:
            raise PairExecutionError(f"Fake runner has no outcome for {key}")
        trajectory = canonical_json_bytes(
            {"task": request.task_instance_id, "role": request.artifact.role}
        )
        result = canonical_json_bytes({"resolved": self.outcomes[key]})
        atomic_write(evidence_dir / "trajectory.jsonl", trajectory)
        atomic_write(evidence_dir / "evaluation-result.json", result)
        return ArtifactObservation(
            execution_identity_hash=self.identity_override or request.identity_hash,
            status="completed",
            resolved=self.outcomes[key],
            input_tokens=10,
            output_tokens=2,
            cost=0.01,
            latency_seconds=0.1,
            trajectory_hash=sha256_bytes(trajectory),
            result_hash=sha256_bytes(result),
            trajectory_artifact="trajectory.jsonl",
            result_artifact="evaluation-result.json",
            public_summary="fake public result",
        )
