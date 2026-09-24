"""Multi-fidelity promotion replay over fully observed DGM SWE candidates.

All eight candidates in this benchmark have 197-200 released task outcomes.
We hide outcomes behind 10/60/200 panels and compare promotion schedules. This
tests evaluation allocation only; it does not estimate counterfactual agent
generation or CLM rollback quality.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import statistics
from dataclasses import asdict, dataclass

from config import OUTPUT_DIR
from evo_tree import EvoNode, EvoTree


@dataclass(frozen=True)
class TrialResult:
    method: str
    selected_ids: tuple[str, ...]
    best_selected_score: float
    contains_global_best: bool
    task_evaluations: int
    promoted_after_10: int
    promoted_after_60: int


METHODS = (
    "uniform-full",
    "dgm-threshold-top2",
    "successive-4-2",
    "risk-limiting-5-2",
    "stability-gated-6",
    "top1-after-60",
)
PRIMARY_METHOD = "stability-gated-6"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260924)
    parser.add_argument(
        "--output",
        default=os.path.join(OUTPUT_DIR, "dgm_multifidelity_race.json"),
    )
    args = parser.parse_args()

    tree = EvoTree.load()
    arms, small_tasks, medium_tasks, big_tasks = load_fully_observed_problem(tree)
    canonical_tasks = (*small_tasks, *medium_tasks, *big_tasks)
    global_best = max(arms, key=lambda node: score(node, canonical_tasks))

    official_order = (
        *hash_order(small_tasks, args.seed, "official-small"),
        *hash_order(medium_tasks, args.seed, "official-medium"),
        *hash_order(big_tasks, args.seed, "official-big"),
    )
    official = {
        method: asdict(
            run_trial(
                arms,
                official_order,
                global_best.id,
                method,
                tie_seed=args.seed,
            )
        )
        for method in METHODS
    }

    rows = {method: [] for method in METHODS}
    for trial in range(args.trials):
        task_order = hash_order(
            canonical_tasks,
            args.seed + trial,
            "rotated",
        )
        for method in METHODS:
            rows[method].append(
                run_trial(
                    arms,
                    task_order,
                    global_best.id,
                    method,
                    tie_seed=args.seed + trial,
                )
            )
    summary = {
        method: summarize(trials)
        for method, trials in rows.items()
    }
    dgm_cost = summary["dgm-threshold-top2"]["mean_task_evaluations"]
    for row in summary.values():
        row["cost_saving_vs_dgm"] = round(
            1.0 - row["mean_task_evaluations"] / dgm_cost,
            4,
        )

    primary = summary[PRIMARY_METHOD]
    result = {
        "schema_version": 1,
        "scope": (
            "Fully observed eight-candidate promotion replay. Hash rotations "
            "are sensitivity trials, not independent agent-generation runs."
        ),
        "task_panels": {
            "small": len(small_tasks),
            "medium": len(medium_tasks),
            "big": len(big_tasks),
            "total": len(canonical_tasks),
        },
        "candidate_count": len(arms),
        "global_best": {
            "node_id": global_best.id,
            "score": score(global_best, canonical_tasks),
        },
        "preregistration": {
            "hypothesis": (
                "Stability-gated promotion contains the global-best candidate "
                "in at least 95% of hash-rotated trials and uses at least 20% "
                "fewer task evaluations than documented DGM staging."
            ),
            "kill_criterion": (
                "Kill if hit rate is below 0.95 or mean task-evaluation saving "
                "versus DGM staging is below 0.20."
            ),
            "primary_method": PRIMARY_METHOD,
        },
        "official_split": official,
        "rotated_trials": {
            "count": args.trials,
            "seed": args.seed,
            "summary": summary,
        },
        "verdict": {
            "passed": (
                primary["global_best_hit_rate"] >= 0.95
                and primary["cost_saving_vs_dgm"] >= 0.20
            ),
            "accuracy_passed": primary["global_best_hit_rate"] >= 0.95,
            "cost_passed": primary["cost_saving_vs_dgm"] >= 0.20,
        },
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w") as file:
        json.dump(result, file, indent=2)
        file.write("\n")
    print_report(result)
    print(f"\nSaved result to {args.output}")


def load_fully_observed_problem(
    tree: EvoTree,
) -> tuple[list[EvoNode], tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    arms = sorted(
        (
            node
            for node in tree.nodes.values()
            if node.scored and len(node.submitted) >= 190
        ),
        key=lambda node: node.id,
    )
    if not arms:
        raise ValueError("No fully observed DGM candidates found.")
    full_tasks = set.union(*(node.submitted for node in arms))
    ten_task_sets = [
        node.submitted
        for node in tree.nodes.values()
        if node.scored and len(node.submitted) == 10
    ]
    small_tasks = set.intersection(*ten_task_sets)
    medium_tasks = tree.nodes["initial"].submitted - small_tasks
    big_tasks = full_tasks - small_tasks - medium_tasks
    if (len(small_tasks), len(medium_tasks), len(big_tasks)) != (10, 50, 140):
        raise ValueError("Released DGM task panels are not 10/50/140.")
    return (
        arms,
        tuple(sorted(small_tasks)),
        tuple(sorted(medium_tasks)),
        tuple(sorted(big_tasks)),
    )


def run_trial(
    arms: list[EvoNode],
    task_order: tuple[str, ...],
    global_best_id: str,
    method: str,
    *,
    tie_seed: int,
) -> TrialResult:
    if len(task_order) != 200:
        raise ValueError("Expected exactly 200 tasks.")
    if method == "uniform-full":
        finalists = arms
        after_10 = len(arms)
        after_60 = len(arms)
    else:
        ranked_10 = rank(arms, task_order[:10], tie_seed)
        if method == "dgm-threshold-top2":
            promoted = [
                node for node in ranked_10 if score(node, task_order[:10]) >= 0.4
            ]
            if not promoted:
                promoted = ranked_10[:1]
        elif method == "successive-4-2":
            promoted = ranked_10[:4]
        elif method == "risk-limiting-5-2":
            promoted = ranked_10[:5]
        elif method in ("stability-gated-6", "top1-after-60"):
            promoted = ranked_10[:6]
        else:
            raise ValueError(f"Unknown method: {method}")

        ranked_60 = rank(promoted, task_order[:60], tie_seed)
        if method == "top1-after-60":
            finalists = ranked_60[:1]
        elif method == "stability-gated-6":
            leader_30 = rank(promoted, task_order[:30], tie_seed)[0]
            finalist_count = 1 if leader_30.id == ranked_60[0].id else 2
            finalists = ranked_60[:finalist_count]
        else:
            finalists = ranked_60[:2]
        after_10 = len(promoted)
        after_60 = len(finalists)

    selected = rank(finalists, task_order, tie_seed)[0]
    task_evaluations = (
        len(arms) * 10
        + after_10 * 50
        + after_60 * 140
        if method != "uniform-full"
        else len(arms) * 200
    )
    return TrialResult(
        method=method,
        selected_ids=tuple(node.id for node in finalists),
        best_selected_score=round(score(selected, task_order), 4),
        contains_global_best=global_best_id in {node.id for node in finalists},
        task_evaluations=task_evaluations,
        promoted_after_10=after_10,
        promoted_after_60=after_60,
    )


def rank(
    arms: list[EvoNode],
    tasks: tuple[str, ...],
    tie_seed: int,
) -> list[EvoNode]:
    return sorted(
        arms,
        key=lambda node: (
            -score(node, tasks),
            hashlib.sha256(f"{tie_seed}|{node.id}".encode()).hexdigest(),
        ),
    )


def score(node: EvoNode, tasks: tuple[str, ...]) -> float:
    return sum(task in node.resolved for task in tasks) / len(tasks)


def hash_order(
    tasks: tuple[str, ...],
    seed: int,
    namespace: str,
) -> tuple[str, ...]:
    return tuple(
        sorted(
            tasks,
            key=lambda task: hashlib.sha256(
                f"{namespace}|{seed}|{task}".encode()
            ).hexdigest(),
        )
    )


def summarize(trials: list[TrialResult]) -> dict:
    return {
        "global_best_hit_rate": round(
            statistics.mean(trial.contains_global_best for trial in trials),
            4,
        ),
        "mean_selected_score": round(
            statistics.mean(trial.best_selected_score for trial in trials),
            4,
        ),
        "mean_task_evaluations": round(
            statistics.mean(trial.task_evaluations for trial in trials),
            4,
        ),
        "mean_promoted_after_10": round(
            statistics.mean(trial.promoted_after_10 for trial in trials),
            4,
        ),
        "mean_promoted_after_60": round(
            statistics.mean(trial.promoted_after_60 for trial in trials),
            4,
        ),
    }


def print_report(result: dict) -> None:
    print("=== DGM MULTI-FIDELITY PROMOTION REPLAY ===")
    print(
        f"candidates={result['candidate_count']} "
        f"global_best={result['global_best']['score']:.4f}"
    )
    print("\nOfficial 10/50/140 split:")
    for method, row in result["official_split"].items():
        print(
            f"  {method:<24} best={row['best_selected_score']:.4f} "
            f"cost={row['task_evaluations']} "
            f"contains_best={row['contains_global_best']}"
        )
    print("\nHash-rotated sensitivity:")
    for method, row in result["rotated_trials"]["summary"].items():
        print(
            f"  {method:<24} hit={row['global_best_hit_rate']:.4f} "
            f"score={row['mean_selected_score']:.4f} "
            f"cost={row['mean_task_evaluations']:.1f} "
            f"save_vs_dgm={row['cost_saving_vs_dgm']:.2%}"
        )
    print(
        "\nPrimary verdict="
        f"{'PASS' if result['verdict']['passed'] else 'KILL'}"
    )


if __name__ == "__main__":
    main()
