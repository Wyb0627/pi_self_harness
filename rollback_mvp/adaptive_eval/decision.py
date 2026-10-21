"""Deterministic three-state decision engine over complete paired evidence."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import random
from dataclasses import dataclass
from typing import Sequence

from .paired_executor import ExecutionSettings, FrozenTaskPlan, PairResult
from .schemas import (
    CatalogueManifest,
    DecisionOutcome,
    DecisionPolicy,
    ExperimentConfig,
    PairExecutionError,
)
from .schemas import hash_json


@dataclass(frozen=True, slots=True)
class DecisionResult:
    outcome: DecisionOutcome
    final_manifest_hash: str
    task_count: int
    child_only_wins: int
    parent_only_wins: int
    ties_both_pass: int
    ties_both_fail: int
    mean_delta: float
    confidence_interval: tuple[float, float]
    exact_mcnemar_p_value: float
    audit_delta: float
    audit_guard_passed: bool
    rationale: str
    expansion_task_cap: int | None


def percentile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise PairExecutionError("Cannot compute percentile of empty values")
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def paired_bootstrap_interval(
    deltas: Sequence[int], policy: DecisionPolicy
) -> tuple[float, float]:
    if not deltas or any(delta not in {-1, 0, 1} for delta in deltas):
        raise PairExecutionError("Bootstrap requires non-empty paired {-1,0,1} deltas")
    generator = random.Random(policy.bootstrap_seed)
    count = len(deltas)
    samples = [
        sum(deltas[generator.randrange(count)] for _ in range(count)) / count
        for _ in range(policy.bootstrap_samples)
    ]
    alpha = 1 - policy.confidence_level
    return percentile(samples, alpha / 2), percentile(samples, 1 - alpha / 2)


def exact_mcnemar_p_value(parent_only: int, child_only: int) -> float:
    discordant = parent_only + child_only
    if discordant == 0:
        return 1.0
    tail = min(parent_only, child_only)
    probability = sum(math.comb(discordant, index) for index in range(tail + 1)) / (2**discordant)
    return min(1.0, 2 * probability)


def validate_complete_pairs(
    plan: FrozenTaskPlan,
    pairs: Sequence[PairResult],
    catalogue: CatalogueManifest,
    settings: ExecutionSettings,
    config: ExperimentConfig,
) -> tuple[PairResult, ...]:
    values = tuple(pairs)
    if not values:
        raise PairExecutionError("Final paired evidence cannot be empty")
    ids = [pair.task_instance_id for pair in values]
    if len(ids) != len(set(ids)):
        raise PairExecutionError("Duplicate pair results exist for a final task")
    if tuple(ids) != plan.final_task_ids:
        missing = sorted(set(plan.final_task_ids) - set(ids))
        extra = sorted(set(ids) - set(plan.final_task_ids))
        raise PairExecutionError(
            f"Pair results do not exactly match final manifest: missing={missing}, extra={extra}"
        )
    for pair in values:
        pair_payload = {
            "task_instance_id": pair.task_instance_id,
            "final_manifest_hash": pair.final_manifest_hash,
            "parent_identity_hash": pair.parent_identity_hash,
            "child_identity_hash": pair.child_identity_hash,
            "paired_identity_hash": pair.paired_identity_hash,
            "paired_identity_payload": pair.paired_identity_payload,
            "parent": dataclasses.asdict(pair.parent),
            "child": dataclasses.asdict(pair.child),
            "execution_order": pair.execution_order,
        }
        if pair.pair_hash != hashlib.sha256(
            json.dumps(
                pair_payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
            ).encode()
        ).hexdigest():
            raise PairExecutionError("Pair result hash mismatch")
        if pair.final_manifest_hash != plan.manifest_hash:
            raise PairExecutionError("Pair result uses a different final manifest hash")
        if pair.parent.execution_identity_hash != pair.parent_identity_hash:
            raise PairExecutionError("Parent observation identity mismatch")
        if pair.child.execution_identity_hash != pair.child_identity_hash:
            raise PairExecutionError("Child observation identity mismatch")
        if pair.paired_identity_hash != hash_json(pair.paired_identity_payload):
            raise PairExecutionError("Paired execution identity payload hash mismatch")
        identity = pair.paired_identity_payload
        required_identity_keys = {
            "schema_version",
            "task_instance_id",
            "task_repo",
            "task_base_commit",
            "parent_artifact_hash",
            "child_artifact_hash",
            "dataset_manifest_hash",
            "final_manifest_hash",
            "model",
            "budgets",
            "runner",
            "evaluator",
            "container_policy_hash",
        }
        if set(identity) != required_identity_keys or identity.get("schema_version") != 1:
            raise PairExecutionError("Paired execution identity schema is invalid")
        model = identity["model"]
        if not isinstance(model, dict) or set(model) != {
            "provider",
            "model_id",
            "model_revision",
            "inference_settings",
        }:
            raise PairExecutionError("Paired model identity schema is invalid")
        if any(not isinstance(model[key], str) or not model[key] for key in ("provider", "model_id", "model_revision")):
            raise PairExecutionError("Paired model identity lacks required strings")
        if not isinstance(model["inference_settings"], (list, tuple)):
            raise PairExecutionError("Paired inference settings are invalid")
        budgets = identity["budgets"]
        if not isinstance(budgets, dict) or set(budgets) != {
            "timeout_seconds",
            "token_budget",
            "retry_budget",
            "tool_budget",
        }:
            raise PairExecutionError("Paired budget identity schema is invalid")
        if any(
            isinstance(value, bool) or not isinstance(value, int) or value < 0
            for value in budgets.values()
        ):
            raise PairExecutionError("Paired budget identity contains invalid values")
        for component in ("runner", "evaluator"):
            value = identity[component]
            if not isinstance(value, dict) or set(value) != {"image", "image_digest", "revision"}:
                raise PairExecutionError(f"Paired {component} identity schema is invalid")
            if any(not isinstance(value[key], str) or not value[key] for key in ("image", "revision")):
                raise PairExecutionError(f"Paired {component} identity lacks required strings")
            if len(value["image_digest"]) != 64:
                raise PairExecutionError(f"Paired {component} digest is invalid")
        if not isinstance(identity["container_policy_hash"], str) or len(identity["container_policy_hash"]) != 64:
            raise PairExecutionError("Paired container policy hash is invalid")
        expected_model = dataclasses.asdict(settings.model)
        if model != expected_model:
            raise PairExecutionError("Paired model identity differs from frozen settings")
        expected_budgets = {
            "timeout_seconds": config.per_task_timeout_seconds,
            "token_budget": config.per_task_token_budget,
            "retry_budget": config.per_task_retry_budget,
            "tool_budget": config.per_task_tool_budget,
        }
        if budgets != expected_budgets:
            raise PairExecutionError("Paired budgets differ from frozen config")
        expected_runner = {
            "image": settings.runner_image,
            "image_digest": settings.runner_image_digest,
            "revision": settings.runner_revision,
        }
        expected_evaluator = {
            "image": settings.evaluator_image,
            "image_digest": settings.evaluator_image_digest,
            "revision": settings.evaluator_revision,
        }
        if identity["runner"] != expected_runner:
            raise PairExecutionError("Paired runner identity differs from frozen settings")
        if identity["evaluator"] != expected_evaluator:
            raise PairExecutionError("Paired evaluator identity differs from frozen settings")
        if identity["container_policy_hash"] != settings.container_policy_hash:
            raise PairExecutionError(
                "Paired container policy differs from frozen settings"
            )
        card = catalogue.by_id[pair.task_instance_id]
        if identity.get("task_repo") != card.repo:
            raise PairExecutionError("Paired execution identity has the wrong task repo")
        if identity.get("task_base_commit") != card.base_commit:
            raise PairExecutionError(
                "Paired execution identity has the wrong task base commit"
            )
        if identity.get("task_instance_id") != pair.task_instance_id:
            raise PairExecutionError("Paired execution identity has the wrong task")
        if identity.get("final_manifest_hash") != plan.manifest_hash:
            raise PairExecutionError("Paired execution identity has the wrong final manifest")
        if identity.get("dataset_manifest_hash") != plan.dataset_manifest_hash:
            raise PairExecutionError("Paired execution identity has the wrong dataset manifest")
        if identity.get("parent_artifact_hash") != plan.parent_artifact_hash:
            raise PairExecutionError("Paired execution identity has the wrong parent artifact")
        if identity.get("child_artifact_hash") != plan.child_artifact_hash:
            raise PairExecutionError("Paired execution identity has the wrong child artifact")
        expected_parent_identity = hash_json(
            identity | {"artifact_role": "parent", "artifact_hash": plan.parent_artifact_hash}
        )
        expected_child_identity = hash_json(
            identity | {"artifact_role": "child", "artifact_hash": plan.child_artifact_hash}
        )
        if pair.parent_identity_hash != expected_parent_identity:
            raise PairExecutionError("Parent identity is not derived from paired identity")
        if pair.child_identity_hash != expected_child_identity:
            raise PairExecutionError("Child identity is not derived from paired identity")
        if pair.execution_order not in {("parent", "child"), ("child", "parent")}:
            raise PairExecutionError("Pair execution order is invalid")
    shared_fields = (
        "model",
        "budgets",
        "runner",
        "evaluator",
        "container_policy_hash",
    )
    baseline = {field: values[0].paired_identity_payload.get(field) for field in shared_fields}
    for pair in values[1:]:
        current = {field: pair.paired_identity_payload.get(field) for field in shared_fields}
        if current != baseline:
            raise PairExecutionError("Final pairs use inconsistent execution settings")
    return values


def decide(
    plan: FrozenTaskPlan,
    pairs: Sequence[PairResult],
    policy: DecisionPolicy,
    catalogue: CatalogueManifest,
    settings: ExecutionSettings,
    config: ExperimentConfig,
) -> DecisionResult:
    values = validate_complete_pairs(plan, pairs, catalogue, settings, config)
    deltas = tuple(pair.delta for pair in values)
    lower, upper = paired_bootstrap_interval(deltas, policy)
    child_only = sum(delta == 1 for delta in deltas)
    parent_only = sum(delta == -1 for delta in deltas)
    both_pass = sum(pair.parent.resolved and pair.child.resolved for pair in values)
    both_fail = sum(not pair.parent.resolved and not pair.child.resolved for pair in values)
    audit_ids = set(plan.audit_task_ids)
    audit_values = [pair.delta for pair in values if pair.task_instance_id in audit_ids]
    audit_delta = sum(audit_values) / len(audit_values) if audit_values else 0.0
    audit_guard_passed = bool(audit_values) and audit_delta >= policy.audit_guard_min_delta
    if lower > policy.acceptance_margin and audit_guard_passed:
        outcome = DecisionOutcome.ACCEPT
        rationale = "Bootstrap lower bound clears acceptance margin and audit guard passes."
        expansion_cap = None
    elif upper <= policy.rollback_margin:
        outcome = DecisionOutcome.ROLLBACK
        rationale = "Bootstrap upper bound is at or below rollback margin."
        expansion_cap = None
    else:
        outcome = DecisionOutcome.ESCALATE
        rationale = (
            "Evidence is inconclusive or targeted and independent-audit evidence disagree; "
            "hold child for a separately bounded expansion."
        )
        expansion_cap = policy.escalation_task_cap
    return DecisionResult(
        outcome=outcome,
        final_manifest_hash=plan.manifest_hash,
        task_count=len(values),
        child_only_wins=child_only,
        parent_only_wins=parent_only,
        ties_both_pass=both_pass,
        ties_both_fail=both_fail,
        mean_delta=sum(deltas) / len(deltas),
        confidence_interval=(lower, upper),
        exact_mcnemar_p_value=exact_mcnemar_p_value(parent_only, child_only),
        audit_delta=audit_delta,
        audit_guard_passed=audit_guard_passed,
        rationale=rationale,
        expansion_task_cap=expansion_cap,
    )
