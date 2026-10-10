from __future__ import annotations

import dataclasses
import json
import tempfile
import unittest
from pathlib import Path

from .catalogue import load_frozen_catalogue
from .decision import decide
from .paired_executor import (
    ArtifactRef,
    ExecutionSettings,
    FakeArtifactRunner,
    FrozenTaskPlan,
    ModelSettings,
    PairedExecutor,
)
from .schemas import (
    DecisionOutcome,
    DecisionPolicy,
    PairExecutionError,
    SCHEMA_VERSION,
    ExperimentConfig,
    hash_json,
)


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


def plain_progress(items, _description: str, _total: int):
    return items


class PairedDecisionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalogue = load_frozen_catalogue(MANIFEST)
        cls.task_ids = cls.catalogue.task_ids[:3]
        cls.settings = ExecutionSettings(
            model=ModelSettings(
                provider="fake",
                model_id="fake-model",
                model_revision="fake-revision",
                inference_settings=(("temperature", "0"),),
            ),
            timeout_seconds=60,
            token_budget=1000,
            retry_budget=0,
            tool_budget=20,
            runner_image="runner@sha256",
            runner_image_digest=HASH_C,
            evaluator_image="evaluator@sha256",
            evaluator_image_digest=HASH_D,
            runner_revision="runner-v1",
            evaluator_revision="evaluator-v1",
            container_policy_hash=HASH_E,
        )
        cls.parent = ArtifactRef("parent", HASH_A, "/artifacts/parent")
        cls.child = ArtifactRef("child", HASH_B, "/artifacts/child")
        cls.policy = DecisionPolicy(
            schema_version=SCHEMA_VERSION,
            confidence_level=0.95,
            bootstrap_seed=7,
            bootstrap_samples=500,
            acceptance_margin=0.1,
            rollback_margin=-0.1,
            audit_guard_min_delta=0.0,
            escalation_task_cap=20,
        )
        cls.config = ExperimentConfig(
            schema_version=SCHEMA_VERSION,
            task_budget=2,
            max_rounds=2,
            max_tasks_per_round=2,
            audit_size=1,
            max_tool_calls_per_round=5,
            per_task_timeout_seconds=60,
            per_task_token_budget=1000,
            per_task_retry_budget=0,
            per_task_tool_budget=20,
            selector_token_budget=100,
            selector_time_limit_seconds=10,
            experiment_seed="seed",
            selector_model_revision="selector-v1",
            embedding_model_revision="6c3ae70858513f1a78e9cdca3cae330d9075cd2a",
            embedding_manifest_hash=HASH_C,
        )
        cls.selection_without_hash = {
            "dataset_manifest_hash": cls.catalogue.dataset_manifest_hash,
            "catalogue_hash": cls.catalogue.catalogue_hash,
            "parent_artifact_hash": HASH_A,
            "child_artifact_hash": HASH_B,
            "config_hash": cls.config.config_hash,
            "final_task_ids": list(cls.task_ids),
            "pre_audit_task_ids": list(cls.task_ids[:2]),
            "audit_task_ids": list(cls.task_ids[2:]),
        }
        cls.selection_hash = hash_json(cls.selection_without_hash)

    def plan(self) -> FrozenTaskPlan:
        return FrozenTaskPlan(
            schema_version=1,
            dataset_manifest_hash=self.catalogue.dataset_manifest_hash,
            catalogue_hash=self.catalogue.catalogue_hash,
            parent_artifact_hash=HASH_A,
            child_artifact_hash=HASH_B,
            pre_audit_task_ids=self.task_ids[:2],
            audit_task_ids=self.task_ids[2:],
            final_task_ids=self.task_ids,
            selection_manifest_hash=self.selection_hash,
            config_hash=self.config.config_hash,
        )

    def execute_pairs(self, parent_values, child_values):
        outcomes = {}
        for task_id, parent, child in zip(self.task_ids, parent_values, child_values):
            outcomes[(task_id, "parent")] = parent
            outcomes[(task_id, "child")] = child
        temporary = tempfile.TemporaryDirectory()
        selection_path = Path(temporary.name) / "selection-manifest.json"
        selection_path.write_text(
            json.dumps(self.selection_without_hash | {"manifest_hash": self.selection_hash})
        )
        runner = FakeArtifactRunner(outcomes)
        executor = PairedExecutor(
            catalogue=self.catalogue,
            plan=self.plan(),
            settings=self.settings,
            experiment_config=self.config,
            selection_manifest_path=selection_path,
            runner=runner,
            output_root=Path(temporary.name),
            progress_factory=plain_progress,
        )
        pairs = executor.run_pairs(self.parent, self.child)
        return temporary, executor, runner, pairs

    def test_accept_rollback_and_escalate(self) -> None:
        accepted = self.execute_pairs((False, False, False), (True, True, True))
        try:
            result = decide(
                self.plan(), accepted[3], self.policy, self.catalogue, self.settings, self.config
            )
            self.assertEqual(result.outcome, DecisionOutcome.ACCEPT)
            self.assertEqual(result.child_only_wins, 3)
            self.assertEqual(result.confidence_interval, (1.0, 1.0))
        finally:
            accepted[0].cleanup()

        rolled_back = self.execute_pairs((True, True, True), (False, False, False))
        try:
            result = decide(
                self.plan(), rolled_back[3], self.policy, self.catalogue, self.settings, self.config
            )
            self.assertEqual(result.outcome, DecisionOutcome.ROLLBACK)
        finally:
            rolled_back[0].cleanup()

        escalated = self.execute_pairs((False, True, False), (True, False, False))
        try:
            result = decide(
                self.plan(), escalated[3], self.policy, self.catalogue, self.settings, self.config
            )
            self.assertEqual(result.outcome, DecisionOutcome.ESCALATE)
            self.assertEqual(result.expansion_task_cap, 20)
        finally:
            escalated[0].cleanup()

    def test_identity_contains_all_required_execution_dimensions(self) -> None:
        run = self.execute_pairs((False, False, False), (True, True, True))
        try:
            request = run[2].requests[0]
            identity = request.identity_payload
            self.assertEqual(identity["task_instance_id"], request.task_instance_id)
            self.assertEqual(identity["parent_artifact_hash"], HASH_A)
            self.assertEqual(identity["child_artifact_hash"], HASH_B)
            self.assertEqual(identity["model"]["model_revision"], "fake-revision")
            self.assertEqual(identity["budgets"]["token_budget"], 1000)
            self.assertEqual(identity["runner"]["image_digest"], HASH_C)
            self.assertEqual(identity["evaluator"]["image_digest"], HASH_D)
            self.assertEqual(identity["container_policy_hash"], HASH_E)
        finally:
            run[0].cleanup()

    def test_wrong_runner_identity_is_terminal_and_persisted(self) -> None:
        outcomes = {
            (task_id, role): False
            for task_id in self.task_ids
            for role in ("parent", "child")
        }
        with tempfile.TemporaryDirectory() as temporary:
            selection_path = Path(temporary) / "selection-manifest.json"
            selection_path.write_text(
                json.dumps(self.selection_without_hash | {"manifest_hash": self.selection_hash})
            )
            executor = PairedExecutor(
                catalogue=self.catalogue,
                plan=self.plan(),
                settings=self.settings,
                experiment_config=self.config,
                selection_manifest_path=selection_path,
                runner=FakeArtifactRunner(outcomes, identity_override=HASH_E),
                output_root=Path(temporary),
                progress_factory=plain_progress,
            )
            with self.assertRaisesRegex(PairExecutionError, "wrong execution identity"):
                executor.run_pairs(self.parent, self.child)
            mismatch = list(Path(temporary).glob("pairs/*/*/identity-mismatch.json"))
            self.assertEqual(len(mismatch), 1)

    def test_incomplete_duplicate_or_cross_manifest_pairs_are_invalid(self) -> None:
        run = self.execute_pairs((False, False, False), (True, True, True))
        try:
            with self.assertRaisesRegex(PairExecutionError, "exactly match final manifest"):
                decide(
                    self.plan(), run[3][:-1], self.policy, self.catalogue, self.settings, self.config
                )
            with self.assertRaisesRegex(PairExecutionError, "Duplicate pair"):
                decide(
                    self.plan(),
                    (run[3][0], run[3][0], run[3][2]),
                    self.policy,
                    self.catalogue,
                    self.settings,
                    self.config,
                )
            changed = dataclasses.replace(run[3][0], final_manifest_hash=HASH_E)
            with self.assertRaisesRegex(PairExecutionError, "Pair result hash mismatch"):
                decide(
                    self.plan(),
                    (changed, *run[3][1:]),
                    self.policy,
                    self.catalogue,
                    self.settings,
                    self.config,
                )
        finally:
            run[0].cleanup()

    def test_counterfactual_rejects_different_final_task_plan(self) -> None:
        run = self.execute_pairs((False, False, False), (True, True, True))
        try:
            different = dataclasses.replace(
                self.plan(),
                pre_audit_task_ids=(self.task_ids[0],),
                final_task_ids=(self.task_ids[0], self.task_ids[2]),
            )
            counterfactual = ArtifactRef("counterfactual", HASH_E, "/counterfactual")
            with self.assertRaisesRegex(PairExecutionError, "identical frozen final"):
                run[1].run_counterfactual(counterfactual, different)
        finally:
            run[0].cleanup()

    def test_selection_manifest_tampering_and_budget_mismatch_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            selection_path = Path(temporary) / "selection-manifest.json"
            selection_path.write_text(
                json.dumps(
                    self.selection_without_hash
                    | {"manifest_hash": self.selection_hash, "tampered": True}
                )
            )
            with self.assertRaisesRegex(PairExecutionError, "content/hash"):
                PairedExecutor(
                    catalogue=self.catalogue,
                    plan=self.plan(),
                    settings=self.settings,
                    experiment_config=self.config,
                    selection_manifest_path=selection_path,
                    runner=FakeArtifactRunner({}),
                    output_root=Path(temporary) / "out",
                    progress_factory=plain_progress,
                )

            selection_path.write_text(
                json.dumps(
                    self.selection_without_hash | {"manifest_hash": self.selection_hash}
                )
            )
            relabelled = dataclasses.replace(
                self.plan(),
                pre_audit_task_ids=self.task_ids[:1],
                audit_task_ids=self.task_ids[1:],
            )
            with self.assertRaisesRegex(PairExecutionError, "pre_audit_task_ids"):
                PairedExecutor(
                    catalogue=self.catalogue,
                    plan=relabelled,
                    settings=self.settings,
                    experiment_config=self.config,
                    selection_manifest_path=selection_path,
                    runner=FakeArtifactRunner({}),
                    output_root=Path(temporary) / "out-relabelled",
                    progress_factory=plain_progress,
                )

            selection_path.write_text(
                json.dumps(
                    self.selection_without_hash | {"manifest_hash": self.selection_hash}
                )
            )
            mismatched = dataclasses.replace(self.settings, token_budget=999)
            with self.assertRaisesRegex(PairExecutionError, "experiment budgets"):
                PairedExecutor(
                    catalogue=self.catalogue,
                    plan=self.plan(),
                    settings=mismatched,
                    experiment_config=self.config,
                    selection_manifest_path=selection_path,
                    runner=FakeArtifactRunner({}),
                    output_root=Path(temporary) / "out2",
                    progress_factory=plain_progress,
                )

    def test_pair_hash_tampering_is_invalid(self) -> None:
        run = self.execute_pairs((False, False, False), (True, True, True))
        try:
            changed = dataclasses.replace(run[3][0], pair_hash=HASH_E)
            with self.assertRaisesRegex(PairExecutionError, "Pair result hash mismatch"):
                decide(
                    self.plan(),
                    (changed, *run[3][1:]),
                    self.policy,
                    self.catalogue,
                    self.settings,
                    self.config,
                )
        finally:
            run[0].cleanup()


if __name__ == "__main__":
    unittest.main()
