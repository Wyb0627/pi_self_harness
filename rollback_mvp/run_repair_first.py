"""Compare repair-first CLM with failure-core-first rollback."""

from __future__ import annotations

import itertools
import json
import os
import random
import statistics

from active_replay import (
    Diagnosis,
    SyntheticLineage,
    failure_first_repair,
    full_repair_ddmin,
    generate_family_cases,
    repair_first_ddmin,
)
from config import OUTPUT_DIR


SETTINGS = (
    ("clean", 0.0, 1, 1.0, 0.75, (8, 16, 32)),
    ("noise-05", 0.05, 3, 1.0, 0.75, (8, 16, 32)),
    ("noise-10", 0.10, 5, 1.0, 0.75, (8, 16, 32)),
    ("slice-recall-80", 0.0, 1, 0.80, 0.75, (8, 16, 32)),
    ("prior-none", 0.0, 1, 1.0, 0.0, (8, 16, 32)),
    ("prior-misleading", 0.0, 1, 1.0, -0.75, (8, 16, 32)),
    ("dgm-depth-clean", 0.0, 1, 1.0, 0.75, (3, 4, 5, 6)),
)


def main() -> None:
    rows: list[dict] = []
    summaries: dict[str, dict] = {}
    for setting_index, (
        setting,
        noise_rate,
        repeats,
        slice_recall,
        prior_strength,
        sizes,
    ) in enumerate(SETTINGS):
        cases = generate_family_cases(
            seed=20260940 + setting_index,
            cases_per_size=100,
            sizes=sizes,
            noise_rate=noise_rate,
            slice_fraction=0.30,
            slice_recall=slice_recall,
            prior_strength=prior_strength,
        )
        setting_rows = run_setting(setting, repeats, cases)
        rows.extend(setting_rows)
        summaries[setting] = summarize(setting_rows, seed=20260940 + setting_index)
        print_summary(setting, summaries[setting])

    comparisons = {
        setting: compare(summary)
        for setting, summary in summaries.items()
    }
    result = {
        "schema_version": 1,
        "scope": (
            "Synthetic single, joint, alternative, and mixed failure families "
            "with deterministic or majority-vote noisy replay."
        ),
        "preregistration": {
            "hypothesis": (
                "Repair-first CLM is within 0.02 repair success of the previous "
                "failure-first CLM and reduces paired mean probe calls by at least 20%."
            ),
            "kill_criterion": (
                "Kill if repair-success difference is below -0.02, relative "
                "call saving is below 0.20, or the paired 95% bootstrap interval "
                "for call reduction includes zero."
            ),
        },
        "summaries": summaries,
        "comparisons": comparisons,
        "verdict": {
            "passed": all(row["passed"] for row in comparisons.values()),
            "settings_passing": sum(
                row["passed"] for row in comparisons.values()
            ),
            "settings_total": len(comparisons),
        },
    }
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "repair_first_results.json")
    with open(path, "w") as file:
        json.dump({"result": result, "rows": rows}, file, indent=2)
        file.write("\n")
    print(
        "\nJoint verdict: "
        f"{'PASS' if result['verdict']['passed'] else 'KILL'}"
    )
    print(f"Saved {len(rows)} rows to {path}")


def run_setting(
    setting: str,
    repeats: int,
    cases: list[SyntheticLineage],
) -> list[dict]:
    rows: list[dict] = []
    for case in cases:
        for diagnosis in (
            failure_first_repair(case, repeats),
            full_repair_ddmin(case, repeats),
            repair_first_ddmin(case, repeats),
        ):
            rows.append(score_diagnosis(setting, case, diagnosis))
    return rows


