"""Versioned, dependency-free data contracts for adaptive evaluation."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = 1
EXPECTED_DATASET_MANIFEST_SHA256 = (
    "3fb913fbc73a05c1f7cae3b708c976374632820b58377aab5de08b742f96c967"
)
EXPECTED_ORDERED_IDS_SHA256 = (
    "421c950302366954005dab020cdc89ca0d6ae1f0423e2b662637f7790a31d0d7"
)
EXPECTED_TASK_COUNT = 200
EXPECTED_REPOSITORY_COUNTS = {"astropy": 22, "django": 153, "sphinx": 25}
EMBEDDING_MODEL_ID = "mlx-community/Qwen3-Embedding-0.6B-4bit-DWQ"
EMBEDDING_MODEL_REVISION = "6c3ae70858513f1a78e9cdca3cae330d9075cd2a"
EMBEDDING_DIMENSION = 1024
QUERY_TEMPLATE_REVISION = "qwen3-swe-relevance-v1"
QUERY_TEMPLATE = (
    "Instruct: Retrieve SWE-bench tasks whose affected behavior is relevant to a\n"
    "coding-agent evolution and its observed failure mode.\n"
    "Query: {query}"
)


class AdaptiveEvalError(RuntimeError):
    """Base class for terminal controller errors."""


class ValidationError(AdaptiveEvalError):
    """A frozen contract or evidence record is invalid."""


class InfrastructureError(AdaptiveEvalError):
    """Required infrastructure is absent or has the wrong identity."""


class SelectorError(AdaptiveEvalError):
    """Selector output or tool behavior violates the frozen protocol."""


class PairExecutionError(AdaptiveEvalError):
    """Paired evidence is incomplete or has inconsistent identity."""


class ContainerIsolationError(AdaptiveEvalError):
    """The full-candidate container boundary cannot be established."""


class RetrievalRole(StrEnum):
    REPAIR_CAUSE = "repair_cause"
    REGRESSION = "regression"
    REPRESENTATIVE_COVERAGE = "representative_coverage"


class DecisionOutcome(StrEnum):
    ACCEPT = "ACCEPT"
    ROLLBACK = "ROLLBACK"
    ESCALATE = "ESCALATE"
    INVALID = "INVALID"


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def hash_json(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def ordered_ids_hash(instance_ids: Sequence[str]) -> str:
    return sha256_bytes("".join(f"{item}\n" for item in instance_ids).encode())


def dataclass_dict(value: Any) -> dict[str, Any]:
    if not dataclasses.is_dataclass(value) or isinstance(value, type):
        raise TypeError(f"Expected dataclass instance, found {type(value).__name__}")
    return dataclasses.asdict(value)


def require_nonempty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} must be a non-empty string")
    return value


def require_sha256(value: str, field_name: str) -> str:
    require_nonempty(value, field_name)
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ValidationError(f"{field_name} must be a lowercase SHA-256 digest")
    return value


def require_unique_strings(values: Sequence[str], field_name: str) -> tuple[str, ...]:
    result = tuple(values)
    if not all(isinstance(value, str) and value for value in result):
        raise ValidationError(f"{field_name} must contain non-empty strings")
    if len(result) != len(set(result)):
        raise ValidationError(f"{field_name} contains duplicates")
    return result


def source_tree_records(path: Path) -> tuple[dict[str, Any], ...]:
    if not path.is_dir():
        raise ValidationError(f"Source snapshot must be a directory: {path}")
    records: list[dict[str, Any]] = []
    for item in sorted(path.rglob("*")):
        relative = item.relative_to(path).as_posix()
        if item.is_symlink():
            raise ValidationError(f"Source snapshot contains a symlink: {relative}")
        if item.is_dir():
            continue
        if not item.is_file():
            raise ValidationError(f"Source snapshot contains a non-regular file: {relative}")
        records.append(
            {
                "path": relative,
                "mode": item.stat().st_mode & 0o777,
                "sha256": sha256_bytes(item.read_bytes()),
            }
        )
    return tuple(records)


def source_tree_hash(path: Path) -> str:
    return hash_json({"schema_version": 1, "files": source_tree_records(path)})


def source_diff_hash(parent: Path, child: Path) -> str:
    parent_records = {item["path"]: item for item in source_tree_records(parent)}
    child_records = {item["path"]: item for item in source_tree_records(child)}
    changes = [
        {"path": path, "parent": parent_records.get(path), "child": child_records.get(path)}
        for path in sorted(set(parent_records) | set(child_records))
        if parent_records.get(path) != child_records.get(path)
    ]
    return hash_json(
        {
            "schema_version": 1,
            "parent_artifact_hash": source_tree_hash(parent),
            "child_artifact_hash": source_tree_hash(child),
            "changes": changes,
        }
    )


@dataclass(frozen=True, slots=True)
class TaskCard:
    instance_id: str
    repo: str
    base_commit: str
    problem_statement: str
    lexical_terms: tuple[str, ...]
    structured_tags: tuple[str, ...]
    task_text_hash: str
    embedding_id: str
    embedding_vector_hash: str
    catalogue_revision: str

    def __post_init__(self) -> None:
        for name in ("instance_id", "repo", "base_commit", "problem_statement"):
            require_nonempty(getattr(self, name), name)
        require_unique_strings(self.lexical_terms, "lexical_terms")
        require_unique_strings(self.structured_tags, "structured_tags")
        require_sha256(self.task_text_hash, "task_text_hash")
        require_sha256(self.catalogue_revision, "catalogue_revision")
        if bool(self.embedding_id) != bool(self.embedding_vector_hash):
            raise ValidationError(
                "embedding_id and embedding_vector_hash must both be present or absent"
            )
        if self.embedding_vector_hash:
            require_sha256(self.embedding_id, "embedding_id")
            require_sha256(self.embedding_vector_hash, "embedding_vector_hash")

    @property
    def task_text(self) -> str:
        return (
            f"Instance: {self.instance_id}\nRepository: {self.repo}\n"
            f"Base commit: {self.base_commit}\nIssue:\n{self.problem_statement}"
        )


@dataclass(frozen=True, slots=True)
class BadCaseCard:
    bad_case_id: str
    parent_artifact_hash: str
    instance_id: str
    outcome: str
    failure_taxonomy: str
    trajectory_summary: str
    tool_error_fingerprints: tuple[str, ...]
    changed_paths: tuple[str, ...]
    public_test_summary: str
    source_trace_hash: str
    created_at: str

    def __post_init__(self) -> None:
        for name in (
            "bad_case_id",
            "instance_id",
            "outcome",
            "failure_taxonomy",
            "trajectory_summary",
            "created_at",
        ):
            require_nonempty(getattr(self, name), name)
        require_sha256(self.parent_artifact_hash, "parent_artifact_hash")
        require_sha256(self.source_trace_hash, "source_trace_hash")
        require_unique_strings(self.tool_error_fingerprints, "tool_error_fingerprints")
        require_unique_strings(self.changed_paths, "changed_paths")


@dataclass(frozen=True, slots=True)
class CandidateChangeCard:
    parent_artifact_hash: str
    child_artifact_hash: str
    diff_hash: str
    changed_paths: tuple[str, ...]
    changed_symbols: tuple[str, ...]
    dependency_change: str
    mutation_summary: str
    source_revision: str
    created_at: str

    def __post_init__(self) -> None:
        for name in ("parent_artifact_hash", "child_artifact_hash", "diff_hash"):
            require_sha256(getattr(self, name), name)
        require_unique_strings(self.changed_paths, "changed_paths")
        require_unique_strings(self.changed_symbols, "changed_symbols")
        for name in ("dependency_change", "mutation_summary", "source_revision", "created_at"):
            require_nonempty(getattr(self, name), name)


@dataclass(frozen=True, slots=True)
class CatalogueManifest:
    source_path: str
    dataset_manifest_hash: str
    ordered_ids_hash: str
    catalogue_hash: str
    task_ids: tuple[str, ...]
    cards: tuple[TaskCard, ...]
    embedding_index_hash: str = ""
    embedding_response_hash: str = ""

    def __post_init__(self) -> None:
        require_nonempty(self.source_path, "source_path")
        for name in ("dataset_manifest_hash", "ordered_ids_hash", "catalogue_hash"):
            require_sha256(getattr(self, name), name)
        require_unique_strings(self.task_ids, "task_ids")
        if self.dataset_manifest_hash != EXPECTED_DATASET_MANIFEST_SHA256:
            raise ValidationError("Catalogue uses a non-DGM-200 dataset manifest")
        if self.ordered_ids_hash != EXPECTED_ORDERED_IDS_SHA256:
            raise ValidationError("Catalogue uses a non-DGM-200 ordered-ID hash")
        if len(self.task_ids) != EXPECTED_TASK_COUNT:
            raise ValidationError("Catalogue must contain exactly the frozen 200 tasks")
        if tuple(card.instance_id for card in self.cards) != self.task_ids:
            raise ValidationError("Task cards do not match frozen task ID order")
        if bool(self.embedding_index_hash) != bool(self.embedding_response_hash):
            raise ValidationError(
                "embedding_index_hash and embedding_response_hash must both be present or absent"
            )
        if self.embedding_index_hash:
            require_sha256(self.embedding_index_hash, "embedding_index_hash")
            require_sha256(self.embedding_response_hash, "embedding_response_hash")

    @property
    def by_id(self) -> Mapping[str, TaskCard]:
        return {card.instance_id: card for card in self.cards}


@dataclass(frozen=True, slots=True)
class EmbeddingSpec:
    sidecar_url: str
    sidecar_manifest_hash: str
    model_id: str = EMBEDDING_MODEL_ID
    model_revision: str = EMBEDDING_MODEL_REVISION
    dimension: int = EMBEDDING_DIMENSION
    normalized: bool = True
    max_length: int = 2048
    query_template_revision: str = QUERY_TEMPLATE_REVISION

    def __post_init__(self) -> None:
        require_nonempty(self.sidecar_url, "sidecar_url")
        require_sha256(self.sidecar_manifest_hash, "sidecar_manifest_hash")
        if self.model_id != EMBEDDING_MODEL_ID:
            raise ValidationError(f"Unsupported embedding model: {self.model_id}")
        if self.model_revision != EMBEDDING_MODEL_REVISION:
            raise ValidationError("Embedding model revision does not match frozen revision")
        if self.dimension != EMBEDDING_DIMENSION or not self.normalized:
            raise ValidationError("Embedding contract requires normalized 1024-D vectors")
        if self.max_length != 2048:
            raise ValidationError("Embedding max_length must be the frozen value 2048")
        if self.query_template_revision != QUERY_TEMPLATE_REVISION:
            raise ValidationError("Embedding query template revision mismatch")


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    schema_version: int
    task_budget: int
    max_rounds: int
    max_tasks_per_round: int
    audit_size: int
    max_tool_calls_per_round: int
    per_task_timeout_seconds: int
    per_task_token_budget: int
    per_task_retry_budget: int
    per_task_tool_budget: int
    selector_token_budget: int
    selector_time_limit_seconds: int
    experiment_seed: str
    selector_model_revision: str
    embedding_model_revision: str
    embedding_manifest_hash: str

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValidationError(f"Unsupported config schema_version: {self.schema_version}")
        positive = (
            "task_budget",
            "max_rounds",
            "max_tasks_per_round",
            "max_tool_calls_per_round",
            "per_task_timeout_seconds",
            "per_task_token_budget",
            "per_task_tool_budget",
            "selector_token_budget",
            "selector_time_limit_seconds",
        )
        for name in positive:
            if getattr(self, name) <= 0:
                raise ValidationError(f"{name} must be positive")
        if self.audit_size <= 0:
            raise ValidationError("audit_size must be positive for the independent audit guard")
        if self.per_task_retry_budget < 0:
            raise ValidationError("per_task_retry_budget cannot be negative")
        if self.task_budget + self.audit_size > EXPECTED_TASK_COUNT:
            raise ValidationError("task_budget plus audit_size exceeds frozen catalogue")
        if self.max_tasks_per_round > self.task_budget:
            raise ValidationError("max_tasks_per_round cannot exceed task_budget")
        for name in ("experiment_seed", "selector_model_revision"):
            require_nonempty(getattr(self, name), name)
        if self.embedding_model_revision != EMBEDDING_MODEL_REVISION:
            raise ValidationError("Config embedding revision does not match frozen revision")
        require_sha256(self.embedding_manifest_hash, "embedding_manifest_hash")

    @property
    def config_hash(self) -> str:
        return hash_json(dataclass_dict(self))


@dataclass(frozen=True, slots=True)
class TaskProposal:
    instance_id: str
    retrieval_role: RetrievalRole
    evidence_reference: str
    expected_signal: str
    rationale: str
    necessary_distinct_reason: str = ""

    def __post_init__(self) -> None:
        for name in (
            "instance_id",
            "evidence_reference",
            "expected_signal",
            "rationale",
        ):
            require_nonempty(getattr(self, name), name)
        if self.retrieval_role is RetrievalRole.REPRESENTATIVE_COVERAGE:
            if self.necessary_distinct_reason:
                raise ValidationError(
                    "Coverage proposals cannot claim a causal distinctness exception"
                )


@dataclass(frozen=True, slots=True)
class SelectedTask:
    proposal: TaskProposal
    marginal_coverage: float
    selection_source: str

    def __post_init__(self) -> None:
        if not math.isfinite(self.marginal_coverage) or self.marginal_coverage < 0:
            raise ValidationError("marginal_coverage must be finite and non-negative")
        require_nonempty(self.selection_source, "selection_source")


@dataclass(frozen=True, slots=True)
class DecisionPolicy:
    schema_version: int
    confidence_level: float
    bootstrap_seed: int
    bootstrap_samples: int
    acceptance_margin: float
    rollback_margin: float
    audit_guard_min_delta: float
    escalation_task_cap: int

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValidationError("Unsupported decision policy schema version")
        if not 0 < self.confidence_level < 1:
            raise ValidationError("confidence_level must be between zero and one")
        if self.bootstrap_samples <= 0:
            raise ValidationError("bootstrap_samples must be positive")
        for name in ("acceptance_margin", "rollback_margin", "audit_guard_min_delta"):
            if not -1 <= getattr(self, name) <= 1:
                raise ValidationError(f"{name} must be between -1 and 1")
        if self.rollback_margin > self.acceptance_margin:
            raise ValidationError("rollback_margin cannot exceed acceptance_margin")
        if self.escalation_task_cap <= 0:
            raise ValidationError("escalation_task_cap must be positive")


def load_strict_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"Cannot load JSON from {path}: {error}") from error
