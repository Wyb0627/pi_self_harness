"""Logged-candidate replay for branch-quarantine policies on DGM releases.

The replay asks a narrow question: if DGM's already generated candidates were
offered in the same chronological order, could a policy stop evaluating
descendants of directly observed regression-only patches without losing the
best released endpoint?

This is not an off-policy estimate of end-to-end evolution. A different parent
policy would generate different children, which are absent from the release.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass

from config import DGM_SWE_ROOT, OUTPUT_DIR
from evo_tree import EvoNode, EvoTree


@dataclass(frozen=True)
class Attempt:
    generation: int
    child_id: str


@dataclass(frozen=True)
class EdgeDelta:
    common_tasks: int
    gained: int
    lost: int


@dataclass(frozen=True)
class QuarantineRule:
    name: str
    min_lost: int
    max_gained: int | None = None
    min_net_loss: int | None = None

    def matches(self, delta: EdgeDelta) -> bool:
        if delta.common_tasks == 0 or delta.lost < self.min_lost:
            return False
        if self.max_gained is not None and delta.gained > self.max_gained:
            return False
        if self.min_net_loss is not None:
            return delta.lost - delta.gained >= self.min_net_loss
        return True


RULES = (
    QuarantineRule("no-new-gain-1", min_lost=1, max_gained=0),
    QuarantineRule("confirmed-no-new-gain", min_lost=2, max_gained=0),
    QuarantineRule("net-loss-2", min_lost=2, min_net_loss=2),
)
PRIMARY_RULE = "confirmed-no-new-gain"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--proposal-task-equivalents",
        type=float,
        default=1.0,
        help="Cost assigned to generating one candidate before task evaluation.",
    )
    parser.add_argument(
        "--output",
        default=os.path.join(OUTPUT_DIR, "dgm_budgeted_quarantine.json"),
    )
    args = parser.parse_args()

    roots = {
        "dgm": DGM_SWE_ROOT,
        "no-open-ended": os.path.join(
            os.path.dirname(DGM_SWE_ROOT),
            "swe_dgm_nodarwin",
        ),
        "no-self-improve": os.path.join(
            os.path.dirname(DGM_SWE_ROOT),
            "swe_dgm_noselfimprove",
        ),
    }
    runs = {
        name: evaluate_run(root, args.proposal_task_equivalents)
        for name, root in roots.items()
    }
    primary_rows = [
        run["policies"][PRIMARY_RULE]
        for run in runs.values()
    ]
    result = {
        "schema_version": 1,
        "scope": (
            "Chronological logged-candidate replay. It can measure whether a "
            "quarantine rule would have skipped released descendants, but not "
            "which counterfactual children another evolution policy would generate."
        ),
        "cost_model": {
            "task_evaluation": 1.0,
            "candidate_proposal": args.proposal_task_equivalents,
            "note": "The proposal weight is a conservative task-equivalent proxy.",
        },
        "preregistration": {
            "hypothesis": (
                "The primary confirmed-no-new-gain rule preserves each run's "
                "best fixed-D60 endpoint, improves normalized quality-cost AUC, "
                "and saves at least 20% of total task-equivalent cost."
            ),
            "kill_criterion": (
                "Kill if any released run loses its best endpoint, fails to "
                "improve AUC, or saves less than 20% cost."
            ),
            "primary_rule": PRIMARY_RULE,
        },
        "runs": runs,
        "verdict": {
            "passed": all(
                row["best_preserved"]
                and row["auc_improvement"] > 0
                and row["cost_saving_fraction"] >= 0.20
                for row in primary_rows
            ),
            "primary_rule": PRIMARY_RULE,
            "runs_passing": sum(
                row["best_preserved"]
                and row["auc_improvement"] > 0
                and row["cost_saving_fraction"] >= 0.20
                for row in primary_rows
            ),
            "runs_total": len(primary_rows),
        },
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w") as file:
        json.dump(result, file, indent=2)
        file.write("\n")
    print_report(result)
    print(f"\nSaved result to {args.output}")


def evaluate_run(root: str, proposal_cost: float) -> dict:
    tree = EvoTree.load(root)
    attempts = load_attempts(os.path.join(root, "dgm_metadata.jsonl"))
    initial = tree.nodes["initial"]
    canonical_tasks = set(initial.submitted)
    baseline = replay(
        tree,
        attempts,
        canonical_tasks,
        proposal_cost=proposal_cost,
        rule=None,
        comparison_budget=None,
    )
    policies = {
        rule.name: replay(
            tree,
            attempts,
            canonical_tasks,
            proposal_cost=proposal_cost,
            rule=rule,
            comparison_budget=baseline["total_cost"],
        )
        for rule in RULES
    }
    for row in policies.values():
        row["best_preserved"] = (
            row["best_fixed_d60"] == baseline["best_fixed_d60"]
        )
        row["cost_saving_fraction"] = round(
            1.0 - row["total_cost"] / baseline["total_cost"],
            4,
        )
        row["task_evaluation_saving_fraction"] = round(
            1.0 - row["task_evaluations"] / baseline["task_evaluations"],
            4,
        )
        row["auc_improvement"] = round(
            row["normalized_quality_cost_auc"]
            - baseline["normalized_quality_cost_auc"],
            6,
        )
    return {
        "root": root,
        "canonical_tasks": len(canonical_tasks),
        "attempts": len(attempts),
        "baseline": baseline,
        "policies": policies,
    }


def replay(
    tree: EvoTree,
    attempts: list[Attempt],
    canonical_tasks: set[str],
    *,
    proposal_cost: float,
    rule: QuarantineRule | None,
    comparison_budget: float | None,
) -> dict:
    available = {"initial"}
    evaluated = {"initial"}
    quarantined: list[dict] = []
    skipped: list[str] = []
    task_evaluations = 0
    proposal_attempts = 0
    total_cost = 0.0
    current_best = fixed_accuracy(tree.nodes["initial"], canonical_tasks)
    best_node = "initial"
    auc_area = 0.0

    for attempt in attempts:
        node = tree.nodes.get(attempt.child_id)
        if node is None:
            raise ValueError(f"Missing released node directory: {attempt.child_id}")
        if node.parent_id not in available:
            skipped.append(node.id)
            continue

        attempt_cost = proposal_cost
        proposal_attempts += 1
        if node.scored:
            attempt_cost += len(node.submitted)
            task_evaluations += len(node.submitted)
        auc_area += current_best * attempt_cost
        total_cost += attempt_cost

        if not node.scored:
            continue

        evaluated.add(node.id)
        quality = fixed_accuracy(node, canonical_tasks)
        if quality > current_best:
            current_best = quality
            best_node = node.id

        delta = paired_delta(tree.nodes[node.parent_id], node)
        if rule is not None and rule.matches(delta):
            quarantined.append(
                {
                    "node_id": node.id,
                    "parent_id": node.parent_id,
                    "generation": attempt.generation,
                    "delta": asdict(delta),
                }
            )
        else:
            available.add(node.id)

    budget = comparison_budget if comparison_budget is not None else total_cost
    if total_cost > budget + 1e-9:
        raise ValueError("Policy exceeded its comparison budget.")
    auc_area += current_best * (budget - total_cost)
    return {
        "evaluated_nodes": len(evaluated) - 1,
        "proposal_attempts": proposal_attempts,
        "task_evaluations": task_evaluations,
        "total_cost": round(total_cost, 4),
        "comparison_budget": round(budget, 4),
        "best_fixed_d60": round(current_best, 4),
        "best_node": best_node,
        "normalized_quality_cost_auc": round(
            auc_area / budget if budget else current_best,
            6,
        ),
        "quarantined_count": len(quarantined),
        "skipped_attempts": len(skipped),
        "quarantined": quarantined,
        "skipped_node_ids": skipped,
    }


def load_attempts(path: str) -> list[Attempt]:
    with open(path) as file:
        records = parse_json_stream(file.read())
    attempts = [
        Attempt(generation=record["generation"], child_id=child_id)
        for record in records
        for child_id in record["children"]
    ]
    if len({attempt.child_id for attempt in attempts}) != len(attempts):
        raise ValueError("DGM generation log contains duplicate child IDs.")
    return sorted(attempts, key=lambda attempt: (attempt.generation, attempt.child_id))


def parse_json_stream(text: str) -> list[dict]:
    decoder = json.JSONDecoder()
    records: list[dict] = []
    position = 0
    while position < len(text):
        while position < len(text) and text[position].isspace():
            position += 1
        if position == len(text):
            break
        value, position = decoder.raw_decode(text, position)
        if not isinstance(value, dict):
            raise ValueError("Expected every JSON-stream value to be an object.")
        records.append(value)
    return records


def paired_delta(parent: EvoNode, child: EvoNode) -> EdgeDelta:
    common = parent.submitted & child.submitted
    return EdgeDelta(
        common_tasks=len(common),
        gained=len((child.resolved - parent.resolved) & common),
        lost=len((parent.resolved - child.resolved) & common),
    )


def fixed_accuracy(node: EvoNode, tasks: set[str]) -> float:
    if not tasks:
        raise ValueError("Canonical task set is empty.")
    return len(node.resolved & tasks) / len(tasks)


def print_report(result: dict) -> None:
    print("=== LOGGED-CANDIDATE BRANCH QUARANTINE ===")
    for name, run in result["runs"].items():
        baseline = run["baseline"]
        print(
            f"\n{name}: baseline best={baseline['best_fixed_d60']:.4f} "
            f"cost={baseline['total_cost']:.1f} "
            f"auc={baseline['normalized_quality_cost_auc']:.4f}"
        )
        for method, row in run["policies"].items():
            print(
                f"  {method:<24} best={row['best_fixed_d60']:.4f} "
                f"save={row['cost_saving_fraction']:.2%} "
                f"auc_delta={row['auc_improvement']:+.4f} "
                f"quarantine={row['quarantined_count']} "
                f"skip={row['skipped_attempts']}"
            )
    verdict = result["verdict"]
    print(
        f"\nPrimary {verdict['primary_rule']}: "
        f"{verdict['runs_passing']}/{verdict['runs_total']} runs pass; "
        f"joint verdict={'PASS' if verdict['passed'] else 'KILL'}"
    )


if __name__ == "__main__":
    main()
