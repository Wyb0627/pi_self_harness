from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from .catalogue import load_frozen_catalogue
from .controller import (
    AdaptiveEvaluationController,
    RoundEvidence,
    SanitizedRoundPair,
)
from .embedding_client import FakeEmbeddingClient, embed_catalogue
from .retrieval import LexicalIndex, SemanticIndex
from .schemas import CandidateChangeCard, EmbeddingSpec, ExperimentConfig, SCHEMA_VERSION
from .schemas import hash_json, source_diff_hash, source_tree_hash
from .selector_agent import ScriptedSelectorClient, SelectorToolLoop, SelectorTurn


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
HASH_D = "d" * 64
HASH_E = "e" * 64
MODEL_REVISION = "selector-v1"


def selector_action(tool: str, arguments: dict[str, object]) -> SelectorTurn:
    return SelectorTurn(
        raw_response=json.dumps({"tool": tool, "arguments": arguments}),
        model_revision=MODEL_REVISION,
        input_tokens=1,
        output_tokens=1,
        cost=0,
        latency_seconds=0.01,
    )


class FakeRoundEvaluator:
    def __init__(self) -> None:
        self.calls: list[tuple[int, tuple[str, ...]]] = []

    def evaluate_round(self, round_id, task_ids):
        values = tuple(task_ids)
        self.calls.append((round_id, values))
        pairs = []
        for task_id in values:
            identity = {
                "task_instance_id": task_id,
                "task_repo": ControllerTest.catalogue.by_id[task_id].repo,
                "task_base_commit": ControllerTest.catalogue.by_id[task_id].base_commit,
                "parent_artifact_hash": self.parent_hash,
                "child_artifact_hash": self.child_hash,
                "dataset_manifest_hash": ControllerTest.catalogue.dataset_manifest_hash,
                "budgets": {
                    "timeout_seconds": 60,
                    "token_budget": 1000,
                    "retry_budget": 0,
                    "tool_budget": 20,
                },
            }
            pairs.append(
                SanitizedRoundPair(
                    task_instance_id=task_id,
                    parent_resolved=False,
                    child_resolved=True,
                    pair_result_hash=HASH_E,
                    paired_identity_hash=hash_json(identity),
                    paired_identity_payload=identity,
                )
            )
        return RoundEvidence(
            round_id=round_id,
            task_ids=values,
            pairs=tuple(pairs),
        )


class ControllerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        source_catalogue = load_frozen_catalogue(MANIFEST)
        source_vectors = {}
        for index, task_id in enumerate(source_catalogue.task_ids):
            vector = [0.0] * 1024
            vector[index] = 1.0
            source_vectors[task_id] = tuple(vector)
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

    def build_controller(self, output: Path):
        parent_snapshot = output / "snapshots" / "parent"
        child_snapshot = output / "snapshots" / "child"
        parent_snapshot.mkdir(parents=True)
        child_snapshot.mkdir(parents=True)
        (parent_snapshot / "agent.py").write_text("value = 1\n")
        (child_snapshot / "agent.py").write_text("value = 2\n")
        parent_hash = source_tree_hash(parent_snapshot)
        child_hash = source_tree_hash(child_snapshot)
        diff_hash = source_diff_hash(parent_snapshot, child_snapshot)
        task_id = self.catalogue.task_ids[0]
        client = ScriptedSelectorClient(
            [
                selector_action("get_task", {"instance_id": task_id}),
                selector_action(
                    "propose_tasks",
                    {
                        "proposals": [
                            {
                                "instance_id": task_id,
                                "retrieval_role": "regression",
                                "evidence_reference": "round-0-call-0",
                                "expected_signal": "Child preserves changed behavior.",
                                "rationale": "Task probes the changed execution path.",
                                "necessary_distinct_reason": "",
                            }
                        ]
                    },
                ),
                selector_action(
                    "finish_round",
                    {
                        "stop_reason": "evidence_saturation: direct probe is sufficient",
                        "stop_after_round": True,
                    },
                ),
            ]
        )
        config = ExperimentConfig(
            schema_version=SCHEMA_VERSION,
            task_budget=1,
            max_rounds=2,
            max_tasks_per_round=1,
            audit_size=1,
            max_tool_calls_per_round=5,
            per_task_timeout_seconds=60,
            per_task_token_budget=1000,
            per_task_retry_budget=0,
            per_task_tool_budget=20,
            selector_token_budget=100,
            selector_time_limit_seconds=20,
            experiment_seed="seed-7",
            selector_model_revision=MODEL_REVISION,
            embedding_model_revision="6c3ae70858513f1a78e9cdca3cae330d9075cd2a",
            embedding_manifest_hash=HASH_C,
        )
        change = CandidateChangeCard(
            parent_artifact_hash=parent_hash,
            child_artifact_hash=child_hash,
            diff_hash=diff_hash,
            changed_paths=("src/tool.ts",),
            changed_symbols=("tool",),
            dependency_change="none",
            mutation_summary="Validate tool results.",
            source_revision="child-1",
            created_at="2026-10-09T00:00:00Z",
        )
        spec = EmbeddingSpec(
            sidecar_url="http://127.0.0.1:9999/v1/embeddings",
            sidecar_manifest_hash=HASH_C,
        )
        embedder = FakeEmbeddingClient(
            spec, lambda _text, _role: self.vectors[self.catalogue.task_ids[0]]
        )
        selector = SelectorToolLoop(
            catalogue=self.catalogue,
            lexical_index=LexicalIndex(self.catalogue),
            semantic_index=SemanticIndex(self.catalogue, self.vectors, embedder),
            vectors=self.vectors,
            change=change,
            bad_cases=(),
            config=config,
            client=client,
        )
        evaluator = FakeRoundEvaluator()
        evaluator.parent_hash = parent_hash
        evaluator.child_hash = child_hash
        return (
            AdaptiveEvaluationController(
                run_id="test-run",
                catalogue=self.catalogue,
                config=config,
                selector_loop=selector,
                round_evaluator=evaluator,
                vectors=self.vectors,
                change_hash=diff_hash,
                parent_snapshot=parent_snapshot,
                child_snapshot=child_snapshot,
                output_root=output,
                progress_factory=lambda items, _description, _total: items,
            ),
            client,
            evaluator,
        )

    def test_audit_happens_after_selector_stop_and_manifest_reproduces(self) -> None:
        with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
            first_controller, first_client, first_evaluator = self.build_controller(Path(first_dir))
            second_controller, _, _ = self.build_controller(Path(second_dir))
            first = first_controller.run_selection()
            second = second_controller.run_selection()
            self.assertEqual(first.selection_manifest_hash, second.selection_manifest_hash)
            self.assertEqual(first.frozen_plan.final_task_ids, second.frozen_plan.final_task_ids)
            self.assertEqual(first_evaluator.calls[0][1], first.frozen_plan.pre_audit_task_ids)
            prompt = json.dumps(first_client.prompts)
            self.assertNotIn(first.audit.seed_derivation, prompt)
            self.assertNotIn("audit_seed", prompt)
            self.assertNotIn("audit_candidate_ids", prompt)
            self.assertNotIn("audit_task_ids", prompt)
            self.assertEqual(
                [event.event_type for event in first_controller.state.events],
                [
                    "round_frozen",
                    "round_pair_evidence",
                    "pre_audit_frozen",
                    "final_manifest_frozen",
                ],
            )


if __name__ == "__main__":
    unittest.main()
