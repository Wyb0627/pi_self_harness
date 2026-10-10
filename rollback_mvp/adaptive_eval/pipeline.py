"""Executable final-pair, decision, and report pipeline."""

from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass
from pathlib import Path

from .controller import SelectionResult
from .coverage import redundancy
from .decision import DecisionResult, decide
from .paired_executor import ArtifactRef, PairedExecutor, PairResult
from .reporter import write_error_report, write_final_report
from .schemas import (
    CatalogueManifest,
    DecisionOutcome,
    DecisionPolicy,
    PairExecutionError,
)
from .state import AppendOnlyState, atomic_json


@dataclass(frozen=True, slots=True)
class FinalPipelineResult:
    pairs: tuple[PairResult, ...]
    decision: DecisionResult
    report_hash: str


def run_final_pipeline(
    *,
    selection: SelectionResult,
    executor: PairedExecutor,
    parent: ArtifactRef,
    child: ArtifactRef,
    policy: DecisionPolicy,
    catalogue: CatalogueManifest,
    vectors: dict[str, tuple[float, ...]],
    output_root: Path,
) -> FinalPipelineResult:
    state = AppendOnlyState(output_root / "decision-state")
    if state.events:
        raise PairExecutionError("Decision state already exists; refusing implicit resume")
    try:
        if executor.plan != selection.frozen_plan:
            raise PairExecutionError("Pipeline executor plan differs from selection result")
        if selection.selection_manifest_hash != selection.frozen_plan.selection_manifest_hash:
            raise PairExecutionError("Selection result and frozen plan manifest hashes differ")
        try:
            selection_manifest = json.loads(
                Path(selection.selection_manifest_path).read_text()
            )
        except (OSError, json.JSONDecodeError) as error:
            raise PairExecutionError(
                f"Cannot validate pipeline selection manifest: {error}"
            ) from error
        if selection_manifest.get("manifest_hash") != selection.selection_manifest_hash:
            raise PairExecutionError(
                "Pipeline selection manifest hash differs from selection result"
            )
        pairs = executor.run_pairs(parent, child)
        decision = decide(
            selection.frozen_plan,
            pairs,
            policy,
            catalogue,
            executor.settings,
            executor.experiment_config,
        )
        report_hash = write_final_report(
            output_root,
            plan=selection.frozen_plan,
            pairs=pairs,
            decision=decision,
            coverage=selection.coverage,
            redundancy=redundancy(selection.frozen_plan.final_task_ids, vectors),
            token_cost_latency={
                "input_tokens": sum(
                    pair.parent.input_tokens + pair.child.input_tokens for pair in pairs
                ),
                "output_tokens": sum(
                    pair.parent.output_tokens + pair.child.output_tokens for pair in pairs
                ),
                "cost": sum(pair.parent.cost + pair.child.cost for pair in pairs),
                "latency_seconds": sum(
                    pair.parent.latency_seconds + pair.child.latency_seconds for pair in pairs
                ),
            },
            exceptions=(),
        )
        state.append(
            "decision_complete",
            {
                "outcome": decision.outcome,
                "decision": dataclasses.asdict(decision),
                "report_hash": report_hash,
            },
        )
        return FinalPipelineResult(pairs, decision, report_hash)
    except Exception as error:
        invalid = {
            "outcome": DecisionOutcome.INVALID,
            "error_type": type(error).__name__,
            "message": str(error),
            "final_manifest_hash": selection.frozen_plan.manifest_hash,
        }
        atomic_json(output_root / "invalid-decision.json", invalid)
        write_error_report(
            output_root, phase="final_pair_or_decision", error=error, evidence=invalid
        )
        state.append("decision_invalid", invalid)
        raise
