"""Repair-first causal lineage minimization for artifact mutation lineages."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence, TypeVar

from .artifacts import MutationDelta


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class SkippedMutation:
    mutation_id: str
    reason: str


@dataclass(frozen=True, slots=True)
class RepairPlan:
    rollback_before_mutation: str
    removed_mutation_ids: tuple[str, ...]
    replay_mutation_ids: tuple[str, ...]
    skipped_mutations: tuple[SkippedMutation, ...]


@dataclass(frozen=True, slots=True)
class RepairResult:
    method: str
    removed_mutation_ids: tuple[str, ...]
    plan: RepairPlan | None
    probe_count: int
    abstain_reason: str | None


def ddmin_removals(
    items: Sequence[T],
    repairs: Callable[[tuple[T, ...]], bool],
) -> tuple[T, ...]:
    current = tuple(items)
    if not current or not repairs(current):
        return ()
    granularity = 2
    while len(current) >= 2:
        chunks = _partition(current, granularity)
        reduced = False
        for chunk in chunks:
            if repairs(chunk):
                current = chunk
                granularity = max(granularity - 1, 2)
                reduced = True
                break
        if reduced:
            continue
        for chunk in chunks:
            removed = set(chunk)
            complement = tuple(item for item in current if item not in removed)
            if complement and repairs(complement):
                current = complement
                granularity = max(granularity - 1, 2)
                reduced = True
                break
        if reduced:
            continue
        if granularity >= len(current):
            break
        granularity = min(len(current), granularity * 2)

    index = 0
    while index < len(current):
        candidate = current[:index] + current[index + 1 :]
        if candidate and repairs(candidate):
            current = candidate
        else:
            index += 1
    return current


def repair_first_lineage(
    lineage: Sequence[MutationDelta],
    *,
    fails_with_active: Callable[[tuple[str, ...]], bool],
    prior_order: Sequence[str] = (),
    singleton_budget: int = 1,
) -> RepairResult:
    if not lineage:
        return RepairResult(
            method="abstain",
            removed_mutation_ids=(),
            plan=None,
            probe_count=0,
            abstain_reason="No changed mutation exists after the rollback baseline.",
        )
    mutation_ids = tuple(delta.mutation_id for delta in lineage)
    if len(mutation_ids) != len(set(mutation_ids)):
        raise ValueError("RF-CLM lineage contains duplicate mutation IDs")
    known = set(mutation_ids)
    ordered = tuple(
        dict.fromkeys(
            [
                *(item for item in prior_order if item in known),
                *reversed(mutation_ids),
            ]
        )
    )
    probe_cache: dict[tuple[str, ...], bool] = {}

    def probe(active: tuple[str, ...]) -> bool:
        normalized = tuple(item for item in mutation_ids if item in set(active))
        if normalized not in probe_cache:
            probe_cache[normalized] = fails_with_active(normalized)
        return probe_cache[normalized]

    if not probe(mutation_ids):
        return RepairResult(
            method="abstain",
            removed_mutation_ids=(),
            plan=None,
            probe_count=len(probe_cache),
            abstain_reason="The full mutation lineage does not reproduce the failure.",
        )
    if probe(()):
        return RepairResult(
            method="abstain",
            removed_mutation_ids=(),
            plan=None,
            probe_count=len(probe_cache),
            abstain_reason="The failure reproduces at the rollback baseline.",
        )

    def repairs(removed: tuple[str, ...]) -> bool:
        removed_set = set(removed)
        active = tuple(item for item in mutation_ids if item not in removed_set)
        return not probe(active)

    removed: tuple[str, ...] = ()
    method = "full-repair-ddmin"
    for mutation_id in ordered[:singleton_budget]:
        if repairs((mutation_id,)):
            removed = (mutation_id,)
            method = "singleton-removal"
            break
    if not removed:
        removed = ddmin_removals(ordered, repairs)
    if not removed or not repairs(removed):
        return RepairResult(
            method="abstain",
            removed_mutation_ids=removed,
            plan=None,
            probe_count=len(probe_cache),
            abstain_reason="No sufficient mutation-removal set was verified.",
        )

    plan = build_repair_plan(lineage, removed)
    active_after_replay = tuple(
        mutation_id
        for mutation_id in mutation_ids
        if mutation_id in set(plan.replay_mutation_ids)
        or mutation_ids.index(mutation_id)
        < mutation_ids.index(plan.rollback_before_mutation)
    )
    if probe(active_after_replay):
        return RepairResult(
            method="abstain",
            removed_mutation_ids=removed,
            plan=None,
            probe_count=len(probe_cache),
            abstain_reason=(
                "The dependency-safe rollback-and-replay plan did not repair "
                "the failure."
            ),
        )
    return RepairResult(
        method=method,
        removed_mutation_ids=removed,
        plan=plan,
        probe_count=len(probe_cache),
        abstain_reason=None,
    )


def build_repair_plan(
    lineage: Sequence[MutationDelta],
    removed_mutation_ids: Sequence[str],
) -> RepairPlan:
    removed = set(removed_mutation_ids)
    earliest = next(
        (
            index
            for index, delta in enumerate(lineage)
            if delta.mutation_id in removed
        ),
        -1,
    )
    if earliest < 0:
        raise ValueError("A repair plan requires a mutation in the lineage")
    blocked_ids = set(removed)
    blocked_paths = {
        path
        for delta in lineage
        if delta.mutation_id in removed
        for path in delta.changed_paths
    }
    replay: list[str] = []
    skipped: list[SkippedMutation] = []
    for delta in lineage[earliest:]:
        if delta.mutation_id in removed:
            skipped.append(SkippedMutation(delta.mutation_id, "causal"))
            continue
        if any(dependency in blocked_ids for dependency in delta.depends_on):
            skipped.append(SkippedMutation(delta.mutation_id, "dependency"))
            blocked_ids.add(delta.mutation_id)
            blocked_paths.update(delta.changed_paths)
            continue
        if any(path in blocked_paths for path in delta.changed_paths):
            skipped.append(SkippedMutation(delta.mutation_id, "overlapping-path"))
            blocked_ids.add(delta.mutation_id)
            blocked_paths.update(delta.changed_paths)
            continue
        replay.append(delta.mutation_id)
    return RepairPlan(
        rollback_before_mutation=lineage[earliest].mutation_id,
        removed_mutation_ids=tuple(
            delta.mutation_id
            for delta in lineage
            if delta.mutation_id in removed
        ),
        replay_mutation_ids=tuple(replay),
        skipped_mutations=tuple(skipped),
    )


def apply_repair_plan(
    baseline: Sequence[MutationDelta],
    segment: Sequence[MutationDelta],
    plan: RepairPlan,
) -> tuple[MutationDelta, ...]:
    rollback_index = next(
        index
        for index, delta in enumerate(segment)
        if delta.mutation_id == plan.rollback_before_mutation
    )
    replay = set(plan.replay_mutation_ids)
    return (
        *baseline,
        *segment[:rollback_index],
        *(
            delta
            for delta in segment[rollback_index:]
            if delta.mutation_id in replay
        ),
    )


def _partition(items: Sequence[T], count: int) -> tuple[tuple[T, ...], ...]:
    size = (len(items) + count - 1) // count
    return tuple(
        tuple(items[start : start + size])
        for start in range(0, len(items), size)
    )
