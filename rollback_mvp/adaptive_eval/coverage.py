"""Exact facility-location coverage and report-only redundancy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .schemas import ValidationError


VectorMap = Mapping[str, Sequence[float]]


@dataclass(frozen=True, slots=True)
class RedundancyNeighbor:
    instance_id: str
    neighbor_id: str
    similarity: float


@dataclass(frozen=True, slots=True)
class RedundancyReport:
    value: float
    neighbors: tuple[RedundancyNeighbor, ...]


def _validate_ids(ids: Sequence[str], vectors: VectorMap, field: str) -> tuple[str, ...]:
    values = tuple(ids)
    if len(values) != len(set(values)):
        raise ValidationError(f"{field} contains duplicate task IDs")
    unknown = sorted(set(values) - set(vectors))
    if unknown:
        raise ValidationError(f"{field} contains unknown vector IDs: {unknown}")
    return values


def similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if not left or len(left) != len(right):
        raise ValidationError("Similarity vectors must have equal non-zero dimensions")
    value = sum(a * b for a, b in zip(left, right))
    return max(0.0, min(1.0, value))


def facility_location_coverage(
    selected_ids: Sequence[str], universe_ids: Sequence[str], vectors: VectorMap
) -> float:
    selected = _validate_ids(selected_ids, vectors, "selected_ids")
    universe = _validate_ids(universe_ids, vectors, "universe_ids")
    if not universe:
        raise ValidationError("Coverage universe cannot be empty")
    if not selected:
        return 0.0
    return sum(
        max(similarity(vectors[item], vectors[chosen]) for chosen in selected)
        for item in universe
    ) / len(universe)


def marginal_coverage(
    candidate_id: str,
    selected_ids: Sequence[str],
    universe_ids: Sequence[str],
    vectors: VectorMap,
) -> float:
    selected = _validate_ids(selected_ids, vectors, "selected_ids")
    universe = _validate_ids(universe_ids, vectors, "universe_ids")
    if candidate_id not in vectors:
        raise ValidationError(f"Unknown coverage candidate: {candidate_id}")
    if candidate_id in selected:
        raise ValidationError(f"Coverage candidate is already selected: {candidate_id}")
    if not universe:
        raise ValidationError("Coverage universe cannot be empty")
    total = 0.0
    for item in universe:
        previous = max(
            (similarity(vectors[item], vectors[chosen]) for chosen in selected),
            default=0.0,
        )
        candidate = similarity(vectors[item], vectors[candidate_id])
        total += max(0.0, candidate - previous)
    return total / len(universe)


def greedy_by_marginal_coverage(
    candidate_ids: Sequence[str],
    selected_ids: Sequence[str],
    universe_ids: Sequence[str],
    vectors: VectorMap,
    capacity: int,
) -> tuple[tuple[str, float], ...]:
    if capacity < 0:
        raise ValidationError("Coverage capacity cannot be negative")
    candidates = list(_validate_ids(candidate_ids, vectors, "candidate_ids"))
    selected = list(_validate_ids(selected_ids, vectors, "selected_ids"))
    if set(candidates) & set(selected):
        raise ValidationError("Coverage candidates overlap selected IDs")
    result: list[tuple[str, float]] = []
    while candidates and len(result) < capacity:
        gains = [
            (marginal_coverage(candidate, selected, universe_ids, vectors), candidate)
            for candidate in candidates
        ]
        gain, candidate = min(gains, key=lambda item: (-item[0], item[1]))
        result.append((candidate, gain))
        selected.append(candidate)
        candidates.remove(candidate)
    return tuple(result)


def redundancy(selected_ids: Sequence[str], vectors: VectorMap) -> RedundancyReport:
    selected = _validate_ids(selected_ids, vectors, "selected_ids")
    if len(selected) < 2:
        return RedundancyReport(value=0.0, neighbors=())
    neighbors: list[RedundancyNeighbor] = []
    for instance_id in selected:
        candidates = [
            (similarity(vectors[instance_id], vectors[other]), other)
            for other in selected
            if other != instance_id
        ]
        score, neighbor_id = min(candidates, key=lambda item: (-item[0], item[1]))
        neighbors.append(
            RedundancyNeighbor(
                instance_id=instance_id, neighbor_id=neighbor_id, similarity=score
            )
        )
    return RedundancyReport(
        value=sum(item.similarity for item in neighbors) / len(neighbors),
        neighbors=tuple(neighbors),
    )
