"""Production runner for matched held-out DGM/P2 strategy-and-tool evolution."""

from __future__ import annotations

import dataclasses
import fcntl
import hashlib
import json
import math
import os
import random
import shutil
import socket
import subprocess
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

try:
    from tqdm import tqdm as _tqdm
except ModuleNotFoundError:
    _tqdm = None

from rollback_mvp.adaptive_eval.schemas import hash_json
from rollback_mvp.adaptive_eval.state import (
    AppendOnlyState,
    atomic_json,
    atomic_write,
    freeze_file_once,
)
from rollback_mvp.dgm_evolve.artifacts import (
    ArtifactContent,
    ArtifactValidationError,
    CandidateTool,
    MutationDelta,
    materialize_lineage,
    mutation_delta_from_json,
    mutation_delta_to_json,
    validate_mutation_delta,
    validate_strategy_text,
)
from rollback_mvp.dgm_evolve.rf_clm import (
    apply_repair_plan,
    repair_first_lineage,
)
from rollback_mvp.orchestrate_endpoint_200 import (
    PAID_CONFIRMATION,
    command_environment,
    create_solver_workspace,
    distribution,
    docker_capture,
    ensure_instance_image,
    evaluate_patch,
    exact_mcnemar_p_value,
    load_manifest,
    materialize_inputs,
    paired_bootstrap_interval,
    run_logged,
    sha256_bytes,
    sha256_file,
    sha256_ids,
    total_reported_tokens,
    wilson_interval,
)


SCHEMA_VERSION = 1
PROTOCOL_REVISION = "matched-dgm-pi-v2"
FULL_MANIFEST_SHA256 = (
    "3fb913fbc73a05c1f7cae3b708c976374632820b58377aab5de08b742f96c967"
)
PARTITION_SHA256 = {
    "small": "b8909d87321bf7e9277e82baff8b2a739a3e1e76585ec512ae8ad4b6eef86591",
    "medium": "bf1cde9b2590f7813cc0cbb43a3ce0a9fccbdd163083891ff96b9abc82e4c06f",
    "big": "76a8b81f0c044a64c928ab46312b5eb69c3728ab7d39c4fe6239a790797906cd",
}
EXPECTED_STAGE_SIZES = {"small": 10, "medium": 50, "big": 140}
EXPECTED_SWEBENCH_REVISION = "dc4c087c2b9e4cefebf2e3d201d27e362d899e0f"
DEFAULT_MODEL_PROVIDER = "rollback-deepseek"
DEFAULT_MODEL_ID = "byteplus/deepseek-v4-flash-ga"
EXPERIMENT_ARMS = {"dgm", "p2"}
P0_TASK_CONFIG_FIELDS = (
    "model_provider",
    "model_id",
    "per_task_token_cap",
    "per_task_output_token_cap",
    "agent_timeout_seconds",
    "evaluator_timeout_seconds",
    "image_build_timeout_seconds",
    "image_build_retries",
    "image_build_retry_delay_seconds",
    "inter_task_delay_seconds",
    "task_rollout_count",
    "concurrency",
    "smoke",
)


class DgmEvolutionError(RuntimeError):
    """Base class for fail-closed DGM-on-Pi errors."""


class ConfigurationError(DgmEvolutionError):
    """Frozen configuration or identity is invalid."""


class BudgetExhausted(DgmEvolutionError):
    """A phase exhausted its independent reserve."""


class ObservationInvalid(DgmEvolutionError):
    """A task observation cannot enter scientific metrics."""


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    run_id: str
    experiment_seed: int
    arm: str = "dgm"
    model_provider: str = DEFAULT_MODEL_PROVIDER
    model_id: str = DEFAULT_MODEL_ID
    proposal_slots: int = 10
    proposals_per_wave: int = 2
    promotion_fraction: float = 0.4
    search_token_cap: int | None = None
    search_active_seconds_cap: int = 108_000
    final_endpoint_token_cap: int = 80_000_000
    reference_endpoint_token_cap: int = 80_000_000
    endpoint_active_seconds_cap: int = 108_000
    per_task_token_cap: int = 512_000
    per_task_output_token_cap: int = 65_536
    mutation_token_cap: int = 64_000
    mutation_output_token_cap: int = 32_768
    agent_timeout_seconds: int = 3_600
    mutation_timeout_seconds: int = 900
    evaluator_timeout_seconds: int = 1_800
    image_build_timeout_seconds: int = 7_200
    image_build_retries: int = 2
    image_build_retry_delay_seconds: float = 30.0
    inter_task_delay_seconds: float = 90.0
    task_rollout_count: int = 1
    concurrency: int = 1
    smoke: bool = False
    smoke_small_tasks: int = 1
    smoke_medium_tasks: int = 0
    smoke_endpoint_tasks: int = 2
    adaptive_task_budget: int = 4
    rf_clm_singleton_budget: int = 1

    def __post_init__(self) -> None:
        if not self.run_id.strip():
            raise ConfigurationError("run_id must be non-empty")
        if self.arm not in EXPERIMENT_ARMS:
            raise ConfigurationError(f"arm must be one of {sorted(EXPERIMENT_ARMS)}")
        positive = (
            "proposal_slots",
            "proposals_per_wave",
            "search_active_seconds_cap",
            "final_endpoint_token_cap",
            "reference_endpoint_token_cap",
            "endpoint_active_seconds_cap",
            "per_task_token_cap",
            "per_task_output_token_cap",
            "mutation_token_cap",
            "mutation_output_token_cap",
            "agent_timeout_seconds",
            "mutation_timeout_seconds",
            "evaluator_timeout_seconds",
            "image_build_timeout_seconds",
            "task_rollout_count",
            "concurrency",
            "adaptive_task_budget",
            "rf_clm_singleton_budget",
        )
        for name in positive:
            if getattr(self, name) <= 0:
                raise ConfigurationError(f"{name} must be positive")
        if self.proposal_slots % self.proposals_per_wave:
            raise ConfigurationError(
                "proposal_slots must be divisible by proposals_per_wave"
            )
        if not 0 <= self.promotion_fraction <= 1:
            raise ConfigurationError("promotion_fraction must be in [0, 1]")
        if self.concurrency != 1:
            raise ConfigurationError("The local matched protocol requires concurrency=1")
        if self.task_rollout_count != 1:
            raise ConfigurationError("This protocol currently supports pass@1 only")
        if self.per_task_output_token_cap > self.per_task_token_cap:
            raise ConfigurationError(
                "per_task_output_token_cap cannot exceed per_task_token_cap"
            )
        if self.search_token_cap is not None and self.search_token_cap <= 0:
            raise ConfigurationError("search_token_cap must be positive or null")
        if self.adaptive_task_budget > 4:
            raise ConfigurationError("adaptive_task_budget cannot exceed 4")

    @property
    def max_waves(self) -> int:
        return self.proposal_slots // self.proposals_per_wave

    @property
    def config_hash(self) -> str:
        return hash_json(dataclasses.asdict(self))


@dataclass(frozen=True, slots=True)
class RuntimePaths:
    repo_root: Path
    full_manifest: Path
    output_root: Path
    agent_dir: Path
    swebench_source: Path
    image_builder: Path
    pi_runner: Path
    mutation_runner: Path
    swebench_python: str
    node: str = "node"
    docker_host: str | None = None
    build_wheelhouse: Path | None = None


@dataclass(frozen=True, slots=True)
class ArchiveEntry:
    artifact_hash: str
    parent_artifact_hash: str | None
    score_60: float
    resolved_60: int
    evaluated_tasks: int
    functioning_child_count: int
    functioning_child_slots: tuple[int, ...]
    insertion_ordinal: int


@dataclass(frozen=True, slots=True)
class TaskObservation:
    instance_id: str
    artifact_hash: str
    phase: str
    resolved: bool
    status: str
    valid: bool
    reported_tokens: int
    token_telemetry_complete: bool
    image_build_seconds: float
    agent_duration_seconds: float
    evaluator_duration_seconds: float
    patch_sha256: str
    identity_hash: str
    observation_hash: str


@dataclass(frozen=True, slots=True)
class RunnerClassification:
    valid: bool
    status: str
    should_grade_patch: bool
    telemetry_complete: bool


def directory_hash(path: Path) -> str:
    if not path.is_dir():
        raise ConfigurationError(f"Execution directory is missing: {path}")
    records = []
    for item in sorted(path.rglob("*")):
        if item.is_symlink():
            raise ConfigurationError(f"Execution directory contains symlink: {item}")
        if item.is_file():
            records.append(
                {
                    "path": item.relative_to(path).as_posix(),
                    "sha256": sha256_file(item),
                }
            )
    return hash_json(records)


def classify_runner_result(
    result: Mapping[str, Any],
    return_code: int,
) -> RunnerClassification:
    token_fields = (
        "inputTokens",
        "outputTokens",
        "cacheReadTokens",
        "cacheWriteTokens",
    )
    telemetry_complete = (
        result.get("tokenTelemetryAvailable") is not False
        and all(
            isinstance(result.get(field), int) and result[field] >= 0
            for field in token_fields
        )
    )
    if not telemetry_complete:
        return RunnerClassification(
            valid=False,
            status="missing_token_telemetry",
            should_grade_patch=False,
            telemetry_complete=False,
        )
    budget_aborted = bool(result.get("budgetAborted"))
    timeout_aborted = bool(result.get("timeoutAborted"))
    if budget_aborted or timeout_aborted:
        provider_error = result.get("providerError")
        error_text = str(result.get("error") or "")
        expected_abort = provider_error in {None, "This operation was aborted"} and (
            not error_text or "abort" in error_text.lower()
        )
        if not expected_abort:
            return RunnerClassification(
                valid=False,
                status="aborted_with_unexpected_error",
                should_grade_patch=False,
                telemetry_complete=True,
            )
        return RunnerClassification(
            valid=True,
            status=(
                "task_budget_exhausted_observed_zero"
                if budget_aborted
                else "task_timeout_observed_zero"
            ),
            should_grade_patch=False,
            telemetry_complete=True,
        )
    if result.get("error") or result.get("providerError") or return_code != 0:
        return RunnerClassification(
            valid=False,
            status="provider_or_runner_invalid",
            should_grade_patch=False,
            telemetry_complete=True,
        )
    if result.get("policyViolations"):
        return RunnerClassification(
            valid=True,
            status="policy_violation_observed_zero",
            should_grade_patch=False,
            telemetry_complete=True,
        )
    if not result.get("patch"):
        return RunnerClassification(
            valid=True,
            status="empty_patch_observed_zero",
            should_grade_patch=False,
            telemetry_complete=True,
        )
    return RunnerClassification(
        valid=True,
        status="completed",
        should_grade_patch=True,
        telemetry_complete=True,
    )


def mutation_failure_reason(result: Mapping[str, Any]) -> str:
    for field in ("error", "parseError", "providerError"):
        value = result.get(field)
        if isinstance(value, str) and value.strip():
            return value
    if result.get("budgetAborted"):
        return "Mutation proposer exceeded its frozen token budget."
    if result.get("timeoutAborted"):
        return "Mutation proposer exceeded its frozen time budget."
    if result.get("tokenTelemetryAvailable") is not True:
        return "Mutation proposer returned incomplete token telemetry."
    return "Mutation proposer returned valid=false without a specific error."


def utc_timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def role_manifest(
    full_manifest: Mapping[str, Any],
    *,
    role: str,
    stages: Sequence[str],
    source_manifest_hash: str,
) -> dict[str, Any]:
    if role not in {"evolve", "test"}:
        raise ConfigurationError(f"Unknown role manifest: {role}")
    subsets = full_manifest["dgm"]["subsets"]
    record_by_id = {
        entry["record"]["instance_id"]: entry for entry in full_manifest["records"]
    }
    ordered_ids: list[str] = []
    records = []
    for stage in stages:
        subset = subsets[stage]
        if subset["size"] != EXPECTED_STAGE_SIZES[stage]:
            raise ConfigurationError(f"Unexpected {stage} subset size")
        if subset["sha256"] != PARTITION_SHA256[stage]:
            raise ConfigurationError(f"Unexpected {stage} subset hash")
        for instance_id in subset["instance_ids"]:
            if instance_id in ordered_ids:
                raise ConfigurationError(f"Duplicate split task ID: {instance_id}")
            source = record_by_id.get(instance_id)
            if source is None:
                raise ConfigurationError(f"Split task is absent from manifest: {instance_id}")
            ordered_ids.append(instance_id)
            records.append(
                {
                    "ordinal": len(records),
                    "stage": stage,
                    "source_row_sha256": source["source_row_sha256"],
                    "record": source["record"],
                }
            )
    return {
        "schema_version": SCHEMA_VERSION,
        "role": role,
        "source_manifest_sha256": source_manifest_hash,
        "stages": list(stages),
        "partition_source_sha256": {
            stage: PARTITION_SHA256[stage] for stage in stages
        },
        "ordered_instance_ids_sha256": sha256_ids(ordered_ids),
        "task_count": len(records),
        "records": records,
    }


