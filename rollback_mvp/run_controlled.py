"""Run the controlled delayed-failure rollback experiment.

The controlled cases inject a known latent defect into a version history.
Deepseek must diagnose the culprit edge and select the exact pre-defect
ancestor from current error/debug evidence.

Usage:
  python3 run_controlled.py --offline
  python3 run_controlled.py
  python3 run_controlled.py --llm-repeats 5
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import random

from config import OUTPUT_DIR
from controlled_experiment import (
    ControlledCase,
    ControlledDecision,
    highest_score_decider,
    judge_controlled,
    llm_controlled_decider,
    load_controlled_cases,
    previous_version_decider,
    random_controlled_decider,
)
from llm_client import LLMClient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="run baselines only")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--llm-repeats", type=int, default=5)
    parser.add_argument(
        "--condition",
        choices=("both", "full", "no-debug"),
        default="both",
        help="which LLM evidence condition to run",
    )
    args = parser.parse_args()

    cases = load_controlled_cases()
    rng = random.Random(args.seed)
    results: list[ControlledDecision] = []

    for case in cases:
        results.extend(
            [
                judge_controlled(
                    case,
                    decider="rollback-1",
                    repeat=0,
                    choice=previous_version_decider(case),
                    culprit_edge="",
                    reason="immediate previous version",
                ),
                judge_controlled(
                    case,
                    decider="highest-score",
                    repeat=0,
                    choice=highest_score_decider(case),
                    culprit_edge="",
                    reason="highest-scoring ancestor",
                ),
                judge_controlled(
                    case,
                    decider="random",
                    repeat=0,
                    choice=random_controlled_decider(case, rng),
                    culprit_edge="",
                    reason="uniform random ancestor",
                ),
            ]
        )

    if not args.offline:
        client = LLMClient()
        conditions = (
            [("llm-no-debug", False), ("llm-full", True)]
            if args.condition == "both"
            else [(f"llm-{args.condition}", args.condition == "full")]
        )
        for decider, include_debug in conditions:
            for case_index, case in enumerate(cases, 1):
                print(
                    f"[{decider}] case {case_index}/{len(cases)}: {case.id}",
                    flush=True,
                )
                for repeat in range(1, args.llm_repeats + 1):
                    choice, edge, reason = llm_controlled_decider(
                        case,
                        client,
                        include_debug=include_debug,
                    )
                    results.append(
                        judge_controlled(
                            case,
                            decider=decider,
                            repeat=repeat,
                            choice=choice,
                            culprit_edge=edge,
                            reason=reason,
                        )
                    )

    _report(results, cases)
    filename = (
        "results_controlled_baselines.jsonl"
        if args.offline
        else "results_controlled.jsonl"
    )
    _save(results, filename)


def _report(results: list[ControlledDecision], cases: list[ControlledCase]) -> None:
    print("\n=== VOTE-LEVEL / BASELINE DECISIONS ===")
    print(
        f"{'decider':<16}{'n':>5}{'exact':>9}{'clears':>9}"
        f"{'distance':>11}{'under':>9}{'attr':>9}"
    )
    for decider in _ordered_deciders(results):
        summary = _summarize([row for row in results if row.decider == decider])
        print(
            f"{decider:<16}{summary['n']:>5}"
            f"{summary['exact_rate']:>9.3f}"
            f"{summary['clear_rate']:>9.3f}"
            f"{summary['mean_distance']:>11.3f}"
            f"{summary['under_rate']:>9.3f}"
            f"{summary['attribution_rate']:>9.3f}"
        )

    llm_deciders = [
        decider
        for decider in _ordered_deciders(results)
        if decider.startswith("llm-")
    ]
    if llm_deciders:
        print("\n=== CASE-LEVEL PLURALITY (ties are abstentions) ===")
        print(
            f"{'decider':<16}{'cases':>7}{'exact':>9}{'clears':>9}"
            f"{'distance':>11}{'ties':>7}"
        )
        for decider in llm_deciders:
            aggregate = _plurality_summary(
                [row for row in results if row.decider == decider],
                cases,
            )
            print(
                f"{decider:<16}{aggregate['n_cases']:>7}"
                f"{aggregate['exact_rate']:>9.3f}"
                f"{aggregate['clear_rate']:>9.3f}"
                f"{aggregate['mean_distance']:>11.3f}"
                f"{aggregate['ties']:>7}"
            )


def _ordered_deciders(results: list[ControlledDecision]) -> list[str]:
    order = {
        "rollback-1": 0,
        "highest-score": 1,
        "random": 2,
        "llm-no-debug": 3,
        "llm-full": 4,
    }
    return sorted({row.decider for row in results}, key=lambda name: order.get(name, 99))


def _summarize(rows: list[ControlledDecision]) -> dict[str, float]:
    n = len(rows)
    return {
        "n": n,
        "exact_rate": sum(row.exact for row in rows) / n,
        "clear_rate": sum(row.clears_toxicity for row in rows) / n,
        "mean_distance": sum(row.distance for row in rows) / n,
        "under_rate": sum(row.under_rollback > 0 for row in rows) / n,
        "attribution_rate": sum(row.attribution_hit for row in rows) / n,
    }


def _plurality_summary(
    rows: list[ControlledDecision],
    cases: list[ControlledCase],
) -> dict[str, float]:
    by_case: dict[str, list[ControlledDecision]] = collections.defaultdict(list)
    for row in rows:
        by_case[row.case_id].append(row)

    exact = 0
    clears = 0
    ties = 0
    distances: list[int] = []
    for case in cases:
        votes = collections.Counter(row.choice for row in by_case[case.id])
        top_count = max(votes.values())
        winners = [choice for choice, count in votes.items() if count == top_count]
        if len(winners) != 1:
            ties += 1
            continue
        winner = winners[0]
        representative = next(row for row in by_case[case.id] if row.choice == winner)
        exact += representative.exact
        clears += representative.clears_toxicity
        distances.append(representative.distance)

    n_cases = len(cases)
    return {
        "n_cases": n_cases,
        "exact_rate": exact / n_cases,
        "clear_rate": clears / n_cases,
        "mean_distance": (
            sum(distances) / len(distances) if distances else float("nan")
        ),
        "ties": ties,
    }


def _save(results: list[ControlledDecision], filename: str) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w") as f:
        for row in results:
            f.write(json.dumps(row.__dict__, ensure_ascii=False) + "\n")
    print(f"\nSaved {len(results)} decisions to {path}")


if __name__ == "__main__":
    main()