def score_diagnosis(
    setting: str,
    case: SyntheticLineage,
    diagnosis: Diagnosis,
) -> dict:
    removed = frozenset(diagnosis.predicted_set)
    active = set(case.all_edges) - removed
    repairs = not case.fails(active)
    one_minimal = repairs and all(
        case.fails(set(case.all_edges) - (removed - {edge}))
        for edge in removed
    )
    return {
        "setting": setting,
        "case_id": case.case_id,
        "pattern": family_pattern(case),
        "n_edges": case.n_edges,
        "method": diagnosis.method,
        "removed": sorted(removed),
        "repair_success": int(repairs),
        "one_minimal": int(one_minimal),
        "cardinality_optimal": int(
            repairs and len(removed) == minimum_repair_size(case)
        ),
        "causal_precision": int(removed <= case.cause_set),
        "probe_calls": diagnosis.probe_calls,
        "probe_cost": round(diagnosis.probe_cost, 4),
        "used_fallback": int(diagnosis.used_fallback),
    }


def family_pattern(case: SyntheticLineage) -> str:
    families = case.cause_families
    if len(families) == 1:
        return "conjunctive"
    if all(len(family) == 1 for family in families):
        return "alternative"
    return "mixed"


def minimum_repair_size(case: SyntheticLineage) -> int:
    causes = sorted(case.cause_set)
    for size in range(1, len(causes) + 1):
        for removed in itertools.combinations(causes, size):
            if not case.fails(set(case.all_edges) - set(removed)):
                return size
    raise ValueError("No repair set found.")


def summarize(rows: list[dict], seed: int) -> dict:
    by_method: dict[str, dict] = {}
    methods = sorted({row["method"] for row in rows})
    for method in methods:
        selected = [row for row in rows if row["method"] == method]
        by_method[method] = {
            "n": len(selected),
            "repair_success": mean(selected, "repair_success"),
            "one_minimal": mean(selected, "one_minimal"),
            "cardinality_optimal": mean(selected, "cardinality_optimal"),
            "causal_precision": mean(selected, "causal_precision"),
            "mean_probe_calls": mean(selected, "probe_calls"),
            "mean_probe_cost": mean(selected, "probe_cost"),
            "fallback_rate": mean(selected, "used_fallback"),
        }

    previous = {
        row["case_id"]: row
        for row in rows
        if row["method"] == "failure-first-repair"
    }
    current = {
        row["case_id"]: row
        for row in rows
        if row["method"] == "repair-first-ddmin"
    }
    differences = [
        previous[case_id]["probe_calls"] - current[case_id]["probe_calls"]
        for case_id in sorted(previous)
    ]
    by_method["repair-first-ddmin"]["paired_call_reduction_ci95"] = (
        bootstrap_mean_interval(differences, seed)
    )
    return by_method


def compare(summary: dict) -> dict:
    previous = summary["failure-first-repair"]
    current = summary["repair-first-ddmin"]
    repair_delta = current["repair_success"] - previous["repair_success"]
    saving = 1.0 - current["mean_probe_calls"] / previous["mean_probe_calls"]
    interval = current["paired_call_reduction_ci95"]
    return {
        "repair_success_delta": round(repair_delta, 4),
        "call_saving_fraction": round(saving, 4),
        "paired_call_reduction_ci95": interval,
        "passed": (
            repair_delta >= -0.02
            and saving >= 0.20
            and interval[0] > 0
        ),
    }


def mean(rows: list[dict], key: str) -> float:
    return round(statistics.mean(row[key] for row in rows), 4)


def bootstrap_mean_interval(
    values: list[float],
    seed: int,
    samples: int = 2000,
) -> list[float]:
    rng = random.Random(seed)
    estimates = sorted(
        statistics.mean(rng.choice(values) for _ in values)
        for _ in range(samples)
    )
    return [
        round(estimates[int(0.025 * samples)], 4),
        round(estimates[int(0.975 * samples)], 4),
    ]


def print_summary(setting: str, summary: dict) -> None:
    print(f"\n=== {setting} ===")
    for method, row in summary.items():
        print(
            f"{method:<22} repair={row['repair_success']:.4f} "
            f"minimal={row['one_minimal']:.4f} "
            f"optimal={row['cardinality_optimal']:.4f} "
            f"calls={row['mean_probe_calls']:.2f}"
        )


if __name__ == "__main__":
    main()
