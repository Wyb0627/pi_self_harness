from __future__ import annotations

import dataclasses
import json
import tempfile
import unittest
from pathlib import Path

from .catalogue import load_frozen_catalogue
from .embedding_client import FakeEmbeddingClient, embed_catalogue
from .retrieval import LexicalIndex, SemanticIndex
from .schemas import (
    CandidateChangeCard,
    CoverageSelectionMode,
    EmbeddingSpec,
    ExperimentConfig,
    SCHEMA_VERSION,
    SelectorError,
    ValidationError,
)
from .selector_agent import (
    ScriptedSelectorClient,
    SelectorRound,
    SelectorToolLoop,
    SelectorTurn,
)
from .state import AppendOnlyState


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = (
    ROOT
    / "research_output"
    / "clm_budgeted_evolution_20260924_125503"
    / "dgm_swebench_verified_200.v1.json"
)
HASH_A = "a" * 64
HASH_B = "b" * 64
HASH_C = "c" * 64
MODEL_REVISION = "selector-revision-1"


def action(tool: str, arguments: dict[str, object], *, tokens: int = 1) -> SelectorTurn:
    return SelectorTurn(
        raw_response=json.dumps({"tool": tool, "arguments": arguments}),
        model_revision=MODEL_REVISION,
        input_tokens=tokens,
        output_tokens=tokens,
        cost=0.0,
        latency_seconds=0.01,
    )


class SelectorLoopTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        source_catalogue = load_frozen_catalogue(MANIFEST)
        cls.dimension = 1024
        source_vectors = {}
        for index, instance_id in enumerate(source_catalogue.task_ids):
            vector = [0.0] * cls.dimension
            vector[index] = 1.0
            source_vectors[instance_id] = tuple(vector)
        spec = EmbeddingSpec(
            sidecar_url="http://127.0.0.1:9999/v1/embeddings",
            sidecar_manifest_hash=HASH_C,
        )
        by_text = {card.task_text: source_vectors[card.instance_id] for card in source_catalogue.cards}
        cls.embedding_temporary = tempfile.TemporaryDirectory()
        bound = embed_catalogue(
            source_catalogue,
            FakeEmbeddingClient(spec, lambda text, _role: by_text.get(text, source_vectors[source_catalogue.task_ids[0]])),
            Path(cls.embedding_temporary.name),
        )
        cls.catalogue = bound.catalogue
        cls.vectors = bound.vectors

    @classmethod
    def tearDownClass(cls) -> None:
        cls.embedding_temporary.cleanup()

    def config(
        self,
        *,
        task_budget: int = 1,
        max_tasks_per_round: int = 1,
        token_budget: int = 100,
        coverage_selection_mode: CoverageSelectionMode = CoverageSelectionMode.GREEDY,
    ) -> ExperimentConfig:
        return ExperimentConfig(
            schema_version=SCHEMA_VERSION,
            coverage_selection_mode=coverage_selection_mode,
            task_budget=task_budget,
            max_rounds=2,
            max_tasks_per_round=max_tasks_per_round,
            audit_size=1,
            max_tool_calls_per_round=5,
            per_task_timeout_seconds=60,
            per_task_token_budget=1000,
            per_task_retry_budget=0,
            per_task_tool_budget=20,
            selector_token_budget=token_budget,
            selector_time_limit_seconds=10,
            experiment_seed="seed",
            selector_model_revision=MODEL_REVISION,
            embedding_model_revision="6c3ae70858513f1a78e9cdca3cae330d9075cd2a",
            embedding_manifest_hash=HASH_C,
        )

    def loop(self, client: ScriptedSelectorClient, **config: object) -> SelectorToolLoop:
        spec = EmbeddingSpec(
            sidecar_url="http://127.0.0.1:9999/v1/embeddings",
            sidecar_manifest_hash=HASH_C,
        )
        fake = FakeEmbeddingClient(spec, lambda _text, _role: self.vectors[self.catalogue.task_ids[0]])
        return SelectorToolLoop(
            catalogue=self.catalogue,
            lexical_index=LexicalIndex(self.catalogue),
            semantic_index=SemanticIndex(self.catalogue, self.vectors, fake),
            vectors=self.vectors,
            change=CandidateChangeCard(
                parent_artifact_hash=HASH_A,
                child_artifact_hash=HASH_B,
                diff_hash=HASH_C,
                repo="astropy/astropy",
                changed_paths=("packages/coding-agent/src/tool.ts",),
                changed_symbols=("runTool",),
                dependency_change="none",
                mutation_summary="Validate tool output before compaction.",
                source_revision="candidate-1",
                created_at="2026-10-09T00:00:00Z",
            ),
            bad_cases=(),
            config=self.config(**config),
            client=client,
        )

    def run_proposal_round(
        self,
        *,
        inspected_ids: tuple[str, ...],
        proposal_ids: tuple[str, ...],
        target: int,
        mode: CoverageSelectionMode,
    ) -> tuple[SelectorRound, ScriptedSelectorClient]:
        evidence_call = {
            instance_id: f"round-0-call-{index}"
            for index, instance_id in enumerate(inspected_ids)
        }
        client = ScriptedSelectorClient(
            [
                *[
                    action("get_task", {"instance_id": instance_id})
                    for instance_id in inspected_ids
                ],
                action(
                    "propose_tasks",
                    {
                        "proposals": [
                            {
                                "instance_id": instance_id,
                                "retrieval_role": "regression",
                                "evidence_reference": evidence_call[instance_id],
                                "expected_signal": "Exercise changed behavior.",
                                "rationale": "Direct mutation-specific probe.",
                                "necessary_distinct_reason": "",
                            }
                            for instance_id in proposal_ids
                        ]
                    },
                ),
                action(
                    "finish_round",
                    {"stop_reason": "round evidence ready", "stop_after_round": False},
                ),
            ]
        )
        result = self.loop(
            client,
            task_budget=target,
            max_tasks_per_round=target,
            coverage_selection_mode=mode,
        ).run_round(round_id=0, selected_ids=(), prior_round_summaries={})
        return result, client

    def test_tool_loop_validates_proposals_and_uses_lexicographic_coverage(self) -> None:
        first, second = self.catalogue.task_ids[:2]
        client = ScriptedSelectorClient(
            [
                action("get_task", {"instance_id": first}),
                action("get_task", {"instance_id": second}),
                action(
                    "propose_tasks",
                    {
                        "proposals": [
                            {
                                "instance_id": second,
                                "retrieval_role": "regression",
                                "evidence_reference": "round-0-call-1",
                                "expected_signal": "Child preserves tool execution.",
                                "rationale": "Exercises changed tool behavior.",
                                "necessary_distinct_reason": "",
                            },
                            {
                                "instance_id": first,
                                "retrieval_role": "regression",
                                "evidence_reference": "round-0-call-0",
                                "expected_signal": "Child preserves tool execution.",
                                "rationale": "Exercises changed tool behavior.",
                                "necessary_distinct_reason": "",
                            },
                        ]
                    },
                ),
                action(
                    "finish_round",
                    {"stop_reason": "round evidence ready", "stop_after_round": False},
                ),
            ]
        )
        result = self.loop(client).run_round(
            round_id=0, selected_ids=(), prior_round_summaries={}
        )
        self.assertEqual(result.selected_tasks[0].proposal.instance_id, first)
        self.assertAlmostEqual(result.selected_tasks[0].marginal_coverage, 1 / 200)
        self.assertEqual(result.selected_tasks[0].selection_source, "direct_hypothesis")
        prompt_text = json.dumps(client.prompts)
        self.assertNotIn("audit_seed", prompt_text)
        self.assertNotIn("audit_candidate", prompt_text)
        self.assertNotIn("audit_ids", prompt_text)
        self.assertEqual(client.prompts[0]["coverage_selection_mode"], "greedy")
        self.assertEqual(client.prompts[0]["round_task_capacity"], 1)

    def test_full_direct_budget_selects_same_ids_in_both_modes(self) -> None:
        ordered = tuple(sorted(self.catalogue.task_ids[:3]))
        proposal_ids = (ordered[2], ordered[1])
        greedy, _ = self.run_proposal_round(
            inspected_ids=proposal_ids,
            proposal_ids=proposal_ids,
            target=2,
            mode=CoverageSelectionMode.GREEDY,
        )
        agent_only, _ = self.run_proposal_round(
            inspected_ids=proposal_ids,
            proposal_ids=proposal_ids,
            target=2,
            mode=CoverageSelectionMode.AGENT_ONLY,
        )
        self.assertEqual(
            tuple(item.proposal.instance_id for item in greedy.selected_tasks),
            proposal_ids,
        )
        self.assertEqual(
            tuple(item.proposal.instance_id for item in agent_only.selected_tasks),
            proposal_ids,
        )

    def test_over_capacity_agent_only_preserves_proposal_order(self) -> None:
        ordered = tuple(sorted(self.catalogue.task_ids[:3]))
        proposal_ids = tuple(reversed(ordered))
        greedy, _ = self.run_proposal_round(
            inspected_ids=proposal_ids,
            proposal_ids=proposal_ids,
            target=2,
            mode=CoverageSelectionMode.GREEDY,
        )
        agent_only, _ = self.run_proposal_round(
            inspected_ids=proposal_ids,
            proposal_ids=proposal_ids,
            target=2,
            mode=CoverageSelectionMode.AGENT_ONLY,
        )
        self.assertEqual(
            tuple(item.proposal.instance_id for item in greedy.selected_tasks),
            ordered[:2],
        )
        self.assertEqual(
            tuple(item.proposal.instance_id for item in agent_only.selected_tasks),
            proposal_ids[:2],
        )

    def test_under_capacity_agent_only_does_not_fill(self) -> None:
        first, second = self.catalogue.task_ids[:2]
        greedy, _ = self.run_proposal_round(
            inspected_ids=(first, second),
            proposal_ids=(first,),
            target=2,
            mode=CoverageSelectionMode.GREEDY,
        )
        agent_only, _ = self.run_proposal_round(
            inspected_ids=(first, second),
            proposal_ids=(first,),
            target=2,
            mode=CoverageSelectionMode.AGENT_ONLY,
        )
        self.assertEqual(len(greedy.selected_tasks), 2)
        self.assertEqual(
            greedy.selected_tasks[1].selection_source, "coverage_completion"
        )
        self.assertEqual(
            tuple(item.proposal.instance_id for item in agent_only.selected_tasks),
            (first,),
        )
        self.assertEqual(agent_only.selected_tasks[0].selection_source, "agent_direct")

    def test_coverage_selection_mode_changes_config_hash(self) -> None:
        greedy = self.config()
        agent_only = dataclasses.replace(
            greedy, coverage_selection_mode=CoverageSelectionMode.AGENT_ONLY
        )
        self.assertNotEqual(greedy.config_hash, agent_only.config_hash)
        with self.assertRaisesRegex(ValidationError, "CoverageSelectionMode"):
            dataclasses.replace(greedy, coverage_selection_mode="greedy")

    def test_invalid_json_unknown_tool_unknown_id_and_budget_fail_closed(self) -> None:
        invalid = SelectorTurn(
            raw_response="not json",
            model_revision=MODEL_REVISION,
            input_tokens=1,
            output_tokens=1,
            cost=0,
            latency_seconds=0,
        )
        with self.assertRaisesRegex(SelectorError, "invalid JSON"):
            self.loop(ScriptedSelectorClient([invalid])).run_round(
                round_id=0, selected_ids=(), prior_round_summaries={}
            )
        with self.assertRaisesRegex(SelectorError, "Unknown selector tool"):
            self.loop(
                ScriptedSelectorClient([action("read_gold_patch", {})])
            ).run_round(round_id=0, selected_ids=(), prior_round_summaries={})
        with self.assertRaisesRegex(SelectorError, "Unknown task ID"):
            self.loop(
                ScriptedSelectorClient([action("get_task", {"instance_id": "bad"})])
            ).run_round(round_id=0, selected_ids=(), prior_round_summaries={})
        with self.assertRaisesRegex(SelectorError, "token budget exceeded"):
            self.loop(
                ScriptedSelectorClient([action("get_change", {}, tokens=2)]),
                token_budget=3,
            ).run_round(round_id=0, selected_ids=(), prior_round_summaries={})

    def test_proposal_requires_role_reference_signal_rationale_and_stop(self) -> None:
        task_id = self.catalogue.task_ids[0]
        malformed = {
            "instance_id": task_id,
            "retrieval_role": "regression",
            "evidence_reference": "round-0-call-0",
            "expected_signal": "signal",
            "rationale": "reason",
        }
        client = ScriptedSelectorClient(
            [
                action("get_task", {"instance_id": task_id}),
                action("propose_tasks", {"proposals": [malformed]}),
            ]
        )
        with self.assertRaisesRegex(SelectorError, "fields must be exactly"):
            self.loop(client).run_round(
                round_id=0, selected_ids=(), prior_round_summaries={}
            )

    def test_append_only_state_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            state = AppendOnlyState(Path(temporary))
            state.append("round_frozen", {"round_id": 0})
            state.append("pair_result", {"round_id": 0})
            self.assertEqual(len(AppendOnlyState(Path(temporary)).events), 2)
            first_path = Path(temporary) / "events" / "000000.json"
            raw = json.loads(first_path.read_text())
            raw["payload"]["round_id"] = 4
            first_path.write_text(json.dumps(raw))
            with self.assertRaisesRegex(Exception, "hash mismatch"):
                AppendOnlyState(Path(temporary))


if __name__ == "__main__":
    unittest.main()
