"""Algorithms for low-cost causal localization over version lineages.

This module isolates the algorithmic core from Pi and SWE-bench execution. A
lineage is represented as an ordered set of patches. The replay oracle answers
whether a selected subset still reproduces the failure. Synthetic cases use a
hidden conjunctive cause set, so every causal patch is required for failure.

The intended production mapping is:
  active patch subset -> reconstruct harness -> run the failing task/probe
  True                -> failure reproduced
  False               -> failure removed
"""

from __future__ import annotations

import hashlib
import math
import random
from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class SyntheticLineage:
    case_id: int
    n_edges: int
    cause_set: frozenset[int]
    candidate_slice: tuple[int, ...]
    prior_order: tuple[int, ...]
    noise_rate: float
    cause_families: tuple[frozenset[int], ...] = ()

    @property
    def all_edges(self) -> tuple[int, ...]:
        return tuple(range(self.n_edges))

    def fails(self, active_edges: Iterable[int]) -> bool:
        active = set(active_edges)
        families = self.cause_families or (self.cause_set,)
        return any(family.issubset(active) for family in families)


@dataclass(frozen=True)
class Diagnosis:
    method: str
    predicted_set: tuple[int, ...]
    probe_calls: int
    probe_cost: float
    used_fallback: bool = False


class ReplayOracle:
    """Deterministic common-random-number wrapper around a noisy replay."""

    def __init__(self, case: SyntheticLineage, repeats: int):
        if repeats < 1 or repeats % 2 == 0:
            raise ValueError("repeats must be a positive odd number")
        self.case = case
        self.repeats = repeats
        self.probe_calls = 0
        self.probe_cost = 0.0
        self._cache: dict[tuple[int, ...], bool] = {}

    def __call__(self, active_edges: Iterable[int]) -> bool:
        key = tuple(sorted(active_edges))
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        truth = self.case.fails(key)
        votes = 0
        for repeat in range(self.repeats):
            observed = truth
            if _uniform(self.case.case_id, key, repeat) < self.case.noise_rate:
                observed = not observed
            votes += int(observed)
            self.probe_calls += 1
            # Reconstructing a larger patch set is slightly more expensive.
            self.probe_cost += 1.0 + 0.02 * len(key)
        result = votes > self.repeats // 2
        self._cache[key] = result
        return result


def rollback_one(case: SyntheticLineage) -> Diagnosis:
    return Diagnosis("rollback-1", (case.n_edges - 1,), 0, 0.0)


def linear_prefix(case: SyntheticLineage, repeats: int) -> Diagnosis:
    oracle = ReplayOracle(case, repeats)
    first_bad = case.n_edges - 1
    for prefix_size in range(1, case.n_edges + 1):
        if oracle(range(prefix_size)):
            first_bad = prefix_size - 1
            break
    return Diagnosis(
        "linear-prefix",
        (first_bad,),
        oracle.probe_calls,
        oracle.probe_cost,
    )


def binary_prefix(case: SyntheticLineage, repeats: int) -> Diagnosis:
    """Find the first failing prefix, assuming a monotone prefix predicate."""
    oracle = ReplayOracle(case, repeats)
    low = 0  # empty prefix is known good
    high = case.n_edges  # full prefix is known bad
    while high - low > 1:
        middle = (low + high) // 2
        if oracle(range(middle)):
            high = middle
        else:
            low = middle
    return Diagnosis(
        "binary-prefix",
        (high - 1,),
        oracle.probe_calls,
        oracle.probe_cost,
    )


def full_ddmin(case: SyntheticLineage, repeats: int) -> Diagnosis:
    oracle = ReplayOracle(case, repeats)
    result = ddmin(case.prior_order, oracle)
    return Diagnosis(
        "full-ddmin",
        result,
        oracle.probe_calls,
        oracle.probe_cost,
    )


def full_repair_ddmin(case: SyntheticLineage, repeats: int) -> Diagnosis:
    """Minimize the removed patch set needed to clear the failure."""
    oracle = ReplayOracle(case, repeats)
    all_edges = set(case.all_edges)

    def repairs(removed: Iterable[int]) -> bool:
        return not oracle(all_edges - set(removed))

    result = ddmin(case.prior_order, repairs)
    return Diagnosis(
        "full-repair-ddmin",
        result,
        oracle.probe_calls,
        oracle.probe_cost,
    )


