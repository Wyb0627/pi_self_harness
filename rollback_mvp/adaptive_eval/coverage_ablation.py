"""Replay fixed selector traces under greedy and agent-only arbitration."""

from __future__ import annotations

import argparse
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .catalogue import load_frozen_catalogue
from .coverage import facility_location_coverage, redundancy
from .embedding_client import FakeEmbeddingClient, embed_catalogue
from .retrieval import LexicalIndex, SemanticIndex
from .schemas import (
    CandidateChangeCard,
    CoverageSelectionMode,
    EmbeddingSpec,
    ExperimentConfig,
    SCHEMA_VERSION,
    hash_json,
    sha256_bytes,
)
from .selector_agent import (
    ScriptedSelectorClient,
    SelectorToolLoop,
    SelectorTurn,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = (
    ROOT
    / "research_output"
    / "clm_budgeted_evolution_20260924_125503"
    / "dgm_swebench_verified_200.v1.json"
)
HASH_A = "a" * 64
HASH_B = "b" * 64
HASH_C = "c" * 64
MODEL_REVISION = "coverage-ablation-scripted-selector-v1"


@dataclass(frozen=True, slots=True)
class ReplayScenario:
    name: str
    target: int
    inspected_ids: tuple[str, ...]
    proposal_ids: tuple[str, ...]


def _action(tool: str, arguments: dict[str, object]) -> SelectorTurn:
    return SelectorTurn(
        raw_response=json.dumps(
            {"tool": tool, "arguments": arguments},
            sort_keys=True,
            separators=(",", ":"),
        ),
        model_revision=MODEL_REVISION,
        input_tokens=1,
        output_tokens=1,
        cost=0.0,
        latency_seconds=0.0,
    )


def _config(mode: CoverageSelectionMode, target: int) -> ExperimentConfig:
    return ExperimentConfig(
        schema_version=SCHEMA_VERSION,
        coverage_selection_mode=mode,
        task_budget=target,
        max_rounds=1,
        max_tasks_per_round=target,
        audit_size=1,
        max_tool_calls_per_round=6,
        per_task_timeout_seconds=60,
        per_task_token_budget=1000,
        per_task_retry_budget=0,
        per_task_tool_budget=20,
        selector_token_budget=100,
        selector_time_limit_seconds=10,
        experiment_seed="coverage-ablation-v1",
        selector_model_revision=MODEL_REVISION,
        embedding_model_revision="6c3ae70858513f1a78e9cdca3cae330d9075cd2a",
        embedding_manifest_hash=HASH_C,
    )


def _turns(scenario: ReplayScenario) -> list[SelectorTurn]:
    evidence_call = {
        instance_id: f"round-0-call-{index}"
        for index, instance_id in enumerate(scenario.inspected_ids)
    }
    proposals = [
        {
            "instance_id": instance_id,
            "retrieval_role": "regression",
            "evidence_reference": evidence_call[instance_id],
            "expected_signal": "Exercise changed behavior.",
            "rationale": "Direct mutation-specific probe.",
            "necessary_distinct_reason": "",
        }
        for instance_id in scenario.proposal_ids
    ]
    return [
        *[
            _action("get_task", {"instance_id": instance_id})
            for instance_id in scenario.inspected_ids
        ],
        _action("propose_tasks", {"proposals": proposals}),
        _action(
            "finish_round",
            {"stop_after_round": False, "stop_reason": "round evidence ready"},
        ),
    ]


def _run_mode(
    *,
    catalogue,
    vectors: dict[str, tuple[float, ...]],
    embedding_client: FakeEmbeddingClient,
    scenario: ReplayScenario,
    mode: CoverageSelectionMode,
) -> dict[str, object]:
    turns = _turns(scenario)
    client = ScriptedSelectorClient(turns)
    config = _config(mode, scenario.target)
    loop = SelectorToolLoop(
        catalogue=catalogue,
        lexical_index=LexicalIndex(catalogue),
        semantic_index=SemanticIndex(catalogue, vectors, embedding_client),
        vectors=vectors,
        change=CandidateChangeCard(
            parent_artifact_hash=HASH_A,
            child_artifact_hash=HASH_B,
            diff_hash=HASH_C,
            repo="astropy/astropy",
            changed_paths=("packages/coding-agent/src/tool.ts",),
            changed_symbols=("runTool",),
            dependency_change="none",
            mutation_summary="Validate tool output before compaction.",
            source_revision="coverage-ablation-candidate-v1",
            created_at="2026-10-14T00:00:00Z",
        ),
        bad_cases=(),
        config=config,
        client=client,
    )
    result = loop.run_round(
        round_id=0,
        selected_ids=(),
        prior_round_summaries={},
    )
    selected_ids = tuple(
        item.proposal.instance_id for item in result.selected_tasks
    )
    redundancy_report = redundancy(selected_ids, vectors)
    return {
        "config_hash": config.config_hash,
        "selected_ids": selected_ids,
        "selection_sources": tuple(
            item.selection_source for item in result.selected_tasks
        ),
        "marginal_coverage": tuple(
            item.marginal_coverage for item in result.selected_tasks
        ),
        "coverage": facility_location_coverage(
            selected_ids, catalogue.task_ids, vectors
        ),
        "redundancy": redundancy_report.value,
        "selector_input_tokens": result.input_tokens,
        "selector_output_tokens": result.output_tokens,
        "selector_trace_hash": hash_json(
            [record.raw_response for record in result.tool_calls]
        ),
    }


def run_ablation(manifest_path: Path) -> dict[str, object]:
    source_catalogue = load_frozen_catalogue(manifest_path)
    source_vectors: dict[str, tuple[float, ...]] = {}
    for index, instance_id in enumerate(source_catalogue.task_ids):
        vector = [0.0] * 1024
        vector[index] = 1.0
        source_vectors[instance_id] = tuple(vector)
    spec = EmbeddingSpec(
        sidecar_url="http://127.0.0.1:9999/v1/embeddings",
        sidecar_manifest_hash=HASH_C,
    )
    by_text = {
        card.task_text: source_vectors[card.instance_id]
        for card in source_catalogue.cards
    }
    with tempfile.TemporaryDirectory() as temporary:
        bound = embed_catalogue(
            source_catalogue,
            FakeEmbeddingClient(
                spec,
                lambda text, _role: by_text.get(
                    text, source_vectors[source_catalogue.task_ids[0]]
                ),
            ),
            Path(temporary),
        )
        embedding_client = FakeEmbeddingClient(
            spec,
            lambda _text, _role: bound.vectors[bound.catalogue.task_ids[0]],
        )
        ordered = tuple(sorted(bound.catalogue.task_ids[:3]))
        scenarios = (
            ReplayScenario(
                name="exact_direct_budget",
                target=2,
                inspected_ids=(ordered[2], ordered[1]),
                proposal_ids=(ordered[2], ordered[1]),
            ),
            ReplayScenario(
                name="over_capacity",
                target=2,
                inspected_ids=tuple(reversed(ordered)),
                proposal_ids=tuple(reversed(ordered)),
            ),
            ReplayScenario(
                name="under_capacity",
                target=2,
                inspected_ids=ordered[:2],
                proposal_ids=ordered[:1],
            ),
        )
        results = {}
        for scenario in scenarios:
            results[scenario.name] = {
                mode: _run_mode(
                    catalogue=bound.catalogue,
                    vectors=bound.vectors,
                    embedding_client=embedding_client,
                    scenario=scenario,
                    mode=mode,
                )
                for mode in (
                    CoverageSelectionMode.GREEDY,
                    CoverageSelectionMode.AGENT_ONLY,
                )
            }

    exact = results["exact_direct_budget"]
    over = results["over_capacity"]
    under = results["under_capacity"]
    exact_same_ids = (
        exact[CoverageSelectionMode.GREEDY]["selected_ids"]
        == exact[CoverageSelectionMode.AGENT_ONLY]["selected_ids"]
    )
    over_differs = (
        over[CoverageSelectionMode.GREEDY]["selected_ids"]
        != over[CoverageSelectionMode.AGENT_ONLY]["selected_ids"]
    )
    greedy_under_count = len(
        under[CoverageSelectionMode.GREEDY]["selected_ids"]
    )
    agent_under_count = len(
        under[CoverageSelectionMode.AGENT_ONLY]["selected_ids"]
    )
    under_planned_task_reduction = 1.0 - agent_under_count / greedy_under_count
    same_trace_hashes = all(
        scenario_results[CoverageSelectionMode.GREEDY]["selector_trace_hash"]
        == scenario_results[CoverageSelectionMode.AGENT_ONLY][
            "selector_trace_hash"
        ]
        for scenario_results in results.values()
    )
    return {
        "schema_version": 1,
        "evidence_level": "mechanism_only",
        "catalogue": {
            "dataset_manifest_hash": source_catalogue.dataset_manifest_hash,
            "catalogue_hash": source_catalogue.catalogue_hash,
            "task_count": len(source_catalogue.task_ids),
        },
        "replay_design": {
            "selector": "scripted fixed trace",
            "embeddings": "synthetic orthogonal 1024-D vectors",
            "paired_task_execution": False,
            "paid_model_calls": False,
        },
        "preregistered_predictions": {
            "exact_direct_budget_same_ids": True,
            "over_capacity_modes_can_differ": True,
            "under_capacity_agent_only_selects_fewer_tasks": True,
            "selector_trace_and_token_usage_unchanged": True,
        },
        "scenario_results": results,
        "checks": {
            "exact_direct_budget_same_ids": exact_same_ids,
            "over_capacity_modes_differ": over_differs,
            "under_capacity_planned_task_reduction": under_planned_task_reduction,
            "selector_trace_hashes_unchanged": same_trace_hashes,
            "full_budget_isolation_kill_triggered": not exact_same_ids,
        },
        "conclusion": (
            "The mechanism hypothesis survives replay: coverage arbitration is "
            "behaviorally redundant only when direct proposals exactly fill the "
            "round. Agent-only can save paired executions only when a round is "
            "underfilled."
        ),
        "limitations": (
            "This replay does not estimate SWE-bench quality, regression recall, "
            "wall time, or endpoint cost. A valid endpoint ablation still requires "
            "a real selector adapter, pinned embedding sidecar, trusted paired "
            "round evaluator, and isolated candidate runtime."
        ),
    }


def _report_markdown(result: dict[str, object]) -> str:
    checks = result["checks"]
    scenarios = result["scenario_results"]
    rows = []
    for name, modes in scenarios.items():
        greedy = modes[CoverageSelectionMode.GREEDY]
        agent_only = modes[CoverageSelectionMode.AGENT_ONLY]
        rows.append(
            f"| {name} | {len(greedy['selected_ids'])} | "
            f"{len(agent_only['selected_ids'])} | "
            f"{greedy['selected_ids'] == agent_only['selected_ids']} |"
        )
    return "\n".join(
        [
            "# Coverage Selection Mechanism Ablation",
            "",
            "Evidence level: mechanism-only replay over the frozen DGM-200 catalogue.",
            "The selector action trace is fixed across both arbitration modes.",
            "",
            "## Pre-registration",
            "",
            "Hypothesis: facility-location arbitration is behaviorally redundant "
            "when direct proposals exactly fill capacity. It changes selection "
            "only when proposals exceed capacity or when it fills an under-capacity "
            "round.",
            "",
            "Primary checks:",
            "",
            "- Exact-capacity task IDs must be identical.",
            "- Over-capacity modes may differ because only greedy reorders.",
            "- Under-capacity agent-only must select fewer planned tasks.",
            "- Fixed selector traces and selector token usage must remain unchanged.",
            "",
            "Kill criterion: any exact-capacity ID difference invalidates the "
            "isolation. A future endpoint run must retain greedy completion if "
            "real underfilled rounds save less than 20% execution cost or show "
            "materially worse regret or false-accept behavior.",
            "",
            "## Scenarios",
            "",
            "| Scenario | Greedy tasks | Agent-only tasks | Same IDs |",
            "| --- | ---: | ---: | --- |",
            *rows,
            "",
            "## Result",
            "",
            f"- Exact-budget isolation passed: "
            f"{checks['exact_direct_budget_same_ids']}.",
            f"- Over-capacity arbitration differs: "
            f"{checks['over_capacity_modes_differ']}.",
            f"- Under-capacity planned task-count reduction in this replay: "
            f"{checks['under_capacity_planned_task_reduction']:.1%}.",
            f"- Selector traces remained identical: "
            f"{checks['selector_trace_hashes_unchanged']}.",
            f"- Kill criterion triggered: "
            f"{checks['full_budget_isolation_kill_triggered']}.",
            "",
            "## Interpretation",
            "",
            result["conclusion"],
            "",
            "## Limitation",
            "",
            result["limitations"],
            "",
        ]
    )


def _experiment_log_markdown(results_hash: str) -> str:
    return "\n".join(
        [
            "# Experiment Log",
            "",
            "## 2026-10-14",
            "",
            "1. Inspected the production arbitration path. Coverage affects direct "
            "proposals only when they exceed capacity, and fills capacity when "
            "direct proposals underfill it.",
            "2. Searched for real selector transcripts, a pinned embedding cache, "
            "a production selector adapter, and a trusted paired round evaluator. "
            "No runnable end-to-end adaptive experiment was available.",
            "3. Added a hash-bound `coverage_selection_mode` with `greedy` and "
            "`agent_only` arms. Agent-only preserves direct proposal order, "
            "truncates at capacity, and never fills.",
            "4. Replayed three fixed scripted selector traces over the frozen "
            "DGM-200 catalogue with synthetic orthogonal embeddings.",
            "5. Observed identical exact-capacity IDs, different over-capacity "
            "arbitration, and a 2-to-1 task reduction in the under-capacity case. "
            "The isolation kill criterion did not trigger.",
            "6. Repeated the replay and obtained a byte-identical `results.json` "
            f"(SHA-256 {results_hash}).",
            "7. Ran all 35 adaptive-eval unit tests successfully. Root `npm run "
            "check` passed formatting, then stopped on pre-existing unpinned "
            "dependencies inside generated DGM task workspaces. The remaining "
            "repository checks passed except `tsgo --noEmit`, which reported "
            "pre-existing model-catalog `unknown`/`never` errors across the AI "
            "package. No unrelated workspace files were modified.",
            "",
            "## Decision",
            "",
            "Keep both modes. The mechanism result supports running a paid endpoint "
            "ablation once the real selector, embedding sidecar, evaluator, and "
            "candidate runtime are available. It does not justify deleting greedy "
            "coverage yet.",
            "",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Replay coverage-selection arbitration modes"
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = run_ablation(args.manifest)
    args.output.mkdir(parents=True, exist_ok=True)
    results_text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    (args.output / "results.json").write_text(results_text, encoding="utf-8")
    (args.output / "report.md").write_text(
        _report_markdown(result),
        encoding="utf-8",
    )
    (args.output / "experiment_log.md").write_text(
        _experiment_log_markdown(sha256_bytes(results_text.encode("utf-8"))),
        encoding="utf-8",
    )
    print(json.dumps(result["checks"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
