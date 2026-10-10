from __future__ import annotations

import dataclasses
import json
import tempfile
import unittest
from pathlib import Path

from .audit_sampler import AuditSample
from .catalogue import load_frozen_catalogue
from .controller import SelectionResult
from .paired_executor import ArtifactRef, FrozenTaskPlan
from .pipeline import run_final_pipeline
from .schemas import DecisionPolicy, PairExecutionError, SCHEMA_VERSION


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


class FailingExecutor:
    def __init__(self, plan) -> None:
        self.plan = plan
        self.settings = None
        self.experiment_config = None

    def run_pairs(self, parent, child):
        raise PairExecutionError("incomplete pair evidence")


class PipelineInvalidStateTest(unittest.TestCase):
    def test_invalid_pair_enters_persisted_invalid_state(self) -> None:
        catalogue = load_frozen_catalogue(MANIFEST)
        task_ids = catalogue.task_ids[:2]
        plan = FrozenTaskPlan(
            schema_version=1,
            dataset_manifest_hash=catalogue.dataset_manifest_hash,
            catalogue_hash=catalogue.catalogue_hash,
            parent_artifact_hash=HASH_A,
            child_artifact_hash=HASH_B,
            pre_audit_task_ids=task_ids[:1],
            audit_task_ids=task_ids[1:],
            final_task_ids=task_ids,
            selection_manifest_hash=HASH_C,
            config_hash=HASH_D,
        )
        selection = SelectionResult(
            rounds=(),
            audit=AuditSample(HASH_E, tuple(catalogue.task_ids[1:]), task_ids[1:]),
            frozen_plan=plan,
            coverage=0.1,
            redundancy=0.0,
            selection_manifest_path="selection-manifest.json",
            selection_manifest_hash=HASH_C,
        )
        policy = DecisionPolicy(
            schema_version=SCHEMA_VERSION,
            confidence_level=0.95,
            bootstrap_seed=7,
            bootstrap_samples=100,
            acceptance_margin=0.1,
            rollback_margin=-0.1,
            audit_guard_min_delta=0.0,
            escalation_task_cap=10,
        )
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            selection_path = output / "selection-manifest.json"
            selection_path.write_text(json.dumps({"manifest_hash": HASH_C}))
            selection = dataclasses.replace(
                selection, selection_manifest_path=str(selection_path)
            )
            with self.assertRaisesRegex(PairExecutionError, "incomplete pair"):
                run_final_pipeline(
                    selection=selection,
                    executor=FailingExecutor(plan),
                    parent=ArtifactRef("parent", HASH_A, "/parent"),
                    child=ArtifactRef("child", HASH_B, "/child"),
                    policy=policy,
                    catalogue=catalogue,
                    vectors={task_id: (1.0, 0.0) for task_id in task_ids},
                    output_root=output,
                )
            self.assertTrue((output / "invalid-decision.json").is_file())
            event = output / "decision-state" / "events" / "000000.json"
            self.assertIn("decision_invalid", event.read_text())


if __name__ == "__main__":
    unittest.main()