def sliced_ddmin(case: SyntheticLineage, repeats: int) -> Diagnosis:
    """Run ddmin on the dependency slice, expanding safely if it misses a cause."""
    oracle = ReplayOracle(case, repeats)
    candidate = case.candidate_slice
    used_fallback = not oracle(candidate)
    if used_fallback:
        candidate = case.prior_order
    result = ddmin(candidate, oracle)
    return Diagnosis(
        "sliced-ddmin",
        result,
        oracle.probe_calls,
        oracle.probe_cost,
        used_fallback=used_fallback,
    )


def active_sliced_ddmin(
    case: SyntheticLineage,
    repeats: int,
    singleton_budget: int = 1,
) -> Diagnosis:
    """Probe high-prior singleton causes, then fall back to sliced ddmin."""
    oracle = ReplayOracle(case, repeats)
    candidate = case.candidate_slice
    used_fallback = not oracle(candidate)
    if used_fallback:
        candidate = case.prior_order

    for edge in candidate[:singleton_budget]:
        if oracle((edge,)):
            return Diagnosis(
                "active-sliced-ddmin",
                (edge,),
                oracle.probe_calls,
                oracle.probe_cost,
                used_fallback=used_fallback,
            )

    result = ddmin(candidate, oracle)
    return Diagnosis(
        "active-sliced-ddmin",
        result,
        oracle.probe_calls,
        oracle.probe_cost,
        used_fallback=used_fallback,
    )


def repair_first_ddmin(
    case: SyntheticLineage,
    repeats: int,
    singleton_budget: int = 1,
) -> Diagnosis:
    """Find a one-minimal repair directly instead of reconstructing all causes."""
    oracle = ReplayOracle(case, repeats)
    all_edges = set(case.all_edges)

    def repairs(removed: Iterable[int]) -> bool:
        return not oracle(all_edges - set(removed))

    candidate = case.candidate_slice
    used_fallback = not repairs(candidate)
    if used_fallback:
        candidate = case.prior_order

    for edge in candidate[:singleton_budget]:
        if repairs((edge,)):
            return Diagnosis(
                "repair-first-ddmin",
                (edge,),
                oracle.probe_calls,
                oracle.probe_cost,
                used_fallback=used_fallback,
            )

    result = ddmin(candidate, repairs)
    return Diagnosis(
        "repair-first-ddmin",
        result,
        oracle.probe_calls,
        oracle.probe_cost,
        used_fallback=used_fallback,
    )


def failure_first_repair(
    case: SyntheticLineage,
    repeats: int,
) -> Diagnosis:
    """Reproduce the previous plugin strategy for repair-cost comparison."""
    oracle = ReplayOracle(case, repeats)
    all_edges = set(case.all_edges)
    candidate = case.candidate_slice
    used_fallback = not oracle(candidate)
    if used_fallback:
        candidate = case.prior_order

    failure_core = ddmin(candidate, oracle)
    if not failure_core:
        return Diagnosis(
            "failure-first-repair",
            (),
            oracle.probe_calls,
            oracle.probe_cost,
            used_fallback=used_fallback,
        )

    removed = [min(failure_core)]
    if oracle(all_edges - set(removed)):
        remaining = [edge for edge in case.prior_order if edge not in removed]

        def repairs(additional: Iterable[int]) -> bool:
            return not oracle(all_edges - set(removed) - set(additional))

        removed.extend(ddmin(remaining, repairs))
    return Diagnosis(
        "failure-first-repair",
        tuple(sorted(set(removed))),
        oracle.probe_calls,
        oracle.probe_cost,
        used_fallback=used_fallback,
    )


def ddmin(
    items: Iterable[int],
    reproduces_failure: Callable[[Iterable[int]], bool],
) -> tuple[int, ...]:
    """Return a one-minimal failure-inducing subset."""
    current = list(items)
    if not current or not reproduces_failure(current):
        return ()

    granularity = 2
    while len(current) >= 2:
        chunks = _partition(current, granularity)
        reduced = False

        for chunk in chunks:
            if reproduces_failure(chunk):
                current = chunk
                granularity = max(granularity - 1, 2)
                reduced = True
                break
        if reduced:
            continue

        for chunk in chunks:
            removed = set(chunk)
            complement = [item for item in current if item not in removed]
            if complement and reproduces_failure(complement):
                current = complement
                granularity = max(granularity - 1, 2)
                reduced = True
                break
        if reduced:
            continue

        if granularity >= len(current):
            break
        granularity = min(len(current), granularity * 2)

    # Verification sweep guarantees one-minimality when the oracle is stable.
    index = 0
    while index < len(current):
        candidate = current[:index] + current[index + 1 :]
        if candidate and reproduces_failure(candidate):
            current = candidate
        else:
            index += 1
    return tuple(sorted(current))