def build_split_contract(
    full_manifest: Mapping[str, Any],
    source_manifest_hash: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if source_manifest_hash != FULL_MANIFEST_SHA256:
        raise ConfigurationError("Frozen DGM-200 manifest hash mismatch")
    evolve = role_manifest(
        full_manifest,
        role="evolve",
        stages=("small", "medium"),
        source_manifest_hash=source_manifest_hash,
    )
    test = role_manifest(
        full_manifest,
        role="test",
        stages=("big",),
        source_manifest_hash=source_manifest_hash,
    )
    evolve_ids = [entry["record"]["instance_id"] for entry in evolve["records"]]
    test_ids = [entry["record"]["instance_id"] for entry in test["records"]]
    if len(evolve_ids) != 60 or len(test_ids) != 140:
        raise ConfigurationError("Role manifests must contain exactly 60/140 tasks")
    if set(evolve_ids) & set(test_ids):
        raise ConfigurationError("D_evolve and D_test overlap")
    binding = {
        "schema_version": SCHEMA_VERSION,
        "source_manifest_sha256": source_manifest_hash,
        "partition_source_sha256": PARTITION_SHA256,
        "evolve_task_count": 60,
        "evolve_ordered_ids_sha256": evolve["ordered_instance_ids_sha256"],
        "test_task_count": 140,
        "test_ordered_ids_sha256": test["ordered_instance_ids_sha256"],
        "declaration": (
            "Online search receives only evolve-60-manifest.json. D_test rows, "
            "IDs, issue text, embeddings, trajectories, and outcomes are absent "
            "from mutation and archive inputs."
        ),
    }
    return evolve, test, binding


def validate_evolve_manifest(manifest: Mapping[str, Any]) -> None:
    if manifest.get("role") != "evolve" or manifest.get("task_count") != 60:
        raise ConfigurationError("Search requires the frozen 60-task evolve manifest")
    records = manifest.get("records")
    if not isinstance(records, list) or len(records) != 60:
        raise ConfigurationError("Evolve manifest records are invalid")
    stages = [entry.get("stage") for entry in records]
    if stages != ["small"] * 10 + ["medium"] * 50:
        raise ConfigurationError("Evolve manifest is not literal small+medium order")
    ids = [entry["record"]["instance_id"] for entry in records]
    if sha256_ids(ids) != manifest.get("ordered_instance_ids_sha256"):
        raise ConfigurationError("Evolve manifest ordered-ID hash mismatch")


def validate_test_manifest(
    manifest: Mapping[str, Any],
    split_binding: Mapping[str, Any],
) -> None:
    if manifest.get("role") != "test" or manifest.get("task_count") != 140:
        raise ConfigurationError("Endpoint requires the frozen 140-task test manifest")
    records = manifest.get("records")
    if not isinstance(records, list) or len(records) != 140:
        raise ConfigurationError("Test manifest records are invalid")
    if any(entry.get("stage") != "big" for entry in records):
        raise ConfigurationError("Test manifest contains a non-big task")
    ids = [entry["record"]["instance_id"] for entry in records]
    digest = sha256_ids(ids)
    if digest != manifest.get("ordered_instance_ids_sha256"):
        raise ConfigurationError("Test manifest ordered-ID hash mismatch")
    if digest != split_binding.get("test_ordered_ids_sha256"):
        raise ConfigurationError("Test manifest differs from split binding")


def validate_strategy(strategy: str, evolve_task_ids: Sequence[str]) -> None:
    try:
        validate_strategy_text(strategy, evolve_task_ids)
    except ArtifactValidationError as error:
        raise ConfigurationError(str(error)) from error


def dgm_parent_weight(entry: ArchiveEntry) -> float:
    score_term = 1.0 / (1.0 + math.exp(-10.0 * (entry.score_60 - 0.5)))
    return score_term / (1 + entry.functioning_child_count)


def select_parent_hashes(
    entries: Sequence[ArchiveEntry],
    *,
    seed: int,
    wave: int,
    count: int,
) -> tuple[str, ...]:
    if not entries:
        raise ConfigurationError("Cannot select a parent from an empty archive")
    ordered = sorted(entries, key=lambda entry: entry.insertion_ordinal)
    weights = [dgm_parent_weight(entry) for entry in ordered]
    random_seed = int.from_bytes(
        hashlib.sha256(f"dgm-parent|{seed}|{wave}".encode()).digest()[:8],
        "big",
    )
    generator = random.Random(random_seed)
    return tuple(
        generator.choices(
            [entry.artifact_hash for entry in ordered],
            weights=weights,
            k=count,
        )
    )


def endpoint_order(
    artifact_hashes: Sequence[str],
    instance_id: str,
    seed: int,
) -> tuple[str, ...]:
    return tuple(
        sorted(
            artifact_hashes,
            key=lambda artifact: hashlib.sha256(
                f"endpoint-order|{seed}|{instance_id}|{artifact}".encode()
            ).hexdigest(),
        )
    )


class CostLedger:
    """Hash-chained append-only all-in cost ledger."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.records = self._load()
        self.charge_ids = {record["charge_id"] for record in self.records}

    def _load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        records = []
        previous_hash = "0" * 64
        for sequence, line in enumerate(self.path.read_text().splitlines()):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ConfigurationError(f"Invalid cost ledger line {sequence}") from error
            if record.get("sequence") != sequence:
                raise ConfigurationError("Cost ledger sequence mismatch")
            if record.get("previous_hash") != previous_hash:
                raise ConfigurationError("Cost ledger chain mismatch")
            unhashed = {
                key: value for key, value in record.items() if key != "entry_hash"
            }
            if hash_json(unhashed) != record.get("entry_hash"):
                raise ConfigurationError("Cost ledger entry hash mismatch")
            previous_hash = record["entry_hash"]
            records.append(record)
        return records

    def append(self, charge_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        if charge_id in self.charge_ids:
            return next(
                record for record in self.records if record["charge_id"] == charge_id
            )
        previous_hash = self.records[-1]["entry_hash"] if self.records else "0" * 64
        unhashed = {
            "sequence": len(self.records),
            "charge_id": charge_id,
            "payload": payload,
            "previous_hash": previous_hash,
        }
        record = {**unhashed, "entry_hash": hash_json(unhashed)}
        descriptor = os.open(
            self.path,
            os.O_WRONLY | os.O_APPEND | os.O_CREAT,
            0o600,
        )
        try:
            with os.fdopen(descriptor, "a", encoding="utf-8") as file:
                file.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
                file.flush()
                os.fsync(file.fileno())
        except BaseException:
            raise
        self.records.append(record)
        self.charge_ids.add(charge_id)
        return record

    def totals(self, budget_scope: str) -> dict[str, float | int]:
        payloads = [
            record["payload"]
            for record in self.records
            if record["payload"].get("budget_scope") == budget_scope
        ]
        return {
            "reported_tokens": sum(
                int(payload.get("reported_tokens", 0)) for payload in payloads
            ),
            "conservative_token_charge": sum(
                int(payload.get("conservative_token_charge", 0))
                for payload in payloads
            ),
            "budget_counted_tokens": sum(
                int(payload.get("reported_tokens", 0))
                + int(payload.get("conservative_token_charge", 0))
                for payload in payloads
            ),
            "active_seconds": round(
                sum(float(payload.get("active_seconds", 0.0)) for payload in payloads),
                3,
            ),
            "api_calls": sum(int(payload.get("api_calls", 0)) for payload in payloads),
            "task_executions": sum(
                int(payload.get("task_executions", 0)) for payload in payloads
            ),
        }


class DgmPiExperiment:
    def __init__(
        self,
        config: ExperimentConfig,
        paths: RuntimePaths,
        *,
        progress_factory: Callable[
            [Iterable[Any], str, int], Iterable[Any]
        ] | None = None,
    ) -> None:
        self.config = config
        self.paths = paths
        self.output_root = paths.output_root.resolve()
        self.events = AppendOnlyState(self.output_root / "state")
        self.ledger = CostLedger(self.output_root / "global-cost-ledger.jsonl")
        self.progress_factory = progress_factory or self._default_progress

    @staticmethod
    def _default_progress(
        items: Iterable[Any], description: str, total: int
    ) -> Iterable[Any]:
        if _tqdm is None:
            raise ConfigurationError(
                "tqdm is required for production execution; use the Conda base Python"
            )
        return _tqdm(items, desc=description, total=total, dynamic_ncols=True)

    @property
    def frozen_inputs(self) -> Path:
        return self.output_root / "frozen-inputs"

    @property
    def artifacts_root(self) -> Path:
        return self.output_root / "artifacts"

    @property
    def archive_path(self) -> Path:
        return self.output_root / "archive.json"

    @property
    def search_state_path(self) -> Path:
        return self.output_root / "search-state.json"

    @property
    def search_seal_path(self) -> Path:
        return self.output_root / "search-seal.json"

    @property
    def p0_import_contract_path(self) -> Path:
        return self.output_root / "p0-import-contract.json"

    @property
    def p0_import_completion_path(self) -> Path:
        return self.output_root / "p0-import-complete.json"

    @contextmanager
    def execution_lease(self, command: str) -> Iterator[None]:
        lock_path = self.output_root / ".execution.lock"
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_file = lock_path.open("a+", encoding="utf-8")
        try:
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                lock_file.seek(0)
                holder = lock_file.read().strip() or "unknown holder"
                raise ConfigurationError(
                    f"Experiment output is already active: {holder}"
                ) from error
            lock_file.seek(0)
            lock_file.truncate()
            lock_file.write(
                json.dumps(
                    {
                        "pid": os.getpid(),
                        "host": socket.gethostname(),
                        "command": command,
                        "acquired_at": utc_timestamp(),
                    },
                    sort_keys=True,
                )
                + "\n"
            )
            lock_file.flush()
            os.fsync(lock_file.fileno())
            yield
        finally:
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            finally:
                lock_file.close()

    def prepare(
        self,
        *,
        import_p0_from: Path | None = None,
    ) -> dict[str, Any]:
        protocol_lock_path = self.output_root / "protocol-lock.json"
        if protocol_lock_path.exists():
            protocol_lock = self._load_json(protocol_lock_path)
            if protocol_lock.get("config_hash") != self.config.config_hash:
                raise ConfigurationError(
                    "Existing protocol lock uses a different experiment config"
                )
            if import_p0_from is not None:
                self._import_p0(import_p0_from)
            elif (
                self.p0_import_contract_path.exists()
                and not self.p0_import_completion_path.exists()
            ):
                raise ConfigurationError(
                    "P0 import contract exists without a completion record"
                )
            return protocol_lock
        manifest, manifest_hash = load_manifest(self.paths.full_manifest)
        evolve, test, split_binding = build_split_contract(manifest, manifest_hash)
        self.output_root.mkdir(parents=True, exist_ok=True)
        evolve_hash = freeze_file_once(
            self.frozen_inputs / "evolve-60-manifest.json", evolve
        )
        split_hash = freeze_file_once(
            self.frozen_inputs / "split-binding.json", split_binding
        )
        # D_test content stays out of the online-search root until search seals.
        endpoint_commitment = {
            "schema_version": SCHEMA_VERSION,
            "role": "test_commitment",
            "task_count": test["task_count"],
            "ordered_instance_ids_sha256": test["ordered_instance_ids_sha256"],
            "role_manifest_hash": hash_json(test),
        }
        endpoint_commitment_hash = freeze_file_once(
            self.frozen_inputs / "test-140-commitment.json",
            endpoint_commitment,
        )
        fixed_policy = {
            "schema_version": SCHEMA_VERSION,
            "protocol_revision": PROTOCOL_REVISION,
            "name": f"held-out-adapted-{self.config.arm}-on-pi",
            "arm": self.config.arm,
            "mutable_surface": [
                "strategy.md",
                "tools.json",
                "handlers/*.py",
            ],
            "proposal_slots": self.config.proposal_slots,
            "proposals_per_wave": self.config.proposals_per_wave,
            "parent_selection": (
                "sampling with replacement proportional to "
                "sigmoid(10*(score_60-0.5))/(1+functioning_child_count)"
            ),
            "small_promotion_rule": (
                f"resolved >= ceil({self.config.promotion_fraction} * small_tasks)"
            ),
            "archive_rule": "keep every valid child with complete cumulative-60 evidence",
            "final_selection": (
                "highest score_60; then earliest insertion ordinal; then artifact hash"
            ),
            "endpoint_rule": "P0 and final artifact each run once on sealed big-140",
            "p0_reuse_rule": (
                "explicit pre-search audited import only; preserve source observation "
                "identity and bind exact evolve panel, task stack, evidence, archive, "
                "and cost ledger"
            ),
            "search_global_token_stop": self.config.search_token_cap,
            "search_active_seconds_cap": self.config.search_active_seconds_cap,
            "candidate_tools": (
                "trusted host proxy; generated handlers execute in the task image "
                "with network=none, artifact read-only, and task workspace read-write"
            ),
            "adaptive_gate": (
                {
                    "coverage_selection_mode": "agent_only",
                    "task_budget": self.config.adaptive_task_budget,
                    "same_repo_only": True,
                    "rf_clm": (
                        "repair-first minimal removal with dependency-safe replay"
                    ),
                }
                if self.config.arm == "p2"
                else None
            ),
        }
        fixed_policy_hash = freeze_file_once(
            self.frozen_inputs / "fixed-policy.json", fixed_policy
        )
        config_payload = {
            "schema_version": SCHEMA_VERSION,
            "config": dataclasses.asdict(self.config),
            "config_hash": self.config.config_hash,
        }
        config_hash = freeze_file_once(
            self.frozen_inputs / "experiment-config.json", config_payload
        )
        execution_stack = self._execution_stack_identity()
        execution_stack_hash = freeze_file_once(
            self.frozen_inputs / "execution-stack.json", execution_stack
        )
        p0_hash = self._write_artifact(
            strategy="",
            parent_hash=None,
            mutation_record={
                "kind": "P0",
                "summary": "Frozen Pi baseline with no added strategy.",
            },
        )
        control_plane = {
            "schema_version": SCHEMA_VERSION,
            "files": {
                str(Path(__file__).resolve().relative_to(self.paths.repo_root)): sha256_file(
                    Path(__file__).resolve()
                ),
                str(
                    self.paths.mutation_runner.resolve().relative_to(
                        self.paths.repo_root
                    )
                ): sha256_file(self.paths.mutation_runner),
                str(
                    self.paths.pi_runner.resolve().relative_to(self.paths.repo_root)
                ): sha256_file(self.paths.pi_runner),
                "rollback_mvp/candidate_tool_runtime.mjs": sha256_file(
                    self.paths.repo_root
                    / "rollback_mvp"
                    / "candidate_tool_runtime.mjs"
                ),
                "rollback_mvp/dgm_evolve/artifacts.py": sha256_file(
                    self.paths.repo_root
                    / "rollback_mvp"
                    / "dgm_evolve"
                    / "artifacts.py"
                ),
                "rollback_mvp/dgm_evolve/rf_clm.py": sha256_file(
                    self.paths.repo_root
                    / "rollback_mvp"
                    / "dgm_evolve"
                    / "rf_clm.py"
                ),
                "rollback_mvp/run_dgm_pi_evolution.py": sha256_file(
                    self.paths.repo_root
                    / "rollback_mvp"
                    / "run_dgm_pi_evolution.py"
                ),
            },
        }
        control_plane_hash = freeze_file_once(
            self.frozen_inputs / "control-plane-release-manifest.json",
            control_plane,
        )
        git_sha = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.paths.repo_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        git_status = subprocess.run(
            ["git", "status", "--short"],
            cwd=self.paths.repo_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        historical_root = (
            self.paths.repo_root
            / "research_output"
            / "clm_budgeted_evolution_20260924_125503"
            / "dgm200_run"
        )
        denylist = {
            "schema_version": SCHEMA_VERSION,
            "roots": [
                {
                    "path": str(historical_root.resolve()),
                    "summary_sha256": (
                        sha256_file(historical_root / "summary.json")
                        if (historical_root / "summary.json").exists()
                        else None
                    ),
                    "run_config_sha256": (
                        sha256_file(historical_root / "run_config.json")
                        if (historical_root / "run_config.json").exists()
                        else None
                    ),
                    "allowed_as_search_input": False,
                    "allowed_as_cache": False,
                }
            ],
        }
        denylist_hash = freeze_file_once(
            self.frozen_inputs / "historical-denylist.json", denylist
        )
        attestation = {
            "schema_version": SCHEMA_VERSION,
            "created_at": utc_timestamp(),
            "initial_harness_git_sha": git_sha,
            "initial_harness_source": "clean committed HEAD; dirty files excluded",
            "current_dirty_status_sha256": sha256_bytes(git_status.encode()),
            "pi_runner_sha256": sha256_file(self.paths.pi_runner),
            "mutation_runner_sha256": sha256_file(self.paths.mutation_runner),
            "agent_models_sha256": sha256_file(self.paths.agent_dir / "models.json"),
            "pi_package_sha256": sha256_file(
                self.paths.repo_root
                / "pi-rollback"
                / "node_modules"
                / "@earendil-works"
                / "pi-coding-agent"
                / "package.json"
            ),
            "swebench_revision": self._swebench_revision(),
            "p0_artifact_hash": p0_hash,
            "evolve_manifest_hash": evolve_hash,
            "split_binding_hash": split_hash,
            "endpoint_commitment_hash": endpoint_commitment_hash,
            "fixed_policy_hash": fixed_policy_hash,
            "experiment_config_hash": config_hash,
            "execution_stack_hash": execution_stack_hash,
            "control_plane_release_manifest_hash": control_plane_hash,
            "historical_denylist_hash": denylist_hash,
            "scope_limitation": (
                "Project-specific Pi strategy and tool evolution; Pi core and harness "
                "source remain frozen."
            ),
            "freshness_limitation": (
                "big-140 is isolated from this new search but has appeared in "
                "historical repository runs and human analysis."
            ),
        }
        attestation_hash = freeze_file_once(
            self.output_root / "cold-start-attestation.json", attestation
        )
        protocol_lock = {
            "schema_version": SCHEMA_VERSION,
            "protocol_revision": PROTOCOL_REVISION,
            "run_id": self.config.run_id,
            "arm": f"held-out-adapted-{self.config.arm}-on-pi",
            "confirmatory_status": "exploratory-single-seed",
            "config_hash": self.config.config_hash,
            "cold_start_attestation_hash": attestation_hash,
            "split_binding_hash": split_hash,
            "fixed_policy_hash": fixed_policy_hash,
            "execution_stack_hash": execution_stack_hash,
            "p0_artifact_hash": p0_hash,
            "search_budget_scope": "search",
            "reference_endpoint_budget_scope": "endpoint:p0",
            "final_endpoint_budget_scope": "endpoint:final",
            "d_test_visibility": "post-search-seal endpoint worker only",
            "model_revision_limitation": (
                "Provider exposes model ID but no immutable serving revision."
            ),
        }
        protocol_lock_hash = freeze_file_once(
            self.output_root / "protocol-lock.json", protocol_lock
        )
        if not self.events.events:
            self.events.append(
                "prepared",
                {
                    "protocol_lock_hash": protocol_lock_hash,
                    "config_hash": self.config.config_hash,
                    "p0_artifact_hash": p0_hash,
                },
            )
        if import_p0_from is not None:
            self._import_p0(import_p0_from)
        return protocol_lock

    def preflight(self, *, require_paid_runtime: bool) -> dict[str, Any]:
        protocol_lock = self._load_json(self.output_root / "protocol-lock.json")
        config_payload = self._load_json(
            self.frozen_inputs / "experiment-config.json"
        )
        if config_payload.get("config_hash") != self.config.config_hash:
            raise ConfigurationError("Experiment config differs from frozen lock")
        if protocol_lock.get("config_hash") != self.config.config_hash:
            raise ConfigurationError("Protocol lock config hash mismatch")
        control_plane = self._load_json(
            self.frozen_inputs / "control-plane-release-manifest.json"
        )
        for relative_path, expected_hash in control_plane["files"].items():
            path = self.paths.repo_root / relative_path
            if not path.is_file() or sha256_file(path) != expected_hash:
                raise ConfigurationError(
                    f"Control-plane file differs from frozen release: {relative_path}"
                )
        frozen_execution_stack = self._load_json(
            self.frozen_inputs / "execution-stack.json"
        )
        if frozen_execution_stack != self._execution_stack_identity():
            raise ConfigurationError("Execution stack differs from frozen identity")
        evolve = self._load_json(self.frozen_inputs / "evolve-60-manifest.json")
        validate_evolve_manifest(evolve)
        if (self.frozen_inputs / "test-140-manifest.json").exists():
            raise ConfigurationError(
                "D_test content exists in the online-search frozen input directory"
            )
        if (
            self.p0_import_contract_path.exists()
            or self.p0_import_completion_path.exists()
        ):
            self._validate_completed_p0_import()
        if self._swebench_revision() != EXPECTED_SWEBENCH_REVISION:
            raise ConfigurationError("SWE-bench runner revision mismatch")
        if not self.paths.agent_dir.is_dir():
            raise ConfigurationError("Agent directory is missing")
        if not self.paths.pi_runner.is_file() or not self.paths.mutation_runner.is_file():
            raise ConfigurationError("Pi runner or mutation runner is missing")
        if require_paid_runtime:
            if not os.environ.get("ROLLBACK_ENDPOINT_API_KEY"):
                raise ConfigurationError("ROLLBACK_ENDPOINT_API_KEY is required")
            environment = command_environment(self.paths.docker_host)
            docker = subprocess.run(
                ["docker", "info"],
                env=environment,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            if docker.returncode != 0:
                raise ConfigurationError(f"Docker is unavailable: {docker.stderr}")
            with socket.create_connection(("127.0.0.1", 8765), timeout=2):
                pass
            if _tqdm is None:
                raise ConfigurationError(
                    "Production execution requires tqdm in the orchestration Python"
                )
        return {
            "valid": True,
            "run_id": self.config.run_id,
            "config_hash": self.config.config_hash,
            "paid_runtime_checked": require_paid_runtime,
        }

    def run_search(self) -> dict[str, Any]:
        if self._endpoint_state_path().exists():
            raise ConfigurationError("Search cannot run after endpoint consumption starts")
        search_invalid_path = self.output_root / "search-invalid.json"
        if search_invalid_path.exists():
            invalid = self._load_json(search_invalid_path)
            raise ObservationInvalid(
                f"Search is terminally invalid: {invalid.get('reason')}"
            )
        if self.search_seal_path.exists():
            return self._load_json(self.search_seal_path)
        if (
            self.p0_import_contract_path.exists()
            or self.p0_import_completion_path.exists()
        ):
            self._validate_completed_p0_import()
        evolve = self._load_json(self.frozen_inputs / "evolve-60-manifest.json")
        validate_evolve_manifest(evolve)
        runtime_inputs = self.output_root / "runtime" / "evolve-inputs"
        dataset_path, task_path = materialize_inputs(evolve, runtime_inputs)
        records = evolve["records"]
        small_records = [entry for entry in records if entry["stage"] == "small"]
        medium_records = [entry for entry in records if entry["stage"] == "medium"]
        if self.config.smoke:
            small_records = small_records[: self.config.smoke_small_tasks]
            medium_records = medium_records[: self.config.smoke_medium_tasks]
        p0_hash = self._load_json(self.output_root / "protocol-lock.json")[
            "p0_artifact_hash"
        ]
        archive = self._load_archive()
        if not archive:
            try:
                p0_observations = self._evaluate_records(
                    artifact_hash_value=p0_hash,
                    records=[*small_records, *medium_records],
                    role_manifest=evolve,
                    dataset_path=dataset_path,
                    task_path=task_path,
                    phase="search-p0",
                    budget_scope="search",
                )
                self._require_complete_valid_panel(
                    p0_observations,
                    len(small_records) + len(medium_records),
                )
            except (ObservationInvalid, BudgetExhausted) as error:
                invalid = {
                    "schema_version": SCHEMA_VERSION,
                    "terminal_state": "P0_EVALUATION_INVALID",
                    "reason": str(error),
                    "cost": self.ledger.totals("search"),
                }
                atomic_json(search_invalid_path, invalid)
                self.events.append("search_invalid", invalid)
                raise
            resolved = sum(observation.resolved for observation in p0_observations)
            entry = ArchiveEntry(
                artifact_hash=p0_hash,
                parent_artifact_hash=None,
                score_60=resolved / len(p0_observations),
                resolved_60=resolved,
                evaluated_tasks=len(p0_observations),
                functioning_child_count=0,
                functioning_child_slots=(),
                insertion_ordinal=0,
            )
            archive = [entry]
            self._write_archive(archive)
            self.events.append(
                "p0_evaluated",
                {
                    "artifact_hash": p0_hash,
                    "resolved": resolved,
                    "tasks": len(p0_observations),
                },
            )

        search_state = self._load_search_state()
        next_slot = int(search_state.get("next_slot", 0))
        while next_slot < self.config.proposal_slots:
            if self._phase_exhausted(
                "search",
                self.config.search_token_cap,
                self.config.search_active_seconds_cap,
                minimum_tokens=self.config.mutation_token_cap,
            ):
                break
            wave = next_slot // self.config.proposals_per_wave
            wave_path = self.output_root / "search" / "waves" / f"{wave:04d}.json"
            if wave_path.exists():
                wave_plan = self._load_json(wave_path)
                parent_hashes = tuple(wave_plan["parent_artifact_hashes"])
            else:
                parent_hashes = select_parent_hashes(
                    archive,
                    seed=self.config.experiment_seed,
                    wave=wave,
                    count=self.config.proposals_per_wave,
                )
                wave_plan = {
                    "schema_version": SCHEMA_VERSION,
                    "wave": wave,
                    "slot_start": wave * self.config.proposals_per_wave,
                    "parent_artifact_hashes": parent_hashes,
                    "archive_hash": hash_json(
                        [dataclasses.asdict(entry) for entry in archive]
                    ),
                }
                freeze_file_once(wave_path, wave_plan)

            slot_in_wave = next_slot % self.config.proposals_per_wave
            parent_hash = parent_hashes[slot_in_wave]
            slot_dir = self.output_root / "search" / "slots" / f"{next_slot:04d}"
            terminal_path = slot_dir / "terminal.json"
            if terminal_path.exists():
                next_slot += 1
                search_state["next_slot"] = next_slot
                atomic_json(self.search_state_path, search_state)
                continue

            mutation = self._mutate(parent_hash, next_slot, evolve, task_path)
            if not mutation["valid"]:
                terminal = {
                    "schema_version": SCHEMA_VERSION,
                    "slot": next_slot,
                    "wave": wave,
                    "parent_artifact_hash": parent_hash,
                    "terminal_state": "CANDIDATE_INVALID_REJECTED",
                    "reason": mutation_failure_reason(mutation),
                }
                atomic_json(terminal_path, terminal)
                self.events.append("candidate_invalid", terminal)
                next_slot += 1
                search_state["next_slot"] = next_slot
                atomic_json(self.search_state_path, search_state)
                continue

            child_hash = mutation["artifact_hash"]
            existing_child = next(
                (
                    entry
                    for entry in archive
                    if entry.artifact_hash == child_hash
                ),
                None,
            )
            parent_entry = next(
                entry
                for entry in archive
                if entry.artifact_hash == parent_hash
            )
            if (
                existing_child is not None
                and next_slot in parent_entry.functioning_child_slots
                and existing_child.parent_artifact_hash == parent_hash
            ):
                terminal = {
                    "schema_version": SCHEMA_VERSION,
                    "slot": next_slot,
                    "wave": wave,
                    "parent_artifact_hash": parent_hash,
                    "child_artifact_hash": child_hash,
                    "terminal_state": "ARCHIVED",
                    "resolved": existing_child.resolved_60,
                    "tasks": existing_child.evaluated_tasks,
                    "score_60": existing_child.score_60,
                    "recovered_from_archive": True,
                }
                atomic_json(terminal_path, terminal)
                self.events.append("slot_terminal", terminal)
                next_slot += 1
                search_state["next_slot"] = next_slot
                atomic_json(self.search_state_path, search_state)
                continue
            if existing_child is not None:
                terminal = {
                    "schema_version": SCHEMA_VERSION,
                    "slot": next_slot,
                    "wave": wave,
                    "parent_artifact_hash": parent_hash,
                    "child_artifact_hash": child_hash,
                    "terminal_state": "CANDIDATE_DUPLICATE_REJECTED",
                }
                atomic_json(terminal_path, terminal)
                self.events.append("slot_terminal", terminal)
                next_slot += 1
                search_state["next_slot"] = next_slot
                atomic_json(self.search_state_path, search_state)
                continue
            gate = self._apply_p2_gate(
                parent_hash=parent_hash,
                child_hash=child_hash,
                mutation=mutation,
                slot=next_slot,
                evolve_manifest=evolve,
                dataset_path=dataset_path,
                task_path=task_path,
            )
            if not gate["accepted"]:
                terminal = {
                    "schema_version": SCHEMA_VERSION,
                    "slot": next_slot,
                    "wave": wave,
                    "parent_artifact_hash": parent_hash,
                    "child_artifact_hash": child_hash,
                    "terminal_state": gate["terminal_state"],
                    "adaptive_gate": gate,
                }
                atomic_json(terminal_path, terminal)
                self.events.append("slot_terminal", terminal)
                next_slot += 1
                search_state["next_slot"] = next_slot
                atomic_json(self.search_state_path, search_state)
                continue
            child_hash = gate["artifact_hash"]
            repaired_duplicate = next(
                (
                    entry
                    for entry in archive
                    if entry.artifact_hash == child_hash
                ),
                None,
            )
            if (
                repaired_duplicate is not None
                and next_slot in parent_entry.functioning_child_slots
                and repaired_duplicate.parent_artifact_hash == parent_hash
            ):
                terminal = {
                    "schema_version": SCHEMA_VERSION,
                    "slot": next_slot,
                    "wave": wave,
                    "parent_artifact_hash": parent_hash,
                    "child_artifact_hash": child_hash,
                    "terminal_state": "ARCHIVED",
                    "resolved": repaired_duplicate.resolved_60,
                    "tasks": repaired_duplicate.evaluated_tasks,
                    "score_60": repaired_duplicate.score_60,
                    "recovered_from_archive": True,
                    "adaptive_gate": gate,
                }
                atomic_json(terminal_path, terminal)
                self.events.append("slot_terminal", terminal)
                next_slot += 1
                search_state["next_slot"] = next_slot
                atomic_json(self.search_state_path, search_state)
                continue
            if repaired_duplicate is not None:
                terminal = {
                    "schema_version": SCHEMA_VERSION,
                    "slot": next_slot,
                    "wave": wave,
                    "parent_artifact_hash": parent_hash,
                    "child_artifact_hash": child_hash,
                    "terminal_state": "CANDIDATE_DUPLICATE_REJECTED",
                    "adaptive_gate": gate,
                }
                atomic_json(terminal_path, terminal)
                self.events.append("slot_terminal", terminal)
                next_slot += 1
                search_state["next_slot"] = next_slot
                atomic_json(self.search_state_path, search_state)
                continue
            try:
                small_observations = self._evaluate_records(
                    artifact_hash_value=child_hash,
                    records=small_records,
                    role_manifest=evolve,
                    dataset_path=dataset_path,
                    task_path=task_path,
                    phase=f"search-slot-{next_slot:04d}-small",
                    budget_scope="search",
                )
                self._require_complete_valid_panel(
                    small_observations, len(small_records)
                )
                small_resolved = sum(
                    observation.resolved for observation in small_observations
                )
                threshold = (
                    0
                    if self.config.smoke
                    else math.ceil(
                        self.config.promotion_fraction * len(small_records)
                    )
                )
                if small_resolved < threshold:
                    terminal = {
                        "schema_version": SCHEMA_VERSION,
                        "slot": next_slot,
                        "wave": wave,
                        "parent_artifact_hash": parent_hash,
                        "child_artifact_hash": child_hash,
                        "terminal_state": "REJECT_SMALL",
                        "small_resolved": small_resolved,
                        "small_tasks": len(small_records),
                        "promotion_threshold": threshold,
                        "adaptive_gate": gate,
                    }
                else:
                    medium_observations = self._evaluate_records(
                        artifact_hash_value=child_hash,
                        records=medium_records,
                        role_manifest=evolve,
                        dataset_path=dataset_path,
                        task_path=task_path,
                        phase=f"search-slot-{next_slot:04d}-medium",
                        budget_scope="search",
                    )
                    self._require_complete_valid_panel(
                        medium_observations, len(medium_records)
                    )
                    all_observations = [*small_observations, *medium_observations]
                    resolved = sum(
                        observation.resolved for observation in all_observations
                    )
                    archive = self._increment_child_count(
                        archive, parent_hash, next_slot
                    )
                    archive.append(
                        ArchiveEntry(
                            artifact_hash=child_hash,
                            parent_artifact_hash=parent_hash,
                            score_60=resolved / len(all_observations),
                            resolved_60=resolved,
                            evaluated_tasks=len(all_observations),
                            functioning_child_count=0,
                            functioning_child_slots=(),
                            insertion_ordinal=len(archive),
                        )
                    )
                    self._write_archive(archive)
                    terminal = {
                        "schema_version": SCHEMA_VERSION,
                        "slot": next_slot,
                        "wave": wave,
                        "parent_artifact_hash": parent_hash,
                        "child_artifact_hash": child_hash,
                        "terminal_state": "ARCHIVED",
                        "resolved": resolved,
                        "tasks": len(all_observations),
                        "score_60": resolved / len(all_observations),
                        "adaptive_gate": gate,
                    }
            except (ObservationInvalid, BudgetExhausted) as error:
                terminal = {
                    "schema_version": SCHEMA_VERSION,
                    "slot": next_slot,
                    "wave": wave,
                    "parent_artifact_hash": parent_hash,
                    "child_artifact_hash": child_hash,
                    "terminal_state": (
                        "SEARCH_BUDGET_EXHAUSTED"
                        if isinstance(error, BudgetExhausted)
                        else "EDGE_EVALUATION_INVALID"
                    ),
                    "reason": str(error),
                    "adaptive_gate": gate,
                }
            atomic_json(terminal_path, terminal)
            self.events.append("slot_terminal", terminal)
            next_slot += 1
            search_state["next_slot"] = next_slot
            atomic_json(self.search_state_path, search_state)
            if terminal["terminal_state"] == "SEARCH_BUDGET_EXHAUSTED":
                break

        archive = self._load_archive()
        selected = min(
            archive,
            key=lambda entry: (
                -entry.score_60,
                entry.insertion_ordinal,
                entry.artifact_hash,
            ),
        )
        seal = {
            "schema_version": SCHEMA_VERSION,
            "sealed_at": utc_timestamp(),
            "reason": (
                "proposal_slots_exhausted"
                if next_slot >= self.config.proposal_slots
                else "search_budget_exhausted"
            ),
            "completed_proposal_slots": next_slot,
            "archive_entries": len(archive),
            "final_artifact_hash": selected.artifact_hash,
            "final_score_60": selected.score_60,
            "archive_hash": hash_json(
                [dataclasses.asdict(entry) for entry in archive]
            ),
            "search_cost": self.ledger.totals("search"),
        }
        freeze_file_once(self.search_seal_path, seal)
        if not any(event.event_type == "search_sealed" for event in self.events.events):
            self.events.append("search_sealed", seal)
        return seal

    def _apply_p2_gate(
        self,
        *,
        parent_hash: str,
        child_hash: str,
        mutation: Mapping[str, Any],
        slot: int,
        evolve_manifest: Mapping[str, Any],
        dataset_path: Path,
        task_path: Path,
    ) -> dict[str, Any]:
        if self.config.arm != "p2":
            return {
                "schema_version": SCHEMA_VERSION,
                "arm": "dgm",
                "accepted": True,
                "artifact_hash": child_hash,
                "terminal_state": "GATE_NOT_APPLICABLE",
            }
        gate_path = (
            self.output_root
            / "search"
            / "slots"
            / f"{slot:04d}"
            / "p2-gate.json"
        )
        if gate_path.exists():
            result = self._load_json(gate_path)
            if (
                result.get("parent_artifact_hash") != parent_hash
                or result.get("proposed_artifact_hash") != child_hash
            ):
                raise ConfigurationError("Persisted P2 gate identity mismatch")
            return result

        record_by_id = {
            entry["record"]["instance_id"]: entry
            for entry in evolve_manifest["records"]
        }
        probe_task_ids = tuple(mutation["probe_task_ids"])
        probe_records = [record_by_id[instance_id] for instance_id in probe_task_ids]
        expected_repo = mutation["repo"]
        if any(
            entry["record"]["repo"] != expected_repo for entry in probe_records
        ):
            raise ConfigurationError("P2 gate contains a cross-repository task")
        parent = self._evaluate_records(
            artifact_hash_value=parent_hash,
            records=probe_records,
            role_manifest=evolve_manifest,
            dataset_path=dataset_path,
            task_path=task_path,
            phase=f"p2-slot-{slot:04d}-gate-parent",
            budget_scope="search",
        )
        child = self._evaluate_records(
            artifact_hash_value=child_hash,
            records=probe_records,
            role_manifest=evolve_manifest,
            dataset_path=dataset_path,
            task_path=task_path,
            phase=f"p2-slot-{slot:04d}-gate-child",
            budget_scope="search",
        )
        regressions = tuple(
            parent_observation.instance_id
            for parent_observation, child_observation in zip(parent, child)
            if parent_observation.resolved and not child_observation.resolved
        )
        gate_pairs = [
            {
                "instance_id": parent_observation.instance_id,
                "parent_resolved": parent_observation.resolved,
                "child_resolved": child_observation.resolved,
                "parent_observation_hash": parent_observation.observation_hash,
                "child_observation_hash": child_observation.observation_hash,
            }
            for parent_observation, child_observation in zip(parent, child)
        ]
        if not regressions:
            result = {
                "schema_version": SCHEMA_VERSION,
                "arm": "p2",
                "coverage_selection_mode": "agent_only",
                "same_repo": expected_repo,
                "probe_task_ids": probe_task_ids,
                "parent_artifact_hash": parent_hash,
                "proposed_artifact_hash": child_hash,
                "accepted": True,
                "artifact_hash": child_hash,
                "terminal_state": "ADAPTIVE_GATE_PASSED",
                "pairs": gate_pairs,
                "rf_clm": None,
            }
            atomic_json(gate_path, result)
            return result

        full_lineage = self._artifact_lineage(child_hash)
        regression_records = [
            record_by_id[instance_id] for instance_id in regressions
        ]
        def evaluate_lineage(
            lineage: Sequence[MutationDelta],
            label: str,
        ) -> tuple[str, tuple[TaskObservation, ...]]:
            artifact = self._write_artifact(
                lineage=lineage,
                parent_hash=parent_hash,
                mutation_record={
                    "kind": "RF-CLM counterfactual",
                    "slot": slot,
                    "label": label,
                    "source_candidate": child_hash,
                },
            )
            observations = tuple(
                self._evaluate_records(
                    artifact_hash_value=artifact,
                    records=regression_records,
                    role_manifest=evolve_manifest,
                    dataset_path=dataset_path,
                    task_path=task_path,
                    phase=f"p2-slot-{slot:04d}-rfclm-{label}",
                    budget_scope="search",
                )
            )
            return artifact, observations

        baseline_length = None
        for length in range(len(full_lineage)):
            _, observations = evaluate_lineage(
                full_lineage[:length], f"prefix-{length:03d}"
            )
            if all(observation.resolved for observation in observations):
                baseline_length = length
                break
        if baseline_length is None:
            result = {
                "schema_version": SCHEMA_VERSION,
                "arm": "p2",
                "coverage_selection_mode": "agent_only",
                "same_repo": expected_repo,
                "probe_task_ids": probe_task_ids,
                "parent_artifact_hash": parent_hash,
                "proposed_artifact_hash": child_hash,
                "accepted": False,
                "artifact_hash": child_hash,
                "terminal_state": "RF_CLM_NO_PASSING_BASELINE_REJECTED",
                "pairs": gate_pairs,
                "regression_task_ids": regressions,
                "rf_clm": {
                    "method": "abstain",
                    "reason": (
                        "No lineage prefix resolves every selected regression task."
                    ),
                },
            }
            atomic_json(gate_path, result)
            return result

        baseline = full_lineage[:baseline_length]
        segment = full_lineage[baseline_length:]
        probe_records_log: list[dict[str, Any]] = []

        def fails_with_active(active_ids: tuple[str, ...]) -> bool:
            active = set(active_ids)
            retained_ids = {delta.mutation_id for delta in baseline}
            active_segment = []
            for delta in segment:
                if (
                    delta.mutation_id in active
                    and set(delta.depends_on) <= retained_ids
                ):
                    active_segment.append(delta)
                    retained_ids.add(delta.mutation_id)
            lineage = (*baseline, *active_segment)
            effective_active_ids = tuple(
                delta.mutation_id for delta in active_segment
            )
            probe_key = hash_json(
                {
                    "baseline": [delta.mutation_id for delta in baseline],
                    "requested_active": list(active_ids),
                    "effective_active": list(effective_active_ids),
                }
            )[:12]
            artifact, observations = evaluate_lineage(
                lineage, f"probe-{probe_key}"
            )
            failed = not all(observation.resolved for observation in observations)
            probe_records_log.append(
                {
                    "requested_active_mutation_ids": active_ids,
                    "effective_active_mutation_ids": effective_active_ids,
                    "artifact_hash": artifact,
                    "failed": failed,
                    "task_results": [
                        {
                            "instance_id": observation.instance_id,
                            "resolved": observation.resolved,
                            "observation_hash": observation.observation_hash,
                        }
                        for observation in observations
                    ],
                }
            )
            return failed

        newest_paths = set(segment[-1].changed_paths)
        dependency_prior = [
            mutation_id
            for mutation_id in segment[-1].depends_on
            if any(delta.mutation_id == mutation_id for delta in segment[:-1])
        ]
        overlap_prior = [
            delta.mutation_id
            for delta in segment[:-1]
            if newest_paths & set(delta.changed_paths)
        ]
        repair_prior = tuple(
            dict.fromkeys(
                [
                    *dependency_prior,
                    *overlap_prior,
                    *(delta.mutation_id for delta in reversed(segment)),
                ]
            )
        )
        repair = repair_first_lineage(
            segment,
            fails_with_active=fails_with_active,
            prior_order=repair_prior,
            singleton_budget=self.config.rf_clm_singleton_budget,
        )
        if repair.plan is None:
            result = {
                "schema_version": SCHEMA_VERSION,
                "arm": "p2",
                "coverage_selection_mode": "agent_only",
                "same_repo": expected_repo,
                "probe_task_ids": probe_task_ids,
                "parent_artifact_hash": parent_hash,
                "proposed_artifact_hash": child_hash,
                "accepted": False,
                "artifact_hash": child_hash,
                "terminal_state": "RF_CLM_ABSTAIN_REJECTED",
                "pairs": gate_pairs,
                "regression_task_ids": regressions,
                "rf_clm": {
                    "method": repair.method,
                    "reason": repair.abstain_reason,
                    "removed_mutation_ids": repair.removed_mutation_ids,
                    "probe_count": repair.probe_count,
                    "probes": probe_records_log,
                },
            }
            atomic_json(gate_path, result)
            return result

        repaired_lineage = apply_repair_plan(baseline, segment, repair.plan)
        repaired_hash = self._write_artifact(
            lineage=repaired_lineage,
            parent_hash=parent_hash,
            mutation_record={
                "kind": "RF-CLM repaired candidate",
                "slot": slot,
                "source_candidate": child_hash,
                "repair_plan": dataclasses.asdict(repair.plan),
            },
        )
        result = {
            "schema_version": SCHEMA_VERSION,
            "arm": "p2",
            "coverage_selection_mode": "agent_only",
            "same_repo": expected_repo,
            "probe_task_ids": probe_task_ids,
            "parent_artifact_hash": parent_hash,
            "proposed_artifact_hash": child_hash,
            "accepted": True,
            "artifact_hash": repaired_hash,
            "terminal_state": "RF_CLM_REPAIRED",
            "pairs": gate_pairs,
            "regression_task_ids": regressions,
            "rf_clm": {
                "method": repair.method,
                "removed_mutation_ids": repair.removed_mutation_ids,
                "probe_count": repair.probe_count,
                "plan": dataclasses.asdict(repair.plan),
                "probes": probe_records_log,
            },
        }
        atomic_json(gate_path, result)
        return result

    def run_endpoint(self) -> dict[str, Any]:
        seal = self._load_json(self.search_seal_path)
        endpoint_state_path = self._endpoint_state_path()
        endpoint_identity = hash_json(
            {
                "search_seal": seal,
                "config_hash": self.config.config_hash,
                "source_manifest_sha256": FULL_MANIFEST_SHA256,
            }
        )
        if endpoint_state_path.exists():
            endpoint_state = self._load_json(endpoint_state_path)
            if endpoint_state.get("identity_hash") != endpoint_identity:
                raise ConfigurationError("Endpoint identity differs from frozen state")
            if endpoint_state.get("status") == "complete":
                return self._load_json(self.output_root / "endpoint-summary.json")
            if endpoint_state.get("status") == "invalid":
                raise ObservationInvalid(
                    f"Endpoint is terminally invalid: {endpoint_state.get('reason')}"
                )
        else:
            endpoint_state = {
                "schema_version": SCHEMA_VERSION,
                "identity_hash": endpoint_identity,
                "status": "running",
                "started_at": utc_timestamp(),
            }
            atomic_json(endpoint_state_path, endpoint_state)
            self.events.append("endpoint_started", endpoint_state)

        full_manifest, manifest_hash = load_manifest(self.paths.full_manifest)
        _, test_manifest, split_binding = build_split_contract(
            full_manifest, manifest_hash
        )
        validate_test_manifest(test_manifest, split_binding)
        endpoint_inputs = self.output_root / "endpoints" / "frozen-inputs"
        test_manifest_hash = freeze_file_once(
            endpoint_inputs / "test-140-manifest.json", test_manifest
        )
        commitment = self._load_json(
            self.frozen_inputs / "test-140-commitment.json"
        )
        if commitment["role_manifest_hash"] != hash_json(test_manifest):
            raise ConfigurationError("Post-seal test manifest breaks commitment")
        dataset_path, task_path = materialize_inputs(
            test_manifest, endpoint_inputs / "materialized"
        )
        records = test_manifest["records"]
        if self.config.smoke:
            records = records[: self.config.smoke_endpoint_tasks]
        p0_hash = self._load_json(self.output_root / "protocol-lock.json")[
            "p0_artifact_hash"
        ]
        final_hash = seal["final_artifact_hash"]
        artifacts = [p0_hash] if final_hash == p0_hash else [p0_hash, final_hash]
        schedule = [
            (entry, artifact)
            for entry in records
            for artifact in endpoint_order(
                artifacts,
                entry["record"]["instance_id"],
                self.config.experiment_seed,
            )
        ]
        for entry, artifact in self.progress_factory(
            schedule, "D_test endpoint", len(schedule)
        ):
            label = "p0" if artifact == p0_hash else "final"
            scope = f"endpoint:{label}"
            token_cap = (
                self.config.reference_endpoint_token_cap
                if label == "p0"
                else self.config.final_endpoint_token_cap
            )
            if self._phase_exhausted(
                scope,
                token_cap,
                self.config.endpoint_active_seconds_cap,
                minimum_tokens=self.config.per_task_token_cap,
            ):
                endpoint_state["status"] = "invalid"
                endpoint_state["reason"] = f"{scope} budget exhausted"
                atomic_json(endpoint_state_path, endpoint_state)
                self.events.append("endpoint_invalid", endpoint_state)
                raise BudgetExhausted(endpoint_state["reason"])
            observation = self._evaluate_task(
                artifact_hash_value=artifact,
                entry=entry,
                role_manifest=test_manifest,
                dataset_path=dataset_path,
                task_path=task_path,
                phase=f"endpoint-{label}",
                budget_scope=scope,
            )
            if not observation.valid:
                endpoint_state["status"] = "invalid"
                endpoint_state["reason"] = (
                    f"Invalid endpoint observation: {observation.instance_id}"
                )
                atomic_json(endpoint_state_path, endpoint_state)
                self.events.append("endpoint_invalid", endpoint_state)
                raise ObservationInvalid(endpoint_state["reason"])
            self._record_pacing_delay(
                budget_scope=scope,
                phase=f"endpoint-{label}",
                artifact_hash_value=artifact,
                instance_id=observation.instance_id,
            )

        summary = self._endpoint_summary(
            records=records,
            p0_hash=p0_hash,
            final_hash=final_hash,
            test_manifest_hash=test_manifest_hash,
        )
        atomic_json(self.output_root / "endpoint-summary.json", summary)
        self._write_markdown_report(summary)
        endpoint_state["status"] = "complete"
        endpoint_state["completed_at"] = utc_timestamp()
        endpoint_state["summary_hash"] = hash_json(summary)
        atomic_json(endpoint_state_path, endpoint_state)
        self.events.append("endpoint_complete", endpoint_state)
        return summary

    def _mutate(
        self,
        parent_hash: str,
        slot: int,
        evolve_manifest: Mapping[str, Any],
        task_path: Path,
    ) -> dict[str, Any]:
        slot_dir = self.output_root / "search" / "slots" / f"{slot:04d}"
        raw_result_path = slot_dir / "mutation-result.json"
        final_result_path = slot_dir / "mutation-final.json"
        invocation_path = slot_dir / "mutation-invocation.json"
        evidence_path = slot_dir / "mutation-evidence.json"
        if final_result_path.exists():
            final_result = self._load_json(final_result_path)
            if final_result.get("parentArtifactHash") != parent_hash:
                raise ConfigurationError("Mutation final parent identity mismatch")
            cost_source = (
                self._load_json(raw_result_path)
                if raw_result_path.exists()
                else final_result
            )
            self._ensure_mutation_ledger(slot, cost_source)
            return final_result

        if evidence_path.exists():
            evidence = self._load_json(evidence_path)
            if (
                evidence.get("slot") != slot
                or evidence.get("parent_artifact_hash") != parent_hash
            ):
                raise ConfigurationError("Mutation evidence identity mismatch")
        else:
            parent_content = self._artifact_content(parent_hash)
            parent_lineage = self._artifact_lineage(parent_hash)
            observations = self._artifact_observations(
                parent_hash, phase_prefix="search"
            )
            task_by_id = {
                task["instance_id"]: task for task in self._load_json(task_path)
            }
            unresolved_ids = [
                observation.instance_id
                for observation in observations
                if not observation.resolved
                and observation.instance_id in task_by_id
            ]
            unresolved_ids.sort(
                key=lambda instance_id: hashlib.sha256(
                    f"mutation-evidence|{self.config.experiment_seed}|{slot}|"
                    f"{instance_id}".encode()
                ).hexdigest()
            )
            if not unresolved_ids:
                final_result = {
                    "schemaVersion": SCHEMA_VERSION,
                    "parentArtifactHash": parent_hash,
                    "valid": False,
                    "error": "Parent has no failed D_evolve entry task to anchor mutation.",
                    "inputTokens": 0,
                    "outputTokens": 0,
                    "cacheReadTokens": 0,
                    "cacheWriteTokens": 0,
                    "tokenTelemetryAvailable": True,
                }
                atomic_json(final_result_path, final_result)
                self._ensure_mutation_ledger(slot, final_result)
                return final_result
            entry_task = task_by_id[unresolved_ids[0]]
            same_repo_candidates = [
                {
                    "instance_id": task["instance_id"],
                    "repo": task["repo"],
                    "problem_statement": task["problem_statement"][:2_000],
                }
                for task in task_by_id.values()
                if task["repo"] == entry_task["repo"]
            ]
            evidence = {
                "schema_version": SCHEMA_VERSION,
                "slot": slot,
                "parent_artifact_hash": parent_hash,
                "parent_strategy": parent_content.strategy,
                "parent_tools": parent_content.tools_manifest,
                "parent_lineage": [
                    mutation_delta_to_json(delta) for delta in parent_lineage
                ],
                "parent_score": (
                    sum(observation.resolved for observation in observations)
                    / len(observations)
                    if observations
                    else None
                ),
                "resolved_count": sum(
                    observation.resolved for observation in observations
                ),
                "evaluated_count": len(observations),
                "entry_task": {
                    "instance_id": entry_task["instance_id"],
                    "repo": entry_task["repo"],
                    "problem_statement": entry_task["problem_statement"][:4_000],
                },
                "same_repo_probe_candidates": same_repo_candidates,
                "constraints": {
                    "mutable_surface": [
                        "strategy.md",
                        "tools.json",
                        "handlers/*.py",
                    ],
                    "entry_task_repo": entry_task["repo"],
                    "coverage_selection_mode": "agent_only",
                    "probe_task_limit": self.config.adaptive_task_budget,
                    "same_repo_probe_only": True,
                    "general_only": True,
                    "forbid_task_ids": True,
                    "forbid_benchmark_specific_instructions": True,
                },
            }
            atomic_json(evidence_path, evidence)

        mutation_identity = {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.config.run_id,
            "config_hash": self.config.config_hash,
            "slot": slot,
            "parent_artifact_hash": parent_hash,
            "evidence_hash": hash_json(evidence),
            "model_provider": self.config.model_provider,
            "model_id": self.config.model_id,
            "mutation_runner_sha256": sha256_file(self.paths.mutation_runner),
            "max_output_tokens": self.config.mutation_output_token_cap,
            "max_total_tokens": self.config.mutation_token_cap,
        }
        mutation_identity_hash = hash_json(mutation_identity)
        if raw_result_path.exists():
            if not invocation_path.exists():
                raise ConfigurationError("Mutation result lacks invocation identity")
            invocation = self._load_json(invocation_path)
            if invocation.get("identity_hash") != mutation_identity_hash:
                raise ConfigurationError("Mutation invocation identity mismatch")
            result = self._load_json(raw_result_path)
            if result.get("parentArtifactHash") != parent_hash:
                raise ConfigurationError("Mutation result parent identity mismatch")
            raw_sha256 = sha256_file(raw_result_path)
            if (
                invocation.get("result_sha256")
                and invocation["result_sha256"] != raw_sha256
            ):
                raise ConfigurationError("Mutation result hash mismatch")
            invocation["status"] = "result_persisted"
            invocation["result_sha256"] = raw_sha256
            atomic_json(invocation_path, invocation)
        else:
            if invocation_path.exists():
                invocation = self._load_json(invocation_path)
                final_result = {
                    "schemaVersion": SCHEMA_VERSION,
                    "parentArtifactHash": parent_hash,
                    "valid": False,
                    "error": (
                        "Mutation invocation is ambiguous after interruption; "
                        "refusing a second model sample."
                    ),
                    "inputTokens": 0,
                    "outputTokens": 0,
                    "cacheReadTokens": 0,
                    "cacheWriteTokens": 0,
                    "tokenTelemetryAvailable": False,
                    "invocationStatus": invocation.get("status"),
                }
                atomic_json(final_result_path, final_result)
                self._ensure_mutation_ledger(slot, final_result)
                return final_result
            if self.config.search_token_cap is not None:
                remaining = self.config.search_token_cap - int(
                    self.ledger.totals("search")["budget_counted_tokens"]
                )
                if remaining < self.config.mutation_token_cap:
                    raise BudgetExhausted("Insufficient search reserve for mutation")
            invocation = {
                "schema_version": SCHEMA_VERSION,
                "identity_hash": mutation_identity_hash,
                "status": "model_call_started",
                "started_at": utc_timestamp(),
            }
            atomic_json(invocation_path, invocation)
            command = [
                self.paths.node,
                str(self.paths.mutation_runner),
                "--agent-dir",
                str(self.paths.agent_dir),
                "--evidence-file",
                str(evidence_path),
                "--model-provider",
                self.config.model_provider,
                "--model-id",
                self.config.model_id,
                "--output",
                str(raw_result_path),
                "--trace",
                str(slot_dir / "mutation-trace.jsonl"),
                "--max-output-tokens",
                str(self.config.mutation_output_token_cap),
                "--max-total-tokens",
                str(self.config.mutation_token_cap),
                "--timeout-seconds",
                str(self.config.mutation_timeout_seconds),
            ]
            return_code = run_logged(
                command,
                slot_dir / "mutation-runner.log",
                cwd=self.paths.repo_root,
                environment=command_environment(self.paths.docker_host),
                timeout=self.config.mutation_timeout_seconds + 120,
            )
            if not raw_result_path.exists():
                final_result = {
                    "schemaVersion": SCHEMA_VERSION,
                    "parentArtifactHash": parent_hash,
                    "valid": False,
                    "error": (
                        "Mutation invocation has no durable result; refusing "
                        f"retry (exit {return_code})."
                    ),
                    "inputTokens": 0,
                    "outputTokens": 0,
                    "cacheReadTokens": 0,
                    "cacheWriteTokens": 0,
                    "tokenTelemetryAvailable": False,
                }
                atomic_json(final_result_path, final_result)
                self._ensure_mutation_ledger(slot, final_result)
                return final_result
            result = self._load_json(raw_result_path)
            if result.get("parentArtifactHash") != parent_hash:
                raise ConfigurationError("Mutation result parent identity mismatch")
            invocation["status"] = "result_persisted"
            invocation["return_code"] = return_code
            invocation["result_sha256"] = sha256_file(raw_result_path)
            atomic_json(invocation_path, invocation)

        self._ensure_mutation_ledger(slot, result)
        if not result.get("valid"):
            atomic_json(final_result_path, result)
            return self._load_json(final_result_path)
        try:
            mutation_model_result_hash = hash_json(result)
            evolve_ids = [
                entry["record"]["instance_id"]
                for entry in evolve_manifest["records"]
            ]
            entry_task = evidence["entry_task"]
            task_by_id = {
                entry["record"]["instance_id"]: entry["record"]
                for entry in evolve_manifest["records"]
            }
            probe_task_ids = tuple(result["probeTaskIds"])
            if not probe_task_ids or entry_task["instance_id"] not in probe_task_ids:
                raise ConfigurationError(
                    "Agent-only probe selection must include the failed entry task"
                )
            if len(probe_task_ids) > self.config.adaptive_task_budget:
                raise ConfigurationError("Adaptive probe selection exceeds task budget")
            for instance_id in probe_task_ids:
                task = task_by_id.get(instance_id)
                if task is None:
                    raise ConfigurationError(
                        f"Adaptive probe is outside D_evolve: {instance_id}"
                    )
                if task["repo"] != entry_task["repo"]:
                    raise ConfigurationError(
                        f"Adaptive probe crosses repositories: {instance_id}"
                    )
            mutation_id = (
                f"m-{slot:04d}-"
                f"{hash_json({'parent': parent_hash, 'result': result})[:12]}"
            )
            delta = MutationDelta(
                mutation_id=mutation_id,
                repo=entry_task["repo"],
                entry_task_id=entry_task["instance_id"],
                mutation_summary=result["mutationSummary"],
                strategy_patch=result["strategyPatch"],
                tool=(
                    None
                    if result["tool"] is None
                    else CandidateTool(
                        name=result["tool"]["name"],
                        label=result["tool"]["label"],
                        description=result["tool"]["description"],
                        parameters=result["tool"]["parameters"],
                        handler_code=result["tool"]["handler_code"],
                        timeout_seconds=result["tool"]["timeout_seconds"],
                    )
                ),
                depends_on=tuple(result["dependsOn"]),
            )
            validate_mutation_delta(delta, evolve_ids)
            lineage = (*self._artifact_lineage(parent_hash), delta)
            child_hash = self._write_artifact(
                lineage=lineage,
                parent_hash=parent_hash,
                mutation_record={
                    "kind": "Pi strategy/tool mutation",
                    "slot": slot,
                    "summary": result.get("mutationSummary", ""),
                    "entry_task_id": entry_task["instance_id"],
                    "repo": entry_task["repo"],
                    "probe_task_ids": probe_task_ids,
                    "mutation_delta": mutation_delta_to_json(delta),
                    "mutation_model_result_hash": mutation_model_result_hash,
                },
            )
        except (
            ArtifactValidationError,
            KeyError,
            TypeError,
            ConfigurationError,
        ) as error:
            final_result = {
                **result,
                "valid": False,
                "error": str(error),
            }
            atomic_json(final_result_path, final_result)
            return final_result
        final_result = {
            **result,
            "artifact_hash": child_hash,
            "mutation_id": mutation_id,
            "repo": entry_task["repo"],
            "entry_task_id": entry_task["instance_id"],
            "probe_task_ids": probe_task_ids,
        }
        atomic_json(final_result_path, final_result)
        return final_result

    def _ensure_mutation_ledger(
        self,
        slot: int,
        result: Mapping[str, Any],
    ) -> None:
        charge_id = f"mutation:{slot:04d}"
        if charge_id in self.ledger.charge_ids:
            return
        reported = total_reported_tokens(dict(result))
        telemetry_complete = result.get("tokenTelemetryAvailable") is True
        self.ledger.append(
            charge_id,
            {
                "budget_scope": "search",
                "kind": "mutation_proposer",
                "slot": slot,
                "reported_tokens": reported,
                "conservative_token_charge": (
                    0
                    if telemetry_complete
                    else max(0, self.config.mutation_token_cap - reported)
                ),
                "active_seconds": float(result.get("durationMs", 0)) / 1000,
                "api_calls": 1,
                "task_executions": 0,
                "status": "valid" if result.get("valid") else "invalid",
            },
        )

    def _import_p0(self, source_root: Path) -> dict[str, Any]:
        source_root = source_root.resolve()
        if source_root == self.output_root:
            raise ConfigurationError("P0 import source cannot be the target run")
        if self.p0_import_completion_path.exists():
            contract = self._load_json(self.p0_import_contract_path)
            if contract.get("source", {}).get("run_root") != str(source_root):
                raise ConfigurationError(
                    "Completed P0 import is bound to a different source run"
                )
            completion = self._validate_completed_p0_import()
            self._ensure_p0_import_event(contract, completion)
            return completion
        forbidden = (
            self.search_state_path,
            self.search_seal_path,
            self.output_root / "search-invalid.json",
            self.output_root / "search",
            self._endpoint_state_path(),
            self.output_root / "endpoints",
        )
        if any(path.exists() for path in forbidden):
            raise ConfigurationError("P0 import is allowed only before search starts")
        if (
            not self.p0_import_contract_path.exists()
            and (
                self.archive_path.exists()
                or (self.output_root / "observations" / "search-p0").exists()
                or bool(self.ledger.records)
            )
        ):
            raise ConfigurationError(
                "P0 import requires an otherwise pristine prepared target"
            )

        contract, copies, archive_entry, source_ledger_records = (
            self._validate_p0_import_source(source_root)
        )
        freeze_file_once(self.p0_import_contract_path, contract)
        p0_hash = contract["panel"]["p0_artifact_hash"]
        target_panel_root = (
            self.output_root / "observations" / "search-p0" / p0_hash
        )
        for source_path, relative_path, expected_sha256 in copies:
            target_path = target_panel_root / relative_path
            if target_path.exists():
                if (
                    not target_path.is_file()
                    or target_path.is_symlink()
                    or sha256_file(target_path) != expected_sha256
                ):
                    raise ConfigurationError(
                        f"Imported P0 evidence differs from contract: {target_path}"
                    )
                continue
            atomic_write(target_path, source_path.read_bytes())
            if sha256_file(target_path) != expected_sha256:
                raise ConfigurationError(
                    f"Imported P0 evidence copy failed verification: {target_path}"
                )

        source_binding = contract["source"]
        imported_ledger = []
        source_prefix = source_binding["protocol_lock_sha256"][:16]
        for source_record in source_ledger_records:
            source_charge_id = source_record["charge_id"]
            target_charge_id = (
                f"p0-import:{source_prefix}:{source_charge_id}"
            )
            payload = {
                **source_record["payload"],
                "imported_from": {
                    "run_id": source_binding["run_id"],
                    "source_charge_id": source_charge_id,
                    "source_entry_hash": source_record["entry_hash"],
                    "source_protocol_lock_sha256": source_binding[
                        "protocol_lock_sha256"
                    ],
                },
            }
            target_record = self.ledger.append(target_charge_id, payload)
            imported_ledger.append(
                {
                    "source_charge_id": source_charge_id,
                    "source_entry_hash": source_record["entry_hash"],
                    "target_charge_id": target_charge_id,
                    "target_entry_hash": target_record["entry_hash"],
                }
            )

        if self.archive_path.exists():
            if self._load_archive() != [archive_entry]:
                raise ConfigurationError(
                    "Target archive differs from imported P0 contract"
                )
        else:
            self._write_archive([archive_entry])
        completion_payload = {
            "schema_version": SCHEMA_VERSION,
            "protocol_revision": PROTOCOL_REVISION,
            "completed_at": utc_timestamp(),
            "contract_hash": contract["contract_hash"],
            "p0_artifact_hash": p0_hash,
            "panel_hash": contract["panel"]["panel_hash"],
            "archive_hash": hash_json([dataclasses.asdict(archive_entry)]),
            "imported_ledger": imported_ledger,
            "imported_ledger_hash": hash_json(imported_ledger),
        }
        completion = {
            **completion_payload,
            "completion_hash": hash_json(completion_payload),
        }
        freeze_file_once(self.p0_import_completion_path, completion)
        self._validate_completed_p0_import()
        self._ensure_p0_import_event(contract, completion)
        return completion

    def _validate_p0_import_source(
        self,
        source_root: Path,
    ) -> tuple[
        dict[str, Any],
        list[tuple[Path, str, str]],
        ArchiveEntry,
        list[dict[str, Any]],
    ]:
        required_source_paths = (
            source_root / "protocol-lock.json",
            source_root / "search-invalid.json",
            source_root / "archive.json",
            source_root / "global-cost-ledger.jsonl",
            source_root / "frozen-inputs" / "experiment-config.json",
            source_root / "frozen-inputs" / "execution-stack.json",
            source_root / "frozen-inputs" / "evolve-60-manifest.json",
        )
        if any(not path.is_file() for path in required_source_paths):
            raise ConfigurationError(
                "P0 import source lacks required protocol or evidence files"
            )
        forbidden_source_paths = (
            source_root / "search-seal.json",
            source_root / "endpoint-consumption.json",
            source_root / "frozen-inputs" / "test-140-manifest.json",
            source_root
            / "endpoints"
            / "frozen-inputs"
            / "test-140-manifest.json",
        )
        if any(path.exists() for path in forbidden_source_paths):
            raise ConfigurationError(
                "P0 import source has search-seal or D_test consumption state"
            )

        source_invalid = self._load_json(source_root / "search-invalid.json")
        self._require_self_hash(
            source_invalid,
            hash_field="record_hash",
            label="source search-invalid",
        )
        if (
            source_invalid.get("terminal_state")
            != "SEARCH_INFRASTRUCTURE_INVALID"
            or source_invalid.get("classification") != "infrastructure_invalid"
            or source_invalid.get("p0_reusable") is not True
            or source_invalid.get("search_mutations_reusable") is not False
        ):
            raise ConfigurationError(
                "P0 import source is not terminally infrastructure-invalid"
            )
        events_path = source_root / "state" / "events"
        if not events_path.is_dir():
            raise ConfigurationError("P0 import source lacks an event chain")
        source_events = AppendOnlyState(source_root / "state").events
        if not any(
            event.event_type == "search_invalid"
            and event.payload.get("record_hash") == source_invalid["record_hash"]
            for event in source_events
        ):
            raise ConfigurationError(
                "Source search-invalid record is absent from the event chain"
            )

        source_protocol_path = source_root / "protocol-lock.json"
        source_protocol = self._load_json(source_protocol_path)
        source_config_path = (
            source_root / "frozen-inputs" / "experiment-config.json"
        )
        source_config_payload = self._load_json(source_config_path)
        source_config = source_config_payload.get("config")
        if (
            not isinstance(source_config, dict)
            or hash_json(source_config) != source_config_payload.get("config_hash")
            or source_protocol.get("config_hash")
            != source_config_payload.get("config_hash")
            or source_protocol.get("run_id") != source_config.get("run_id")
        ):
            raise ConfigurationError("Source experiment config binding is invalid")
        target_protocol = self._load_json(self.output_root / "protocol-lock.json")
        target_config_payload = self._load_json(
            self.frozen_inputs / "experiment-config.json"
        )
        target_config = target_config_payload["config"]

        source_evolve_path = (
            source_root / "frozen-inputs" / "evolve-60-manifest.json"
        )
        source_evolve = self._load_json(source_evolve_path)
        target_evolve = self._load_json(
            self.frozen_inputs / "evolve-60-manifest.json"
        )
        validate_evolve_manifest(source_evolve)
        validate_evolve_manifest(target_evolve)
        if source_evolve != target_evolve:
            raise ConfigurationError(
                "Source and target D_evolve manifests are not identical"
            )
        source_execution_path = (
            source_root / "frozen-inputs" / "execution-stack.json"
        )
        source_execution = self._load_json(source_execution_path)
        target_execution = self._load_json(
            self.frozen_inputs / "execution-stack.json"
        )
        if (
            hash_json(source_execution)
            != source_protocol.get("execution_stack_hash")
            or hash_json(target_execution)
            != target_protocol.get("execution_stack_hash")
            or source_execution != target_execution
        ):
            raise ConfigurationError(
                "Source and target task execution stacks are not identical"
            )
        source_p0 = source_protocol.get("p0_artifact_hash")
        target_p0 = target_protocol.get("p0_artifact_hash")
        if not isinstance(source_p0, str) or source_p0 != target_p0:
            raise ConfigurationError(
                "Source and target P0 artifacts are not identical"
            )
        source_task_contract = self._p0_task_execution_contract(
            source_config,
            source_execution,
            source_evolve,
            source_p0,
        )
        target_task_contract = self._p0_task_execution_contract(
            target_config,
            target_execution,
            target_evolve,
            target_p0,
        )
        if source_task_contract != target_task_contract:
            raise ConfigurationError(
                "Source and target P0 task execution contracts differ"
            )
        self._validate_source_p0_artifact(source_root, source_p0)
        self._artifact_content(target_p0)

        source_archive_path = source_root / "archive.json"
        source_archive = self._load_json(source_archive_path)
        source_archive_entries = [
            ArchiveEntry(
                **{
                    **entry,
                    "functioning_child_slots": tuple(
                        entry.get("functioning_child_slots", ())
                    ),
                }
            )
            for entry in source_archive.get("entries", ())
        ]
        if source_archive.get("archive_hash") != hash_json(
            [dataclasses.asdict(entry) for entry in source_archive_entries]
        ):
            raise ConfigurationError("Source archive hash mismatch")
        if len(source_archive_entries) != 1:
            raise ConfigurationError(
                "P0 import source archive must contain only P0"
            )
        archive_entry = source_archive_entries[0]
        if (
            archive_entry.artifact_hash != source_p0
            or archive_entry.parent_artifact_hash is not None
            or archive_entry.evaluated_tasks != 60
            or archive_entry.functioning_child_count != 0
            or archive_entry.functioning_child_slots
            or archive_entry.insertion_ordinal != 0
        ):
            raise ConfigurationError("Source P0 archive entry is invalid")

        ordered_ids = [
            entry["record"]["instance_id"]
            for entry in source_evolve["records"]
        ]
        source_panel_root = (
            source_root / "observations" / "search-p0" / source_p0
        )
        if not source_panel_root.is_dir() or source_panel_root.is_symlink():
            raise ConfigurationError("Source P0 observation panel is missing")
        actual_ids = sorted(
            path.name
            for path in source_panel_root.iterdir()
            if path.is_dir() and not path.is_symlink()
        )
        if actual_ids != sorted(ordered_ids):
            raise ConfigurationError(
                "Source P0 observation panel does not contain exact D_evolve IDs"
            )

        source_role_hash = hash_json(source_evolve)
        source_execution_hash = hash_json(source_execution)
        observation_records = []
        copies: list[tuple[Path, str, str]] = []
        observations_by_identity: dict[str, TaskObservation] = {}
        for entry in source_evolve["records"]:
            row = entry["record"]
            instance_id = row["instance_id"]
            task_dir = source_panel_root / instance_id
            required = {
                "identity.json": task_dir / "identity.json",
                "invocation.json": task_dir / "invocation.json",
                "result.json": task_dir / "result.json",
                "observation.json": task_dir / "observation.json",
            }
            if any(
                not path.is_file() or path.is_symlink()
                for path in required.values()
            ):
                raise ConfigurationError(
                    f"Source P0 evidence is incomplete: {instance_id}"
                )
            identity = self._load_json(required["identity.json"])
            expected_identity = {
                "schema_version": SCHEMA_VERSION,
                "run_id": source_protocol["run_id"],
                "config_hash": source_protocol["config_hash"],
                "artifact_hash": source_p0,
                "instance_id": instance_id,
                "repo": row["repo"],
                "base_commit": row["base_commit"],
                "phase": "search-p0",
                "budget_scope": "search",
                "role_manifest_hash": source_role_hash,
                "model_provider": source_config["model_provider"],
                "model_id": source_config["model_id"],
                "execution_stack_hash": source_execution_hash,
                "artifact_content_hash": source_p0,
                "per_task_output_token_cap": source_config[
                    "per_task_output_token_cap"
                ],
                "per_task_token_cap": source_config["per_task_token_cap"],
                "agent_timeout_seconds": source_config[
                    "agent_timeout_seconds"
                ],
                "evaluator_timeout_seconds": source_config[
                    "evaluator_timeout_seconds"
                ],
                "rollout": 0,
            }
            for name, expected in expected_identity.items():
                if identity.get(name) != expected:
                    raise ConfigurationError(
                        f"Source P0 identity mismatch for {instance_id}: {name}"
                    )
            if (
                not isinstance(identity.get("image"), str)
                or not identity["image"]
                or not isinstance(identity.get("image_digest"), str)
                or not identity["image_digest"]
            ):
                raise ConfigurationError(
                    f"Source P0 image identity is incomplete: {instance_id}"
                )
            identity_hash = hash_json(identity)
            raw_observation = self._load_json(required["observation.json"])
            observation = self._task_observation_from_record(
                raw_observation,
                required["observation.json"],
            )
            if (
                observation.identity_hash != identity_hash
                or observation.instance_id != instance_id
                or observation.artifact_hash != source_p0
                or observation.phase != "search-p0"
                or not observation.valid
            ):
                raise ConfigurationError(
                    f"Source P0 observation binding is invalid: {instance_id}"
                )
            result = self._load_json(required["result.json"])
            invocation = self._load_json(required["invocation.json"])
            if (
                invocation.get("identity_hash") != identity_hash
                or invocation.get("result_sha256")
                != sha256_file(required["result.json"])
            ):
                raise ConfigurationError(
                    f"Source P0 invocation binding is invalid: {instance_id}"
                )
            return_code = result.get("runnerExitCode")
            if isinstance(return_code, bool) or not isinstance(return_code, int):
                raise ConfigurationError(
                    f"Source P0 runner exit code is invalid: {instance_id}"
                )
            classification = classify_runner_result(result, return_code)
            if (
                not classification.valid
                or observation.token_telemetry_complete
                != classification.telemetry_complete
                or observation.reported_tokens
                != total_reported_tokens(result)
                or observation.patch_sha256
                != sha256_bytes(str(result.get("patch") or "").encode())
            ):
                raise ConfigurationError(
                    f"Source P0 result disagrees with observation: {instance_id}"
                )
            optional_paths = {}
            evaluator_invocation = task_dir / "evaluator-invocation.json"
            if evaluator_invocation.exists():
                optional_paths["evaluator-invocation.json"] = evaluator_invocation
            if classification.should_grade_patch:
                evaluation_protocol = f"search-p0-{source_p0[:12]}"
                evaluation_path = (
                    task_dir / evaluation_protocol / "evaluation.json"
                )
                if (
                    not evaluator_invocation.is_file()
                    or evaluator_invocation.is_symlink()
                    or not evaluation_path.is_file()
                    or evaluation_path.is_symlink()
                ):
                    raise ConfigurationError(
                        f"Source P0 evaluator evidence is incomplete: {instance_id}"
                    )
                evaluation = self._load_json(evaluation_path)
                if (
                    evaluation.get("status") != "completed"
                    or bool(evaluation.get("resolved"))
                    != observation.resolved
                    or evaluation.get("submittedPatchSha256")
                    != observation.patch_sha256
                    or observation.status != "completed"
                ):
                    raise ConfigurationError(
                        f"Source P0 evaluator disagrees with observation: {instance_id}"
                    )
                optional_paths[
                    f"{evaluation_protocol}/evaluation.json"
                ] = evaluation_path
                prediction_path = (
                    task_dir / evaluation_protocol / "prediction.json"
                )
                if prediction_path.is_file() and not prediction_path.is_symlink():
                    optional_paths[
                        f"{evaluation_protocol}/prediction.json"
                    ] = prediction_path
            elif (
                observation.resolved
                or observation.status != classification.status
            ):
                raise ConfigurationError(
                    f"Source P0 observed-zero outcome is invalid: {instance_id}"
                )

            evidence_files = {}
            for relative_path, path in {**required, **optional_paths}.items():
                if not path.is_file() or path.is_symlink():
                    raise ConfigurationError(
                        f"Unsafe source P0 evidence path: {path}"
                    )
                digest = sha256_file(path)
                panel_relative = f"{instance_id}/{relative_path}"
                evidence_files[relative_path] = digest
                copies.append((path, panel_relative, digest))
            evidence_hash = hash_json(evidence_files)
            observation_records.append(
                {
                    "instance_id": instance_id,
                    "identity_hash": identity_hash,
                    "observation_hash": observation.observation_hash,
                    "resolved": observation.resolved,
                    "evidence_files": evidence_files,
                    "evidence_hash": evidence_hash,
                }
            )
            observations_by_identity[identity_hash] = observation

        resolved = sum(
            int(record["resolved"]) for record in observation_records
        )
        if (
            archive_entry.resolved_60 != resolved
            or archive_entry.score_60 != resolved / 60
        ):
            raise ConfigurationError(
                "Source archive score disagrees with P0 observations"
            )

        source_ledger = CostLedger(
            source_root / "global-cost-ledger.jsonl"
        )
        ledger_by_charge = {
            record["charge_id"]: record for record in source_ledger.records
        }
        selected_charge_ids = set()
        for identity_hash, observation in observations_by_identity.items():
            charge_id = f"task:{identity_hash}"
            record = ledger_by_charge.get(charge_id)
            if record is None:
                raise ConfigurationError(
                    f"Source P0 ledger lacks task charge: {observation.instance_id}"
                )
            payload = record["payload"]
            if (
                payload.get("budget_scope") != "search"
                or payload.get("kind") != "task_agent_and_evaluator"
                or payload.get("artifact_hash") != source_p0
                or payload.get("instance_id") != observation.instance_id
                or payload.get("phase") != "search-p0"
                or payload.get("reported_tokens")
                != observation.reported_tokens
                or payload.get("valid") is not True
                or bool(payload.get("resolved")) != observation.resolved
                or payload.get("task_executions") != 1
                or payload.get("api_calls") != 1
            ):
                raise ConfigurationError(
                    f"Source P0 task ledger binding is invalid: "
                    f"{observation.instance_id}"
                )
            selected_charge_ids.add(charge_id)
            if float(source_config["inter_task_delay_seconds"]) > 0:
                delay_id = (
                    f"delay:search:search-p0:{source_p0}:"
                    f"{observation.instance_id}"
                )
                delay = ledger_by_charge.get(delay_id)
                if (
                    delay is None
                    or delay["payload"].get("kind") != "request_pacing"
                    or delay["payload"].get("budget_scope") != "search"
                    or delay["payload"].get("api_calls") != 0
                    or delay["payload"].get("task_executions") != 0
                ):
                    raise ConfigurationError(
                        f"Source P0 pacing ledger is invalid: "
                        f"{observation.instance_id}"
                    )
                selected_charge_ids.add(delay_id)
        source_ledger_records = [
            record
            for record in source_ledger.records
            if record["charge_id"] in selected_charge_ids
        ]
        expected_ledger_records = 60 * (
            2 if float(source_config["inter_task_delay_seconds"]) > 0 else 1
        )
        if len(source_ledger_records) != expected_ledger_records:
            raise ConfigurationError("Source P0 ledger selection is incomplete")
        ledger_summary = {
            "records": len(source_ledger_records),
            "reported_tokens": sum(
                int(record["payload"].get("reported_tokens", 0))
                for record in source_ledger_records
            ),
            "conservative_token_charge": sum(
                int(
                    record["payload"].get(
                        "conservative_token_charge",
                        0,
                    )
                )
                for record in source_ledger_records
            ),
            "active_seconds": round(
                sum(
                    float(record["payload"].get("active_seconds", 0))
                    for record in source_ledger_records
                ),
                3,
            ),
            "api_calls": sum(
                int(record["payload"].get("api_calls", 0))
                for record in source_ledger_records
            ),
            "task_executions": sum(
                int(record["payload"].get("task_executions", 0))
                for record in source_ledger_records
            ),
        }
        ledger_bindings = [
            {
                "charge_id": record["charge_id"],
                "entry_hash": record["entry_hash"],
                "payload_hash": hash_json(record["payload"]),
            }
            for record in source_ledger_records
        ]
        panel_payload = {
            "p0_artifact_hash": source_p0,
            "task_count": 60,
            "ordered_instance_ids": ordered_ids,
            "ordered_instance_ids_sha256": sha256_ids(ordered_ids),
            "resolved": resolved,
            "observations": observation_records,
            "observations_hash": hash_json(observation_records),
        }
        panel = {
            **panel_payload,
            "panel_hash": hash_json(panel_payload),
        }
        source_binding = {
            "run_root": str(source_root),
            "run_id": source_protocol["run_id"],
            "config_hash": source_protocol["config_hash"],
            "protocol_lock_sha256": sha256_file(source_protocol_path),
            "experiment_config_sha256": sha256_file(source_config_path),
            "execution_stack_sha256": sha256_file(source_execution_path),
            "evolve_manifest_sha256": sha256_file(source_evolve_path),
            "archive_sha256": sha256_file(source_archive_path),
            "archive_hash": source_archive["archive_hash"],
            "search_invalid_sha256": sha256_file(
                source_root / "search-invalid.json"
            ),
            "search_invalid_record_hash": source_invalid["record_hash"],
            "final_event_hash": source_events[-1].event_hash,
        }
        target_binding = {
            "run_root": str(self.output_root),
            "run_id": target_protocol["run_id"],
            "config_hash": target_protocol["config_hash"],
            "protocol_lock_sha256": sha256_file(
                self.output_root / "protocol-lock.json"
            ),
            "task_execution_contract": target_task_contract,
            "task_execution_contract_hash": hash_json(
                target_task_contract
            ),
        }
        contract_payload = {
            "schema_version": SCHEMA_VERSION,
            "protocol_revision": PROTOCOL_REVISION,
            "kind": "audited_p0_import",
            "source": source_binding,
            "target": target_binding,
            "panel": panel,
            "source_ledger": {
                "summary": ledger_summary,
                "bindings": ledger_bindings,
                "bindings_hash": hash_json(ledger_bindings),
            },
            "declaration": (
                "Only the exact D_evolve P0 panel, compact execution evidence, "
                "archive entry, and attributable costs are imported. Source "
                "observation identities are preserved. No D_test content or "
                "mutation result is imported."
            ),
        }
        contract = {
            **contract_payload,
            "contract_hash": hash_json(contract_payload),
        }
        return contract, copies, archive_entry, source_ledger_records

    def _validate_completed_p0_import(self) -> dict[str, Any]:
        if (
            not self.p0_import_contract_path.is_file()
            or not self.p0_import_completion_path.is_file()
        ):
            raise ConfigurationError(
                "P0 import requires both contract and completion records"
            )
        contract = self._load_json(self.p0_import_contract_path)
        self._require_self_hash(
            contract,
            hash_field="contract_hash",
            label="P0 import contract",
        )
        completion = self._load_json(self.p0_import_completion_path)
        self._require_self_hash(
            completion,
            hash_field="completion_hash",
            label="P0 import completion",
        )
        if completion.get("contract_hash") != contract["contract_hash"]:
            raise ConfigurationError("P0 import completion contract mismatch")
        protocol = self._load_json(self.output_root / "protocol-lock.json")
        if (
            contract.get("target", {}).get("run_id") != self.config.run_id
            or contract.get("target", {}).get("config_hash")
            != self.config.config_hash
            or contract.get("target", {}).get("protocol_lock_sha256")
            != sha256_file(self.output_root / "protocol-lock.json")
            or completion.get("p0_artifact_hash")
            != protocol.get("p0_artifact_hash")
        ):
            raise ConfigurationError("P0 import target binding mismatch")
        if (
            (self.frozen_inputs / "test-140-manifest.json").exists()
            or (
                self.output_root
                / "endpoints"
                / "frozen-inputs"
                / "test-140-manifest.json"
            ).exists()
        ):
            raise ConfigurationError("D_test content exists during P0 import")

        panel = contract["panel"]
        p0_hash = panel["p0_artifact_hash"]
        evolve = self._load_json(
            self.frozen_inputs / "evolve-60-manifest.json"
        )
        ordered_ids = [
            entry["record"]["instance_id"] for entry in evolve["records"]
        ]
        if (
            panel.get("ordered_instance_ids") != ordered_ids
            or panel.get("ordered_instance_ids_sha256") != sha256_ids(ordered_ids)
            or panel.get("task_count") != 60
        ):
            raise ConfigurationError("Imported P0 panel differs from D_evolve")
        target_panel_root = (
            self.output_root / "observations" / "search-p0" / p0_hash
        )
        for observation in panel["observations"]:
            instance_id = observation["instance_id"]
            evidence_files = observation["evidence_files"]
            if hash_json(evidence_files) != observation["evidence_hash"]:
                raise ConfigurationError(
                    f"Imported evidence manifest hash mismatch: {instance_id}"
                )
            for relative_path, expected_sha256 in evidence_files.items():
                relative = Path(relative_path)
                if relative.is_absolute() or ".." in relative.parts:
                    raise ConfigurationError(
                        f"Unsafe imported evidence path: {relative_path}"
                    )
                path = target_panel_root / instance_id / relative
                if (
                    not path.is_file()
                    or path.is_symlink()
                    or sha256_file(path) != expected_sha256
                ):
                    raise ConfigurationError(
                        f"Imported evidence hash mismatch: {path}"
                    )
            raw = self._load_json(
                target_panel_root
                / instance_id
                / "observation.json"
            )
            imported = self._task_observation_from_record(
                raw,
                target_panel_root
                / instance_id
                / "observation.json",
            )
            if (
                imported.identity_hash != observation["identity_hash"]
                or imported.observation_hash
                != observation["observation_hash"]
                or imported.resolved != observation["resolved"]
            ):
                raise ConfigurationError(
                    f"Imported P0 observation mismatch: {instance_id}"
                )
        if hash_json(panel["observations"]) != panel["observations_hash"]:
            raise ConfigurationError("Imported P0 observation panel hash mismatch")
        panel_payload = {
            key: value
            for key, value in panel.items()
            if key != "panel_hash"
        }
        if hash_json(panel_payload) != panel["panel_hash"]:
            raise ConfigurationError("Imported P0 panel self-hash mismatch")

        archive = self._load_archive()
        if (
            len(archive) != 1
            or archive[0].artifact_hash != p0_hash
            or archive[0].resolved_60 != panel["resolved"]
            or archive[0].evaluated_tasks != 60
            or completion.get("archive_hash")
            != hash_json([dataclasses.asdict(archive[0])])
        ):
            raise ConfigurationError("Imported P0 archive binding mismatch")
        ledger_by_charge = {
            record["charge_id"]: record for record in self.ledger.records
        }
        imported_ledger = completion.get("imported_ledger")
        if (
            not isinstance(imported_ledger, list)
            or hash_json(imported_ledger)
            != completion.get("imported_ledger_hash")
        ):
            raise ConfigurationError("Imported P0 ledger completion is invalid")
        expected_source_bindings = [
            (binding["charge_id"], binding["entry_hash"])
            for binding in contract["source_ledger"]["bindings"]
        ]
        actual_source_bindings = [
            (
                binding["source_charge_id"],
                binding["source_entry_hash"],
            )
            for binding in imported_ledger
        ]
        if actual_source_bindings != expected_source_bindings:
            raise ConfigurationError(
                "Imported P0 ledger differs from source contract"
            )
        for binding in imported_ledger:
            target_record = ledger_by_charge.get(binding["target_charge_id"])
            if (
                target_record is None
                or target_record["entry_hash"] != binding["target_entry_hash"]
                or target_record["payload"].get("imported_from", {}).get(
                    "source_entry_hash"
                )
                != binding["source_entry_hash"]
            ):
                raise ConfigurationError(
                    "Imported P0 target ledger binding mismatch"
                )
        return completion

    def _ensure_p0_import_event(
        self,
        contract: Mapping[str, Any],
        completion: Mapping[str, Any],
    ) -> None:
        if any(
            event.event_type == "p0_imported"
            and event.payload.get("contract_hash")
            == contract["contract_hash"]
            for event in self.events.events
        ):
            return
        self.events.append(
            "p0_imported",
            {
                "contract_path": self.p0_import_contract_path.name,
                "contract_hash": contract["contract_hash"],
                "completion_path": self.p0_import_completion_path.name,
                "completion_hash": completion["completion_hash"],
                "source_run_id": contract["source"]["run_id"],
                "p0_artifact_hash": contract["panel"]["p0_artifact_hash"],
                "tasks": contract["panel"]["task_count"],
                "resolved": contract["panel"]["resolved"],
            },
        )

    @staticmethod
    def _p0_task_execution_contract(
        config: Mapping[str, Any],
        execution_stack: Mapping[str, Any],
        evolve_manifest: Mapping[str, Any],
        p0_artifact_hash: str,
    ) -> dict[str, Any]:
        missing = [
            field for field in P0_TASK_CONFIG_FIELDS if field not in config
        ]
        if missing:
            raise ConfigurationError(
                f"P0 task execution config lacks fields: {missing}"
            )
        if config["smoke"]:
            raise ConfigurationError("A smoke P0 panel cannot be imported")
        return {
            "schema_version": SCHEMA_VERSION,
            "config": {
                field: config[field] for field in P0_TASK_CONFIG_FIELDS
            },
            "execution_stack_hash": hash_json(execution_stack),
            "evolve_manifest_hash": hash_json(evolve_manifest),
            "evolve_ordered_instance_ids_sha256": evolve_manifest[
                "ordered_instance_ids_sha256"
            ],
            "p0_artifact_hash": p0_artifact_hash,
        }

    def _validate_source_p0_artifact(
        self,
        source_root: Path,
        p0_artifact_hash: str,
    ) -> None:
        artifact_path = source_root / "artifacts" / p0_artifact_hash
        strategy_path = artifact_path / "strategy.md"
        tools_path = artifact_path / "tools.json"
        lineage_path = artifact_path / "lineage.json"
        record_path = (
            source_root
            / "artifact-records"
            / f"{p0_artifact_hash}.json"
        )
        for path in (strategy_path, tools_path, lineage_path, record_path):
            if not path.is_file() or path.is_symlink():
                raise ConfigurationError(
                    f"Source P0 artifact evidence is missing: {path}"
                )
        tools = self._load_json(tools_path)
        lineage = self._load_json(lineage_path)
        record = self._load_json(record_path)
        if (
            strategy_path.read_text() != ""
            or tools != {"schema_version": 1, "tools": []}
            or lineage != []
            or ArtifactContent(strategy="", tools=()).content_hash
            != p0_artifact_hash
            or record.get("artifact_hash") != p0_artifact_hash
            or record.get("strategy_sha256") != sha256_bytes(b"")
            or record.get("tools_manifest_hash") != hash_json(tools)
        ):
            raise ConfigurationError("Source P0 artifact binding is invalid")

    @staticmethod
    def _require_self_hash(
        record: Mapping[str, Any],
        *,
        hash_field: str,
        label: str,
    ) -> None:
        expected = record.get(hash_field)
        unhashed = {
            key: value for key, value in record.items() if key != hash_field
        }
        if not isinstance(expected, str) or hash_json(unhashed) != expected:
            raise ConfigurationError(f"{label} self-hash mismatch")

    @staticmethod
    def _task_observation_from_record(
        raw: Mapping[str, Any],
        path: Path,
    ) -> TaskObservation:
        expected_fields = set(TaskObservation.__dataclass_fields__)
        if set(raw) != expected_fields:
            raise ConfigurationError(
                f"Observation fields differ from schema: {path}"
            )
        observation_hash = raw.get("observation_hash")
        if (
            hash_json(
                {
                    key: value
                    for key, value in raw.items()
                    if key != "observation_hash"
                }
            )
            != observation_hash
        ):
            raise ConfigurationError(f"Observation hash mismatch: {path}")
        try:
            return TaskObservation(**raw)
        except TypeError as error:
            raise ConfigurationError(
                f"Observation schema is invalid: {path}"
            ) from error

    def _evaluate_records(
        self,
        *,
        artifact_hash_value: str,
        records: Sequence[Mapping[str, Any]],
        role_manifest: Mapping[str, Any],
        dataset_path: Path,
        task_path: Path,
        phase: str,
        budget_scope: str,
    ) -> list[TaskObservation]:
        observations = []
        for entry in self.progress_factory(records, phase, len(records)):
            token_cap, seconds_cap = self._scope_caps(budget_scope)
            if self._phase_exhausted(
                budget_scope,
                token_cap,
                seconds_cap,
                minimum_tokens=self.config.per_task_token_cap,
            ):
                raise BudgetExhausted(f"{budget_scope} reserve exhausted")
            observation = self._evaluate_task(
                artifact_hash_value=artifact_hash_value,
                entry=entry,
                role_manifest=role_manifest,
                dataset_path=dataset_path,
                task_path=task_path,
                phase=phase,
                budget_scope=budget_scope,
            )
            observations.append(observation)
            if not observation.valid:
                raise ObservationInvalid(
                    f"{observation.instance_id}: {observation.status}"
                )
            self._record_pacing_delay(
                budget_scope=budget_scope,
                phase=phase,
                artifact_hash_value=artifact_hash_value,
                instance_id=observation.instance_id,
            )
        return observations

    def _evaluate_task(
        self,
        *,
        artifact_hash_value: str,
        entry: Mapping[str, Any],
        role_manifest: Mapping[str, Any],
        dataset_path: Path,
        task_path: Path,
        phase: str,
        budget_scope: str,
    ) -> TaskObservation:
        row = entry["record"]
        instance_id = row["instance_id"]
        role_hash = hash_json(role_manifest)
        evaluation_dir = (
            self.output_root
            / "observations"
            / phase
            / artifact_hash_value
            / instance_id
        )
        evaluation_dir.mkdir(parents=True, exist_ok=True)
        image_dir = self.output_root / "runtime" / "images" / instance_id
        runtime_args = self._runtime_namespace()
        image_started = time.monotonic()
        image = ensure_instance_image(
            runtime_args,
            dataset_path,
            image_dir,
            instance_id,
        )
        current_image_seconds = time.monotonic() - image_started
        image_digest = docker_capture(
            ["image", "inspect", "--format", "{{.Id}}", image],
            docker_host=self.paths.docker_host,
        )
        execution_stack = self._load_json(
            self.frozen_inputs / "execution-stack.json"
        )
        identity = {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.config.run_id,
            "config_hash": self.config.config_hash,
            "artifact_hash": artifact_hash_value,
            "instance_id": instance_id,
            "repo": row["repo"],
            "base_commit": row["base_commit"],
            "phase": phase,
            "budget_scope": budget_scope,
            "role_manifest_hash": role_hash,
            "model_provider": self.config.model_provider,
            "model_id": self.config.model_id,
            "execution_stack_hash": hash_json(execution_stack),
            "image": image,
            "image_digest": image_digest,
            "artifact_content_hash": self._artifact_content(
                artifact_hash_value
            ).content_hash,
            "per_task_output_token_cap": self.config.per_task_output_token_cap,
            "per_task_token_cap": self.config.per_task_token_cap,
            "agent_timeout_seconds": self.config.agent_timeout_seconds,
            "evaluator_timeout_seconds": self.config.evaluator_timeout_seconds,
            "rollout": 0,
        }
        identity_hash = hash_json(identity)
        observation_path = evaluation_dir / "observation.json"
        if observation_path.exists():
            raw = self._load_json(observation_path)
            if raw.get("identity_hash") != identity_hash:
                raise ConfigurationError(
                    f"Stale observation identity: {observation_path}"
                )
            observation_hash = raw.get("observation_hash")
            if hash_json(
                {key: value for key, value in raw.items() if key != "observation_hash"}
            ) != observation_hash:
                raise ConfigurationError(f"Observation hash mismatch: {observation_path}")
            observation = TaskObservation(
                **{
                    key: raw[key]
                    for key in TaskObservation.__dataclass_fields__
                }
            )
            self._ensure_observation_ledger(observation, budget_scope)
            return observation

        identity_path = evaluation_dir / "identity.json"
        if identity_path.exists() and self._load_json(identity_path) != identity:
            raise ConfigurationError(f"Task identity changed: {identity_path}")
        atomic_json(identity_path, identity)
        result_path = evaluation_dir / "result.json"
        invocation_path = evaluation_dir / "invocation.json"
        workspace = evaluation_dir / "workspace"
        if result_path.exists():
            if not invocation_path.exists():
                raise ObservationInvalid(
                    f"Task result lacks invocation identity: {instance_id}"
                )
            invocation = self._load_json(invocation_path)
            if invocation.get("identity_hash") != identity_hash:
                raise ConfigurationError("Persisted invocation identity mismatch")
            try:
                result = self._load_json(result_path)
            except ConfigurationError as error:
                raise ObservationInvalid(
                    f"Task result is incomplete or corrupt: {instance_id}"
                ) from error
            return_code = int(result.get("runnerExitCode", 0))
            result_sha256 = sha256_file(result_path)
            if (
                invocation.get("result_sha256")
                and invocation["result_sha256"] != result_sha256
            ):
                raise ConfigurationError("Persisted task result hash mismatch")
            invocation["status"] = "result_persisted"
            invocation["result_sha256"] = result_sha256
            atomic_json(invocation_path, invocation)
            image_seconds = float(invocation.get("image_build_seconds", 0.0))
            agent_seconds = float(result.get("durationMs", 0)) / 1000
        else:
            if invocation_path.exists():
                invocation = self._load_json(invocation_path)
                raise ObservationInvalid(
                    "Task invocation is ambiguous after interruption; "
                    f"refusing a second model sample for {instance_id}: "
                    f"{invocation.get('status')}"
                )
            token_cap, _ = self._scope_caps(budget_scope)
            if token_cap is not None:
                remaining = token_cap - int(
                    self.ledger.totals(budget_scope)["budget_counted_tokens"]
                )
                if remaining < self.config.per_task_token_cap:
                    raise BudgetExhausted(
                        f"Insufficient {budget_scope} reserve for task"
                    )
            create_solver_workspace(
                row,
                image,
                workspace,
                self.paths.docker_host,
            )
            invocation = {
                "schema_version": SCHEMA_VERSION,
                "identity_hash": identity_hash,
                "status": "model_call_started",
                "started_at": utc_timestamp(),
                "image_build_seconds": round(current_image_seconds, 3),
            }
            atomic_json(invocation_path, invocation)
            command = [
                self.paths.node,
                str(self.paths.pi_runner),
                "--agent-dir",
                str(self.paths.agent_dir),
                "--instance-id",
                instance_id,
                "--output",
                str(result_path),
                "--task-file",
                str(task_path),
                "--trace",
                str(evaluation_dir / "trace.jsonl"),
                "--workspace",
                str(workspace),
                "--sandbox-image",
                image,
                "--max-output-tokens",
                str(self.config.per_task_output_token_cap),
                "--max-total-tokens",
                str(self.config.per_task_token_cap),
                "--timeout-seconds",
                str(self.config.agent_timeout_seconds),
                "--model-provider",
                self.config.model_provider,
                "--model-id",
                self.config.model_id,
                "--strategy-file",
                str(self._artifact_path(artifact_hash_value) / "strategy.md"),
                "--candidate-artifact",
                str(self._artifact_path(artifact_hash_value)),
            ]
            if self.paths.docker_host:
                command.extend(["--docker-host", self.paths.docker_host])
            agent_started = time.monotonic()
            return_code = run_logged(
                command,
                evaluation_dir / "runner.log",
                cwd=self.paths.repo_root,
                environment=command_environment(self.paths.docker_host),
                timeout=self.config.agent_timeout_seconds + 120,
            )
            agent_seconds = time.monotonic() - agent_started
            if not result_path.exists():
                raise ObservationInvalid(
                    "Pi runner invocation has no durable result; refusing retry "
                    f"for {instance_id} (exit {return_code})"
                )
            try:
                result = self._load_json(result_path)
            except ConfigurationError as error:
                raise ObservationInvalid(
                    f"Pi runner result is corrupt for {instance_id}"
                ) from error
            result["runnerExitCode"] = return_code
            atomic_json(result_path, result)
            invocation["status"] = "result_persisted"
            invocation["result_sha256"] = sha256_file(result_path)
            atomic_json(invocation_path, invocation)
            image_seconds = current_image_seconds

        classification = classify_runner_result(result, return_code)
        valid = classification.valid
        status = classification.status
        resolved = False
        evaluator_seconds = 0.0
        patch = result.get("patch", "")
        if classification.should_grade_patch:
            evaluation_protocol = f"{phase}-{artifact_hash_value[:12]}"
            evaluator_invocation_path = (
                evaluation_dir / "evaluator-invocation.json"
            )
            evaluation_metadata_path = (
                evaluation_dir / evaluation_protocol / "evaluation.json"
            )
            if (
                evaluator_invocation_path.exists()
                and not evaluation_metadata_path.exists()
            ):
                raise ObservationInvalid(
                    "Evaluator invocation is ambiguous after interruption; "
                    f"refusing an untracked rerun for {instance_id}"
                )
            if not evaluator_invocation_path.exists():
                atomic_json(
                    evaluator_invocation_path,
                    {
                        "schema_version": SCHEMA_VERSION,
                        "identity_hash": identity_hash,
                        "status": "evaluator_started",
                        "started_at": utc_timestamp(),
                    },
                )
            evaluator_started = time.monotonic()
            evaluation = evaluate_patch(
                runtime_args,
                dataset_path,
                self.output_root,
                evaluation_dir,
                instance_id,
                evaluation_protocol,
                f"dgm-pi-{artifact_hash_value[:12]}",
                patch,
                role_hash,
            )
            evaluator_seconds = time.monotonic() - evaluator_started
            if evaluation.get("status") != "completed":
                valid = False
                status = "evaluator_invalid"
            else:
                resolved = bool(evaluation.get("resolved"))
                status = "completed"
            evaluator_invocation = self._load_json(evaluator_invocation_path)
            evaluator_invocation["status"] = (
                "completed" if valid else "invalid"
            )
            evaluator_invocation["completed_at"] = utc_timestamp()
            atomic_json(evaluator_invocation_path, evaluator_invocation)
        reported_tokens = total_reported_tokens(result)
        conservative_charge = (
            0
            if classification.telemetry_complete
            else max(0, self.config.per_task_token_cap - reported_tokens)
        )
        unhashed = {
            "instance_id": instance_id,
            "artifact_hash": artifact_hash_value,
            "phase": phase,
            "resolved": resolved,
            "status": status,
            "valid": valid,
            "reported_tokens": reported_tokens,
            "token_telemetry_complete": classification.telemetry_complete,
            "image_build_seconds": round(image_seconds, 3),
            "agent_duration_seconds": round(agent_seconds, 3),
            "evaluator_duration_seconds": round(evaluator_seconds, 3),
            "patch_sha256": sha256_bytes(patch.encode()),
            "identity_hash": identity_hash,
        }
        observation_hash = hash_json(unhashed)
        observation_record = {**unhashed, "observation_hash": observation_hash}
        atomic_json(observation_path, observation_record)
        self.ledger.append(
            f"task:{identity_hash}",
            {
                "budget_scope": budget_scope,
                "kind": "task_agent_and_evaluator",
                "artifact_hash": artifact_hash_value,
                "instance_id": instance_id,
                "phase": phase,
                "reported_tokens": reported_tokens,
                "conservative_token_charge": conservative_charge,
                "active_seconds": round(
                    image_seconds + agent_seconds + evaluator_seconds, 3
                ),
                "image_build_seconds": round(image_seconds, 3),
                "agent_seconds": round(agent_seconds, 3),
                "evaluator_seconds": round(evaluator_seconds, 3),
                "api_calls": 1,
                "task_executions": 1,
                "status": status,
                "valid": valid,
                "resolved": resolved,
            },
        )
        if workspace.exists():
            shutil.rmtree(workspace)
        return TaskObservation(**observation_record)

    def _ensure_observation_ledger(
        self,
        observation: TaskObservation,
        budget_scope: str,
    ) -> None:
        charge_id = f"task:{observation.identity_hash}"
        if charge_id in self.ledger.charge_ids:
            return
        self.ledger.append(
            charge_id,
            {
                "budget_scope": budget_scope,
                "kind": "task_agent_and_evaluator",
                "artifact_hash": observation.artifact_hash,
                "instance_id": observation.instance_id,
                "phase": observation.phase,
                "reported_tokens": observation.reported_tokens,
                "conservative_token_charge": max(
                    0,
                    (
                        0
                        if observation.token_telemetry_complete
                        else self.config.per_task_token_cap
                        - observation.reported_tokens
                    ),
                ),
                "active_seconds": round(
                    observation.image_build_seconds
                    + observation.agent_duration_seconds
                    + observation.evaluator_duration_seconds,
                    3,
                ),
                "image_build_seconds": observation.image_build_seconds,
                "agent_seconds": observation.agent_duration_seconds,
                "evaluator_seconds": observation.evaluator_duration_seconds,
                "api_calls": 1,
                "task_executions": 1,
                "status": observation.status,
                "valid": observation.valid,
                "resolved": observation.resolved,
                "recovered_after_observation_write": True,
            },
        )

    def _endpoint_summary(
        self,
        *,
        records: Sequence[Mapping[str, Any]],
        p0_hash: str,
        final_hash: str,
        test_manifest_hash: str,
    ) -> dict[str, Any]:
        task_ids = [entry["record"]["instance_id"] for entry in records]
        p0 = [
            self._find_endpoint_observation(p0_hash, instance_id)
            for instance_id in task_ids
        ]
        final = (
            p0
            if final_hash == p0_hash
            else [
                self._find_endpoint_observation(final_hash, instance_id)
                for instance_id in task_ids
            ]
        )
        if not all(observation.valid for observation in [*p0, *final]):
            raise ObservationInvalid("Endpoint contains invalid observations")
        p0_outcomes = [observation.resolved for observation in p0]
        final_outcomes = [observation.resolved for observation in final]
        p0_resolved = sum(p0_outcomes)
        final_resolved = sum(final_outcomes)
        p0_only = sum(
            baseline and not candidate
            for baseline, candidate in zip(p0_outcomes, final_outcomes)
        )
        final_only = sum(
            candidate and not baseline
            for baseline, candidate in zip(p0_outcomes, final_outcomes)
        )
        return {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.config.run_id,
            "scope": (
                f"Held-out-adapted {self.config.arm.upper()} Pi strategy/tool "
                "evolution; exploratory single seed."
            ),
            "test_manifest_hash": test_manifest_hash,
            "tasks": len(task_ids),
            "p0_artifact_hash": p0_hash,
            "final_artifact_hash": final_hash,
            "search": self._load_json(self.search_seal_path),
            "p0_reference": {
                "resolved": p0_resolved,
                "accuracy": p0_resolved / len(task_ids),
                "wilson95": wilson_interval(p0_resolved, len(task_ids)),
                "cost": self.ledger.totals("endpoint:p0"),
                "agent_duration_seconds": distribution(
                    [observation.agent_duration_seconds for observation in p0]
                ),
                "evaluator_duration_seconds": distribution(
                    [observation.evaluator_duration_seconds for observation in p0]
                ),
            },
            "final_harness": {
                "resolved": final_resolved,
                "accuracy": final_resolved / len(task_ids),
                "wilson95": wilson_interval(final_resolved, len(task_ids)),
                "cost": (
                    self.ledger.totals("endpoint:p0")
                    if final_hash == p0_hash
                    else self.ledger.totals("endpoint:final")
                ),
                "agent_duration_seconds": distribution(
                    [observation.agent_duration_seconds for observation in final]
                ),
                "evaluator_duration_seconds": distribution(
                    [observation.evaluator_duration_seconds for observation in final]
                ),
            },
            "paired": {
                "absolute_accuracy_difference": (
                    final_resolved - p0_resolved
                )
                / len(task_ids),
                "paired_bootstrap95": paired_bootstrap_interval(
                    p0_outcomes,
                    final_outcomes,
                ),
                "p0_only": p0_only,
                "final_only": final_only,
                "ties": len(task_ids) - p0_only - final_only,
                "exact_mcnemar_p_value": exact_mcnemar_p_value(
                    p0_only, final_only
                ),
            },
            "all_in_cost": {
                "search": self.ledger.totals("search"),
                "p0_reference_endpoint": self.ledger.totals("endpoint:p0"),
                "final_endpoint": (
                    {"shared_with_p0": True}
                    if final_hash == p0_hash
                    else self.ledger.totals("endpoint:final")
                ),
            },
            "task_results": [
                {
                    "instance_id": instance_id,
                    "p0_resolved": baseline,
                    "final_resolved": candidate,
                }
                for instance_id, baseline, candidate in zip(
                    task_ids, p0_outcomes, final_outcomes
                )
            ],
        }

    def _write_markdown_report(self, summary: Mapping[str, Any]) -> None:
        p0 = summary["p0_reference"]
        final = summary["final_harness"]
        paired = summary["paired"]
        search = summary["search"]
        content = "\n".join(
            [
                f"# Matched {self.config.arm.upper()}-on-Pi Held-Out Endpoint",
                "",
                f"Scope: held-out-adapted {self.config.arm.upper()} Pi "
                "strategy/tool evolution, exploratory single seed. Pi core and "
                "host harness source are frozen.",
                "",
                "## Search",
                "",
                f"- Completed proposal slots: {search['completed_proposal_slots']}",
                f"- Archive entries: {search['archive_entries']}",
                f"- Final D_evolve score: {search['final_score_60']:.4f}",
                f"- Search reported tokens: "
                f"{search['search_cost']['reported_tokens']}",
                f"- Search active seconds: "
                f"{search['search_cost']['active_seconds']}",
                "",
                "## D_test",
                "",
                f"- Tasks: {summary['tasks']}",
                f"- P0: {p0['resolved']}/{summary['tasks']} = "
                f"{p0['accuracy']:.4%}",
                f"- Final harness: {final['resolved']}/{summary['tasks']} = "
                f"{final['accuracy']:.4%}",
                f"- Paired difference: "
                f"{paired['absolute_accuracy_difference']:+.4%}",
                f"- P0-only / final-only / ties: "
                f"{paired['p0_only']} / {paired['final_only']} / {paired['ties']}",
                "",
                "## Claim Boundary",
                "",
                "The big-140 panel was hidden from this search but has appeared in "
                "historical repository runs. Results measure isolation from the new "
                "search, not project-wide unseen-benchmark generalization.",
                "",
            ]
        )
        path = self.output_root / "reports" / "heldout_endpoint.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _artifact_observations(
        self, artifact_hash_value: str, *, phase_prefix: str
    ) -> list[TaskObservation]:
        observations = []
        for path in sorted(
            (self.output_root / "observations").glob(
                f"{phase_prefix}*/{artifact_hash_value}/*/observation.json"
            )
        ):
            raw = self._load_json(path)
            observations.append(self._task_observation_from_record(raw, path))
        unique = {observation.instance_id: observation for observation in observations}
        return list(unique.values())

    def _find_endpoint_observation(
        self, artifact_hash_value: str, instance_id: str
    ) -> TaskObservation:
        label = (
            "p0"
            if artifact_hash_value
            == self._load_json(self.output_root / "protocol-lock.json")[
                "p0_artifact_hash"
            ]
            else "final"
        )
        path = (
            self.output_root
            / "observations"
            / f"endpoint-{label}"
            / artifact_hash_value
            / instance_id
            / "observation.json"
        )
        raw = self._load_json(path)
        return self._task_observation_from_record(raw, path)

    def _write_artifact(
        self,
        *,
        strategy: str | None = None,
        lineage: Sequence[MutationDelta] | None = None,
        parent_hash: str | None,
        mutation_record: Mapping[str, Any],
    ) -> str:
        if (strategy is None) == (lineage is None):
            raise ConfigurationError(
                "Artifact write requires exactly one of strategy or lineage"
            )
        evolve_ids = self._evolve_task_ids()
        if lineage is not None:
            try:
                content = materialize_lineage(lineage, evolve_ids)
            except ArtifactValidationError as error:
                raise ConfigurationError(str(error)) from error
        else:
            assert strategy is not None
            try:
                validate_strategy_text(strategy, evolve_ids)
            except ArtifactValidationError as error:
                raise ConfigurationError(str(error)) from error
            content = ArtifactContent(strategy=strategy, tools=())
            lineage = ()
        digest = content.content_hash
        path = self._artifact_path(digest)
        path.mkdir(parents=True, exist_ok=True)
        strategy_path = path / "strategy.md"
        if (
            strategy_path.exists()
            and strategy_path.read_text() != content.strategy
        ):
            raise ConfigurationError("Artifact hash collision or tampering")
        if not strategy_path.exists():
            strategy_path.write_text(content.strategy, encoding="utf-8")
        tools_path = path / "tools.json"
        if tools_path.exists():
            if self._load_json(tools_path) != content.tools_manifest:
                raise ConfigurationError("Artifact tools manifest collision or tampering")
        else:
            atomic_json(tools_path, content.tools_manifest)
        handlers = path / "handlers"
        handlers.mkdir(parents=True, exist_ok=True)
        for tool in content.tools:
            handler_path = path / tool.handler_path
            if (
                handler_path.exists()
                and handler_path.read_text() != tool.handler_code
            ):
                raise ConfigurationError("Artifact handler collision or tampering")
            if not handler_path.exists():
                handler_path.write_text(tool.handler_code, encoding="utf-8")
        lineage_payload = [mutation_delta_to_json(delta) for delta in lineage]
        lineage_hash = hash_json(lineage_payload)
        lineage_path = path / "lineage.json"
        if not lineage_path.exists():
            atomic_json(lineage_path, lineage_payload)
        freeze_file_once(
            self.output_root
            / "artifact-lineages"
            / digest
            / f"{lineage_hash}.json",
            {
                "schema_version": SCHEMA_VERSION,
                "artifact_hash": digest,
                "lineage_hash": lineage_hash,
                "lineage": lineage_payload,
            },
        )
        record = {
            "schema_version": SCHEMA_VERSION,
            "artifact_hash": digest,
            "strategy_sha256": sha256_bytes(content.strategy.encode()),
            "tools_manifest_hash": hash_json(content.tools_manifest),
            "files": [
                "strategy.md",
                "tools.json",
                "lineage.json",
                *[tool.handler_path for tool in content.tools],
            ],
        }
        freeze_file_once(
            self.output_root / "artifact-records" / f"{digest}.json",
            record,
        )
        mutation = dict(mutation_record)
        proposal_key = (
            "p0"
            if mutation.get("kind") == "P0"
            else f"slot-{int(mutation['slot']):04d}"
            if (
                mutation.get("kind") == "Pi strategy/tool mutation"
                and isinstance(mutation.get("slot"), int)
            )
            else (
                f"slot-{int(mutation['slot']):04d}-"
                f"{hash_json(mutation)[:12]}"
            )
            if isinstance(mutation.get("slot"), int)
            else hash_json({"parent": parent_hash, "mutation": mutation})[:16]
        )
        freeze_file_once(
            self.output_root
            / "artifact-proposals"
            / digest
            / f"{proposal_key}.json",
            {
                "schema_version": SCHEMA_VERSION,
                "artifact_hash": digest,
                "parent_artifact_hash": parent_hash,
                "mutation": mutation,
            },
        )
        return digest

    def _artifact_path(self, artifact_hash_value: str) -> Path:
        return self.artifacts_root / artifact_hash_value

    def _artifact_strategy(self, artifact_hash_value: str) -> str:
        artifact_path = self._artifact_path(artifact_hash_value)
        path = artifact_path / "strategy.md"
        if not path.is_file():
            raise ConfigurationError(f"Missing strategy artifact: {artifact_hash_value}")
        return self._artifact_content(artifact_hash_value).strategy

    def _artifact_content(self, artifact_hash_value: str) -> ArtifactContent:
        artifact_path = self._artifact_path(artifact_hash_value)
        strategy_path = artifact_path / "strategy.md"
        tools_path = artifact_path / "tools.json"
        if not strategy_path.is_file() or not tools_path.is_file():
            raise ConfigurationError(
                f"Incomplete artifact content: {artifact_hash_value}"
            )
        raw = self._load_json(tools_path)
        if (
            not isinstance(raw, dict)
            or set(raw) != {"schema_version", "tools"}
            or raw["schema_version"] != 1
            or not isinstance(raw["tools"], list)
        ):
            raise ConfigurationError(f"Invalid tools manifest: {tools_path}")
        tools = []
        for entry in raw["tools"]:
            if not isinstance(entry, dict):
                raise ConfigurationError(f"Invalid tool entry: {tools_path}")
            handler = entry.get("handler")
            handler_path = artifact_path / str(handler)
            if not handler_path.is_file() or handler_path.is_symlink():
                raise ConfigurationError(f"Missing or unsafe tool handler: {handler}")
            try:
                tools.append(
                    CandidateTool(
                        name=entry["name"],
                        label=entry["label"],
                        description=entry["description"],
                        parameters=entry["parameters"],
                        handler_code=handler_path.read_text(),
                        timeout_seconds=entry["timeout_seconds"],
                    )
                )
            except (KeyError, TypeError) as error:
                raise ConfigurationError(
                    f"Invalid tool manifest entry: {entry}"
                ) from error
        content = ArtifactContent(
            strategy=strategy_path.read_text(),
            tools=tuple(tools),
        )
        lineage = self._artifact_lineage(artifact_hash_value)
        try:
            if lineage:
                validated = materialize_lineage(
                    lineage,
                    self._evolve_task_ids(),
                )
            else:
                validate_strategy_text(
                    content.strategy,
                    self._evolve_task_ids(),
                )
                if content.tools:
                    raise ArtifactValidationError(
                        "A direct artifact cannot contain candidate tools"
                    )
                validated = content
        except ArtifactValidationError as error:
            raise ConfigurationError(str(error)) from error
        if validated != content or content.content_hash != artifact_hash_value:
            raise ConfigurationError(
                f"Artifact content or lineage hash mismatch: {artifact_path}"
            )
        return content

    def _artifact_lineage(
        self, artifact_hash_value: str
    ) -> tuple[MutationDelta, ...]:
        path = self._artifact_path(artifact_hash_value) / "lineage.json"
        if not path.is_file():
            raise ConfigurationError(f"Missing artifact lineage: {path}")
        raw = self._load_json(path)
        if not isinstance(raw, list):
            raise ConfigurationError(f"Artifact lineage must be a list: {path}")
        try:
            return tuple(mutation_delta_from_json(item) for item in raw)
        except (
            ArtifactValidationError,
            KeyError,
            TypeError,
            ValueError,
        ) as error:
            raise ConfigurationError(f"Invalid artifact lineage: {path}") from error

    def _evolve_task_ids(self) -> tuple[str, ...]:
        path = self.frozen_inputs / "evolve-60-manifest.json"
        if not path.is_file():
            return ()
        manifest = self._load_json(path)
        return tuple(
            entry["record"]["instance_id"] for entry in manifest["records"]
        )

    def _load_archive(self) -> list[ArchiveEntry]:
        if not self.archive_path.exists():
            return []
        raw = self._load_json(self.archive_path)
        entries = [
            ArchiveEntry(
                **{
                    **entry,
                    "functioning_child_slots": tuple(
                        entry.get("functioning_child_slots", ())
                    ),
                }
            )
            for entry in raw["entries"]
        ]
        if raw.get("archive_hash") != hash_json(
            [dataclasses.asdict(entry) for entry in entries]
        ):
            raise ConfigurationError("Archive hash mismatch")
        return entries

    def _write_archive(self, entries: Sequence[ArchiveEntry]) -> None:
        payload = [dataclasses.asdict(entry) for entry in entries]
        atomic_json(
            self.archive_path,
            {
                "schema_version": SCHEMA_VERSION,
                "entries": payload,
                "archive_hash": hash_json(payload),
            },
        )

    @staticmethod
    def _increment_child_count(
        entries: Sequence[ArchiveEntry], parent_hash: str, slot: int
    ) -> list[ArchiveEntry]:
        found = False
        updated = []
        for entry in entries:
            if entry.artifact_hash == parent_hash:
                if slot not in entry.functioning_child_slots:
                    entry = dataclasses.replace(
                        entry,
                        functioning_child_count=entry.functioning_child_count + 1,
                        functioning_child_slots=(
                            *entry.functioning_child_slots,
                            slot,
                        ),
                    )
                found = True
            updated.append(entry)
        if not found:
            raise ConfigurationError(f"Parent is absent from archive: {parent_hash}")
        return updated

    def _load_search_state(self) -> dict[str, Any]:
        if not self.search_state_path.exists():
            state = {
                "schema_version": SCHEMA_VERSION,
                "next_slot": 0,
                "updated_at": utc_timestamp(),
            }
            atomic_json(self.search_state_path, state)
            return state
        return self._load_json(self.search_state_path)

    def _phase_exhausted(
        self,
        scope: str,
        token_cap: int | None,
        seconds_cap: int,
        *,
        minimum_tokens: int,
    ) -> bool:
        totals = self.ledger.totals(scope)
        return (
            (
                token_cap is not None
                and int(totals["budget_counted_tokens"]) + minimum_tokens
                > token_cap
            )
            or float(totals["active_seconds"]) >= seconds_cap
        )

    def _record_pacing_delay(
        self,
        *,
        budget_scope: str,
        phase: str,
        artifact_hash_value: str,
        instance_id: str,
    ) -> None:
        if self.config.inter_task_delay_seconds <= 0:
            return
        delay_id = (
            f"delay:{budget_scope}:{phase}:{artifact_hash_value}:{instance_id}"
        )
        if delay_id in self.ledger.charge_ids:
            return
        time.sleep(self.config.inter_task_delay_seconds)
        self.ledger.append(
            delay_id,
            {
                "budget_scope": budget_scope,
                "kind": "request_pacing",
                "reported_tokens": 0,
                "conservative_token_charge": 0,
                "active_seconds": self.config.inter_task_delay_seconds,
                "api_calls": 0,
                "task_executions": 0,
                "status": "completed",
            },
        )

    def _scope_caps(self, scope: str) -> tuple[int | None, int]:
        if scope == "search":
            return (
                self.config.search_token_cap,
                self.config.search_active_seconds_cap,
            )
        if scope == "endpoint:p0":
            return (
                self.config.reference_endpoint_token_cap,
                self.config.endpoint_active_seconds_cap,
            )
        if scope == "endpoint:final":
            return (
                self.config.final_endpoint_token_cap,
                self.config.endpoint_active_seconds_cap,
            )
        raise ConfigurationError(f"Unknown budget scope: {scope}")

    @staticmethod
    def _require_complete_valid_panel(
        observations: Sequence[TaskObservation], expected: int
    ) -> None:
        if len(observations) != expected:
            raise ObservationInvalid(
                f"Panel incomplete: expected {expected}, found {len(observations)}"
            )
        if not all(observation.valid for observation in observations):
            raise ObservationInvalid("Panel contains an invalid observation")

    def _runtime_namespace(self) -> SimpleNamespace:
        return SimpleNamespace(
            repo_root=self.paths.repo_root,
            docker_host=self.paths.docker_host,
            swebench_source=self.paths.swebench_source,
            swebench_python=self.paths.swebench_python,
            image_builder=self.paths.image_builder,
            build_wheelhouse=self.paths.build_wheelhouse,
            image_build_retries=self.config.image_build_retries,
            image_build_retry_delay_seconds=self.config.image_build_retry_delay_seconds,
            image_build_timeout_seconds=self.config.image_build_timeout_seconds,
            evaluator_timeout_seconds=self.config.evaluator_timeout_seconds,
            swebench_revision=self._swebench_revision(),
            model_id=self.config.model_id,
        )

    def _execution_stack_identity(self) -> dict[str, Any]:
        package_root = (
            self.paths.repo_root
            / "pi-rollback"
            / "node_modules"
            / "@earendil-works"
            / "pi-coding-agent"
        )
        models_store = self.paths.agent_dir / "models-store.json"
        auth_path = self.paths.agent_dir / "auth.json"
        swebench_python = Path(
            shutil.which(self.paths.swebench_python)
            or self.paths.swebench_python
        ).resolve()
        if not swebench_python.is_file():
            raise ConfigurationError(
                f"SWE-bench Python is missing: {swebench_python}"
            )
        python_version = subprocess.run(
            [str(swebench_python), "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
        pip_freeze = subprocess.run(
            [str(swebench_python), "-m", "pip", "freeze", "--all"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        return {
            "schema_version": SCHEMA_VERSION,
            "orchestrator_sha256": sha256_file(
                self.paths.repo_root
                / "rollback_mvp"
                / "orchestrate_endpoint_200.py"
            ),
            "image_builder_sha256": sha256_file(self.paths.image_builder),
            "pi_runner_sha256": sha256_file(self.paths.pi_runner),
            "candidate_tool_runtime_sha256": sha256_file(
                self.paths.repo_root
                / "rollback_mvp"
                / "candidate_tool_runtime.mjs"
            ),
            "pi_package_json_sha256": sha256_file(package_root / "package.json"),
            "pi_package_dist_tree_hash": directory_hash(package_root / "dist"),
            "pi_rollback_package_lock_sha256": sha256_file(
                self.paths.repo_root / "pi-rollback" / "package-lock.json"
            ),
            "agent_models_sha256": sha256_file(
                self.paths.agent_dir / "models.json"
            ),
            "agent_models_store_sha256": (
                sha256_file(models_store) if models_store.exists() else None
            ),
            "agent_auth_shape_sha256": (
                sha256_file(auth_path) if auth_path.exists() else None
            ),
            "swebench_revision": self._swebench_revision(),
            "swebench_python": str(swebench_python),
            "swebench_python_sha256": sha256_file(swebench_python),
            "swebench_python_version": (
                python_version.stdout.strip() or python_version.stderr.strip()
            ),
            "swebench_python_freeze_sha256": sha256_bytes(
                pip_freeze.encode()
            ),
            "node_version": subprocess.run(
                [self.paths.node, "--version"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip(),
        }

    def _swebench_revision(self) -> str:
        return subprocess.run(
            ["git", "-C", str(self.paths.swebench_source), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def _endpoint_state_path(self) -> Path:
        return self.output_root / "endpoint-consumption.json"

    @staticmethod
    def _load_json(path: Path) -> Any:
        try:
            return json.loads(path.read_text())
        except (OSError, json.JSONDecodeError) as error:
            raise ConfigurationError(f"Cannot load JSON from {path}: {error}") from error


def require_paid_confirmation(value: str | None) -> None:
    if value != PAID_CONFIRMATION:
        raise ConfigurationError(
            f"Paid execution requires --confirm-paid-run {PAID_CONFIRMATION}"
        )
