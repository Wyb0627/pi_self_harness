"""Evaluate causal-lineage localization algorithms on generated lineages."""

from __future__ import annotations

import json
import os

from active_replay import (
    active_sliced_ddmin,
    Diagnosis,
    SyntheticLineage,
    binary_prefix,
    full_ddmin,
    full_repair_ddmin,
    generate_cases,
    linear_prefix,
    repair_first_ddmin,
    rollback_one,
    sliced_ddmin,
)
from config import OUTPUT_DIR

SETTINGS = (
    {
        "name": "clean",
        "noise_rate": 0.0,
        "repeats": 1,
        "slice_recall": 1.0,
    },
    {
        "name": "noise-05",
        "noise_rate": 0.05,
        "repeats": 3,
        "slice_recall": 1.0,
    },
    {
        "name": "noise-10",
        "noise_rate": 0.10,
        "repeats": 5,
        "slice_recall": 1.0,
    },
    {
        "name": "slice-recall-80",
        "noise_rate": 0.0,
        "repeats": 1,
        "slice_recall": 0.80,
    },
)


def main() -> None:
    all_rows: list[dict] = []
    for setting_index, setting in enumerate(SETTINGS):
        cases = generate_cases(
            seed=20260924 + setting_index,
            cases_per_size=100,
            sizes=(8, 16, 32),
            noise_rate=setting["noise_rate"],
            slice_fraction=0.40,
            slice_recall=setting["slice_recall"],
            prior_strength=0.75,
        )
        rows = _run_setting(setting["name"], setting["repeats"], cases)
        all_rows.extend(rows)
        _report(setting["name"], rows)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "active_replay_results.jsonl")
    with open(path, "w") as f:
        for row in all_rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"\nSaved {len(all_rows)} rows to {path}")


def _run_setting(
    setting: str,
    repeats: int,
    cases: list[SyntheticLineage],
) -> list[dict]:
    rows: list[dict] = []
    for case in cases:
        diagnoses = (
            rollback_one(case),
            linear_prefix(case, repeats),
            binary_prefix(case, repeats),
            full_ddmin(case, repeats),
            full_repair_ddmin(case, repeats),
            sliced_ddmin(case, repeats),
            active_sliced_ddmin(case, repeats),
            repair_first_ddmin(case, repeats),
        )
        for diagnosis in diagnoses:
            rows.append(_score(setting, case, diagnosis))
    return rows


def _score(
    setting: str,
    case: SyntheticLineage,
    diagnosis: Diagnosis,
) -> dict:
    predicted = frozenset(diagnosis.predicted_set)
    active_after_repair = set(case.all_edges) - predicted
    repairs = not case.fails(active_after_repair)
    minimal_removal = repairs and all(
        case.fails(
            set(case.all_edges) - (predicted - {edge})
        )
        for edge in predicted
    )
    return {
        "setting": setting,
        "case_id": case.case_id,
        "n_edges": case.n_edges,
        "cause_size": len(case.cause_set),
        "method": diagnosis.method,
        "predicted_set": list(diagnosis.predicted_set),
        "cause_set": sorted(case.cause_set),
        "exact_set": int(predicted == case.cause_set),
        "earliest_exact": int(
            bool(predicted) and min(predicted) == min(case.cause_set)
        ),
        "repair_success": int(repairs),
        "minimal_removal": int(minimal_removal),
        "probe_calls": diagnosis.probe_calls,
        "probe_cost": round(diagnosis.probe_cost, 4),
        "used_fallback": int(diagnosis.used_fallback),
    }


def _report(setting: str, rows: list[dict]) -> None:
    methods = (
        "rollback-1",
        "linear-prefix",
        "binary-prefix",
        "full-ddmin",
        "full-repair-ddmin",
        "sliced-ddmin",
        "active-sliced-ddmin",
        "repair-first-ddmin",
    )
    print(f"\n=== {setting} ===")
    print(
        f"{'method':<20}{'exact':>9}{'earliest':>10}{'repair':>9}"
        f"{'minimal':>9}{'calls':>9}{'cost':>9}{'fallback':>10}"
    )
    summaries: dict[str, dict[str, float]] = {}
    for method in methods:
        selected = [row for row in rows if row["method"] == method]
        n = len(selected)
        summary = {
            "exact": sum(row["exact_set"] for row in selected) / n,
            "earliest": sum(row["earliest_exact"] for row in selected) / n,
            "repair": sum(row["repair_success"] for row in selected) / n,
            "minimal": sum(row["minimal_removal"] for row in selected) / n,
            "calls": sum(row["probe_calls"] for row in selected) / n,
            "cost": sum(row["probe_cost"] for row in selected) / n,
            "fallback": sum(row["used_fallback"] for row in selected) / n,
        }
        summaries[method] = summary
        print(
            f"{method:<20}{summary['exact']:>9.3f}"
            f"{summary['earliest']:>10.3f}"
            f"{summary['repair']:>9.3f}"
            f"{summary['minimal']:>9.3f}"
            f"{summary['calls']:>9.2f}"
            f"{summary['cost']:>9.2f}"
            f"{summary['fallback']:>10.3f}"
        )

    full_calls = summaries["full-ddmin"]["calls"]
    sliced_calls = summaries["sliced-ddmin"]["calls"]
    active_calls = summaries["active-sliced-ddmin"]["calls"]
    repair_first_calls = summaries["repair-first-ddmin"]["calls"]
    print(f"sliced call saving vs full ddmin: {1.0 - sliced_calls / full_calls:.3f}")
    print(f"active call saving vs full ddmin: {1.0 - active_calls / full_calls:.3f}")
    print(
        "repair-first call saving vs full ddmin: "
        f"{1.0 - repair_first_calls / full_calls:.3f}"
    )


if __name__ == "__main__":
    main()