def generate_cases(
    *,
    seed: int,
    cases_per_size: int,
    sizes: tuple[int, ...],
    noise_rate: float,
    slice_fraction: float,
    slice_recall: float,
    prior_strength: float,
) -> list[SyntheticLineage]:
    rng = random.Random(seed)
    cases: list[SyntheticLineage] = []
    case_id = seed * 1_000_000
    for n_edges in sizes:
        for _ in range(cases_per_size):
            case_id += 1
            cause_size = rng.choices((1, 2, 3), weights=(0.5, 0.35, 0.15))[0]
            cause_set = frozenset(rng.sample(range(n_edges), cause_size))

            scores = {
                edge: rng.random() + (prior_strength if edge in cause_set else 0.0)
                for edge in range(n_edges)
            }
            prior_order = tuple(
                sorted(scores, key=lambda edge: scores[edge], reverse=True)
            )

            slice_size = max(cause_size, math.ceil(n_edges * slice_fraction))
            retained_causes = [
                edge for edge in cause_set if rng.random() <= slice_recall
            ]
            distractors = [
                edge for edge in prior_order if edge not in cause_set
            ][: max(0, slice_size - len(retained_causes))]
            candidate_slice = tuple(
                sorted(set(retained_causes + distractors), key=prior_order.index)
            )

            cases.append(
                SyntheticLineage(
                    case_id=case_id,
                    n_edges=n_edges,
                    cause_set=cause_set,
                    candidate_slice=candidate_slice,
                    prior_order=prior_order,
                    noise_rate=noise_rate,
                )
            )
    return cases


def generate_family_cases(
    *,
    seed: int,
    cases_per_size: int,
    sizes: tuple[int, ...],
    noise_rate: float,
    slice_fraction: float,
    slice_recall: float,
    prior_strength: float,
) -> list[SyntheticLineage]:
    rng = random.Random(seed)
    cases: list[SyntheticLineage] = []
    case_id = seed * 1_000_000
    patterns = ("conjunctive", "alternative", "mixed")
    for n_edges in sizes:
        for index in range(cases_per_size):
            case_id += 1
            pattern = patterns[index % len(patterns)]
            if pattern == "conjunctive":
                family = frozenset(rng.sample(range(n_edges), 3))
                families = (family,)
            elif pattern == "alternative":
                selected = rng.sample(range(n_edges), 3)
                families = tuple(frozenset({edge}) for edge in selected)
            else:
                selected = rng.sample(range(n_edges), 3)
                families = (
                    frozenset(selected[:2]),
                    frozenset({selected[2]}),
                )
            cause_set = frozenset().union(*families)
            scores = {
                edge: rng.random() + (prior_strength if edge in cause_set else 0.0)
                for edge in range(n_edges)
            }
            prior_order = tuple(
                sorted(scores, key=lambda edge: scores[edge], reverse=True)
            )
            slice_size = max(
                len(cause_set),
                math.ceil(n_edges * slice_fraction),
            )
            retained_causes = [
                edge for edge in cause_set if rng.random() <= slice_recall
            ]
            distractors = [
                edge for edge in prior_order if edge not in cause_set
            ][: max(0, slice_size - len(retained_causes))]
            candidate_slice = tuple(
                sorted(
                    set(retained_causes + distractors),
                    key=prior_order.index,
                )
            )
            cases.append(
                SyntheticLineage(
                    case_id=case_id,
                    n_edges=n_edges,
                    cause_set=cause_set,
                    candidate_slice=candidate_slice,
                    prior_order=prior_order,
                    noise_rate=noise_rate,
                    cause_families=families,
                )
            )
    return cases


def _partition(items: list[int], count: int) -> list[list[int]]:
    size = math.ceil(len(items) / count)
    return [items[start : start + size] for start in range(0, len(items), size)]


def _uniform(case_id: int, active: tuple[int, ...], repeat: int) -> float:
    payload = f"{case_id}|{active}|{repeat}".encode()
    digest = hashlib.sha256(payload).digest()
    return int.from_bytes(digest[:8], "big") / 2**64
