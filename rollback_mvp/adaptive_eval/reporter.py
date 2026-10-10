"""Content-hashed run reports and immutable evidence summaries."""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any, Mapping, Sequence

from .coverage import RedundancyReport
from .decision import DecisionResult
from .paired_executor import FrozenTaskPlan, PairResult
from .schemas import hash_json
from .state import atomic_json, freeze_file_once


def write_final_report(
    output_root: Path,
    *,
    plan: FrozenTaskPlan,
    pairs: Sequence[PairResult],
    decision: DecisionResult,
    coverage: float,
    redundancy: RedundancyReport,
    token_cost_latency: Mapping[str, Any],
    exceptions: Sequence[Mapping[str, Any]],
) -> str:
    payload = {
        "schema_version": 1,
        "plan": dataclasses.asdict(plan),
        "plan_hash": plan.plan_hash,
        "pair_result_hashes": [pair.pair_hash for pair in pairs],
        "decision": dataclasses.asdict(decision),
        "coverage": coverage,
        "redundancy": dataclasses.asdict(redundancy),
        "token_cost_latency": dict(token_cost_latency),
        "exceptions": list(exceptions),
    }
    report_hash = hash_json(payload)
    freeze_file_once(
        output_root / "final-report.json", payload | {"report_hash": report_hash}
    )
    return report_hash


def write_error_report(
    output_root: Path, *, phase: str, error: BaseException, evidence: Mapping[str, Any]
) -> Path:
    path = output_root / "errors" / f"{len(list((output_root / 'errors').glob('*.json'))):06d}.json"
    atomic_json(
        path,
        {
            "phase": phase,
            "error_type": type(error).__name__,
            "message": str(error),
            "evidence": dict(evidence),
        },
    )
    return path
