from __future__ import annotations

import dataclasses
import json
import sys
import tempfile
import unittest
from pathlib import Path

from rollback_mvp.dgm_evolve.experiment import (
    ArchiveEntry,
    ConfigurationError,
    CostLedger,
    DgmPiExperiment,
    ExperimentConfig,
    RuntimePaths,
    TaskObservation,
    build_split_contract,
    classify_runner_result,
    dgm_parent_weight,
    endpoint_order,
    mutation_failure_reason,
    select_parent_hashes,
    validate_evolve_manifest,
    validate_strategy,
)
from rollback_mvp.dgm_evolve.artifacts import (
    ArtifactValidationError,
    CandidateTool,
    MutationDelta,
    materialize_lineage,
    validate_candidate_tool,
)
from rollback_mvp.dgm_evolve.rf_clm import (
    apply_repair_plan,
    repair_first_lineage,
)
from rollback_mvp.adaptive_eval.schemas import hash_json
from rollback_mvp.adaptive_eval.state import atomic_json
from rollback_mvp.orchestrate_endpoint_200 import load_manifest


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = (
    ROOT
    / "research_output"
    / "clm_budgeted_evolution_20260924_125503"
    / "dgm_swebench_verified_200.v1.json"
)


def runtime_paths(output: Path) -> RuntimePaths:
    return RuntimePaths(
        repo_root=ROOT,
        full_manifest=MANIFEST,
        output_root=output,
        agent_dir=(
            ROOT
            / "research_output"
            / "clm_budgeted_evolution_20260924_125503"
            / "pi_home"
            / "agent"
        ),
        swebench_source=ROOT / "datasets" / "SWE-bench",
        image_builder=ROOT / "rollback_mvp" / "build_local_swebench_images.py",
        pi_runner=ROOT / "rollback_mvp" / "pi_swe_runner.mjs",
        mutation_runner=ROOT / "rollback_mvp" / "pi_strategy_mutator.mjs",
        swebench_python=sys.executable,
    )


class FakeDgmPiExperiment(DgmPiExperiment):
    def _mutate(self, parent_hash, slot, evolve_manifest, task_path):
        strategy = f"General strategy revision {slot}: inspect, edit, verify."
        child_hash = self._write_artifact(
            strategy=strategy,
            parent_hash=parent_hash,
            mutation_record={"kind": "fake", "slot": slot},
        )
        self.ledger.append(
            f"mutation:{slot:04d}",
            {
                "budget_scope": "search",
                "kind": "mutation_proposer",
                "reported_tokens": 10,
                "conservative_token_charge": 0,
                "active_seconds": 0.1,
                "api_calls": 1,
                "task_executions": 0,
                "status": "valid",
            },
        )
        return {
            "valid": True,
            "artifact_hash": child_hash,
            "parentArtifactHash": parent_hash,
        }

    def _evaluate_task(
        self,
        *,
        artifact_hash_value,
        entry,
        role_manifest,
        dataset_path,
        task_path,
        phase,
        budget_scope,
    ):
        instance_id = entry["record"]["instance_id"]
        p0_hash = self._load_json(self.output_root / "protocol-lock.json")[
            "p0_artifact_hash"
        ]
        identity_hash = hash_json(
            {
                "artifact": artifact_hash_value,
                "instance": instance_id,
                "phase": phase,
            }
        )
        unhashed = {
            "instance_id": instance_id,
            "artifact_hash": artifact_hash_value,
            "phase": phase,
            "resolved": artifact_hash_value != p0_hash,
            "status": "completed",
            "valid": True,
            "reported_tokens": 10,
            "token_telemetry_complete": True,
            "image_build_seconds": 0.0,
            "agent_duration_seconds": 0.1,
            "evaluator_duration_seconds": 0.1,
            "patch_sha256": "a" * 64,
            "identity_hash": identity_hash,
        }
        record = {**unhashed, "observation_hash": hash_json(unhashed)}
        path = (
            self.output_root
            / "observations"
            / phase
            / artifact_hash_value
            / instance_id
            / "observation.json"
        )
        atomic_json(path, record)
        self.ledger.append(
            f"task:{identity_hash}",
            {
                "budget_scope": budget_scope,
                "kind": "task_agent_and_evaluator",
                "reported_tokens": 10,
                "conservative_token_charge": 0,
                "active_seconds": 0.2,
                "api_calls": 1,
                "task_executions": 1,
                "status": "completed",
                "valid": True,
                "resolved": artifact_hash_value != p0_hash,
            },
        )
        return TaskObservation(**record)


class FakeP2GateExperiment(DgmPiExperiment):
    def _evaluate_records(
        self,
        *,
        artifact_hash_value,
        records,
        role_manifest,
        dataset_path,
        task_path,
        phase,
        budget_scope,
    ):
        mutation_ids = {
            delta.mutation_id
            for delta in self._artifact_lineage(artifact_hash_value)
        }
        failed = {
            "m-0001-aaaaaaaaaaaa",
            "m-0003-aaaaaaaaaaaa",
        } <= mutation_ids
        observations = []
        for entry in records:
            instance_id = entry["record"]["instance_id"]
            unhashed = {
                "instance_id": instance_id,
                "artifact_hash": artifact_hash_value,
                "phase": phase,
                "resolved": not failed,
                "status": "completed",
                "valid": True,
                "reported_tokens": 0,
                "token_telemetry_complete": True,
                "image_build_seconds": 0.0,
                "agent_duration_seconds": 0.0,
                "evaluator_duration_seconds": 0.0,
                "patch_sha256": "a" * 64,
                "identity_hash": hash_json(
                    {
                        "artifact": artifact_hash_value,
                        "task": instance_id,
                        "phase": phase,
                    }
                ),
            }
            observations.append(
                TaskObservation(
                    **{
                        **unhashed,
                        "observation_hash": hash_json(unhashed),
                    }
                )
            )
        return observations


class InvalidMutationExperiment(FakeDgmPiExperiment):
    def _mutate(self, parent_hash, slot, evolve_manifest, task_path):
        self.ledger.append(
            f"mutation:{slot:04d}",
            {
                "budget_scope": "search",
                "kind": "mutation_proposer",
                "reported_tokens": 10,
                "conservative_token_charge": 0,
                "active_seconds": 0.1,
                "api_calls": 1,
                "task_executions": 0,
                "status": "invalid",
            },
        )
        return {
            "valid": False,
            "parentArtifactHash": parent_hash,
            "budgetAborted": True,
            "tokenTelemetryAvailable": True,
        }


class SplitContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.full, cls.full_hash = load_manifest(MANIFEST)
        cls.evolve, cls.test, cls.binding = build_split_contract(
            cls.full, cls.full_hash
        )

    def test_literal_60_140_split_is_disjoint_and_hash_bound(self) -> None:
        validate_evolve_manifest(self.evolve)
        evolve_ids = {
            entry["record"]["instance_id"] for entry in self.evolve["records"]
        }
        test_ids = {
            entry["record"]["instance_id"] for entry in self.test["records"]
        }
        self.assertEqual(len(evolve_ids), 60)
        self.assertEqual(len(test_ids), 140)
        self.assertFalse(evolve_ids & test_ids)
        self.assertEqual(
            self.binding["test_ordered_ids_sha256"],
            self.test["ordered_instance_ids_sha256"],
        )

    def test_online_evolve_payload_contains_no_big_task_id(self) -> None:
        serialized = json.dumps(self.evolve, sort_keys=True)
        for entry in self.test["records"]:
            self.assertNotIn(entry["record"]["instance_id"], serialized)


class DgmPolicyTest(unittest.TestCase):
    def entry(
        self,
        artifact: str,
        score: float,
        children: int,
        ordinal: int,
    ) -> ArchiveEntry:
        return ArchiveEntry(
            artifact_hash=artifact,
            parent_artifact_hash=None,
            score_60=score,
            resolved_60=round(score * 60),
            evaluated_tasks=60,
            functioning_child_count=children,
            functioning_child_slots=tuple(range(children)),
            insertion_ordinal=ordinal,
        )

    def test_parent_weight_uses_score_and_child_count(self) -> None:
        fresh = self.entry("a" * 64, 0.6, 0, 0)
        explored = dataclasses.replace(fresh, functioning_child_count=3)
        stronger = self.entry("b" * 64, 0.8, 0, 1)
        self.assertAlmostEqual(
            dgm_parent_weight(explored),
            dgm_parent_weight(fresh) / 4,
        )
        self.assertGreater(dgm_parent_weight(stronger), dgm_parent_weight(fresh))

    def test_parent_draw_is_deterministic_with_replacement(self) -> None:
        entries = [
            self.entry("a" * 64, 0.5, 0, 0),
            self.entry("b" * 64, 0.6, 1, 1),
        ]
        first = select_parent_hashes(entries, seed=7, wave=2, count=20)
        second = select_parent_hashes(entries, seed=7, wave=2, count=20)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 20)
        self.assertTrue(set(first) <= {"a" * 64, "b" * 64})

    def test_functioning_child_count_is_slot_idempotent(self) -> None:
        parent = self.entry("a" * 64, 0.5, 0, 0)
        once = DgmPiExperiment._increment_child_count([parent], parent.artifact_hash, 3)
        twice = DgmPiExperiment._increment_child_count(
            once, parent.artifact_hash, 3
        )
        self.assertEqual(twice[0].functioning_child_count, 1)
        self.assertEqual(twice[0].functioning_child_slots, (3,))

    def test_endpoint_order_counterbalances_artifacts(self) -> None:
        artifacts = ("a" * 64, "b" * 64)
        orders = {
            endpoint_order(artifacts, f"repo__task-{index}", 7)
            for index in range(100)
        }
        self.assertEqual(
            orders,
            {
                ("a" * 64, "b" * 64),
                ("b" * 64, "a" * 64),
            },
        )

    def test_strategy_validation_rejects_task_specific_content(self) -> None:
        validate_strategy(
            "Inspect relevant code, make a minimal patch, and run focused tests.",
            ("repo__task-1",),
        )
        with self.assertRaisesRegex(ConfigurationError, "task ID"):
            validate_strategy("Always special-case repo__task-1.", ("repo__task-1",))
        with self.assertRaisesRegex(ConfigurationError, "benchmark-specific"):
            validate_strategy("Use the SWE-bench official evaluator.", ())

    def test_task_abort_is_observed_zero_and_never_graded(self) -> None:
        result = {
            "inputTokens": 10,
            "outputTokens": 20,
            "cacheReadTokens": 0,
            "cacheWriteTokens": 0,
            "tokenTelemetryAvailable": True,
            "budgetAborted": True,
            "timeoutAborted": False,
            "providerError": "This operation was aborted",
            "patch": "diff --git a/a b/a\n",
        }
        classification = classify_runner_result(result, 1)
        self.assertTrue(classification.valid)
        self.assertFalse(classification.should_grade_patch)
        self.assertEqual(
            classification.status,
            "task_budget_exhausted_observed_zero",
        )

    def test_provider_error_and_missing_telemetry_are_invalid(self) -> None:
        base = {
            "inputTokens": 10,
            "outputTokens": 20,
            "cacheReadTokens": 0,
            "cacheWriteTokens": 0,
            "tokenTelemetryAvailable": True,
            "budgetAborted": False,
            "timeoutAborted": False,
            "patch": "",
        }
        provider = classify_runner_result(
            {**base, "providerError": "403 rejected"},
            1,
        )
        self.assertFalse(provider.valid)
        missing = classify_runner_result(
            {**base, "tokenTelemetryAvailable": False},
            0,
        )
        self.assertFalse(missing.valid)

    def test_invalid_mutation_reason_is_total_for_budget_abort(self) -> None:
        self.assertEqual(
            mutation_failure_reason(
                {
                    "valid": False,
                    "budgetAborted": True,
                    "tokenTelemetryAvailable": True,
                }
            ),
            "Mutation proposer exceeded its frozen token budget.",
        )
        self.assertEqual(
            mutation_failure_reason(
                {
                    "valid": False,
                    "parseError": "invalid JSON",
                    "tokenTelemetryAvailable": True,
                }
            ),
            "invalid JSON",
        )

    def test_matched_pilot_defaults_to_ten_slots_without_global_token_stop(
        self,
    ) -> None:
        config = ExperimentConfig(run_id="pilot", experiment_seed=7)
        self.assertEqual(config.proposal_slots, 10)
        self.assertIsNone(config.search_token_cap)

    def test_dgm_and_p2_share_execution_budgets(self) -> None:
        dgm = ExperimentConfig(run_id="dgm", experiment_seed=7, arm="dgm")
        p2 = ExperimentConfig(run_id="p2", experiment_seed=7, arm="p2")
        budget_fields = (
            "proposal_slots",
            "proposals_per_wave",
            "search_token_cap",
            "search_active_seconds_cap",
            "per_task_token_cap",
            "per_task_output_token_cap",
            "mutation_token_cap",
            "mutation_output_token_cap",
            "agent_timeout_seconds",
            "mutation_timeout_seconds",
        )
        self.assertEqual(
            tuple(getattr(dgm, field) for field in budget_fields),
            tuple(getattr(p2, field) for field in budget_fields),
        )


class ArtifactAndRfClmTest(unittest.TestCase):
    def delta(
        self,
        ordinal: int,
        *,
        strategy: str = "",
        tool_name: str | None = None,
        depends_on: tuple[str, ...] = (),
    ) -> MutationDelta:
        tool = (
            None
            if tool_name is None
            else CandidateTool(
                name=tool_name,
                label=f"Tool {ordinal}",
                description="Inspect repository text deterministically.",
                parameters={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                    },
                    "required": ["path"],
                    "additionalProperties": False,
                },
                handler_code=(
                    "import json\n"
                    "import sys\n"
                    "request = json.load(sys.stdin)\n"
                    "print(json.dumps({'content': request['path']}))\n"
                ),
                timeout_seconds=30,
            )
        )
        return MutationDelta(
            mutation_id=f"m-{ordinal:04d}-{'a' * 12}",
            repo="django/django",
            entry_task_id="django__django-10973",
            mutation_summary=f"General change {ordinal}.",
            strategy_patch=strategy,
            tool=tool,
            depends_on=depends_on,
        )

    def test_artifact_materializes_strategy_and_human_readable_tool(self) -> None:
        lineage = (
            self.delta(1, strategy="Inspect the relevant implementation."),
            self.delta(2, tool_name="inspect_text"),
        )
        content = materialize_lineage(lineage, ("django__django-10973",))
        self.assertIn("Inspect the relevant implementation.", content.strategy)
        self.assertEqual(content.tools[0].name, "inspect_text")
        self.assertEqual(
            content.tools_manifest["tools"][0]["handler"],
            "handlers/inspect_text.py",
        )

    def test_tool_validation_rejects_host_or_subprocess_capabilities(self) -> None:
        unsafe = dataclasses.replace(
            self.delta(1, tool_name="inspect_text").tool,
            handler_code="import subprocess\nsubprocess.run(['sh'])\n",
        )
        assert unsafe is not None
        with self.assertRaisesRegex(ArtifactValidationError, "import"):
            validate_candidate_tool(unsafe, ())

    def test_rf_clm_removes_earlier_cause_and_replays_independent_change(
        self,
    ) -> None:
        first = self.delta(1, tool_name="inspect_text")
        independent = self.delta(2, strategy="Verify the narrowest behavior.")
        interacting = self.delta(3, tool_name="inspect_text")
        lineage = (first, independent, interacting)
        result = repair_first_lineage(
            lineage,
            fails_with_active=lambda active: (
                first.mutation_id in active and interacting.mutation_id in active
            ),
            prior_order=(first.mutation_id,),
            singleton_budget=1,
        )
        self.assertEqual(result.method, "singleton-removal")
        self.assertEqual(result.removed_mutation_ids, (first.mutation_id,))
        self.assertIsNotNone(result.plan)
        assert result.plan is not None
        self.assertEqual(result.plan.replay_mutation_ids, (independent.mutation_id,))
        self.assertEqual(
            apply_repair_plan((), lineage, result.plan),
            (independent,),
        )

    def test_p2_gate_materializes_verified_multigeneration_repair(self) -> None:
        full, full_hash = load_manifest(MANIFEST)
        evolve, _, _ = build_split_contract(full, full_hash)
        entry = evolve["records"][0]
        task_id = entry["record"]["instance_id"]
        repo = entry["record"]["repo"]
        first = dataclasses.replace(
            self.delta(1, strategy="Inspect the relevant implementation."),
            entry_task_id=task_id,
            repo=repo,
        )
        independent = dataclasses.replace(
            self.delta(2, strategy="Verify the narrowest behavior."),
            entry_task_id=task_id,
            repo=repo,
        )
        interacting = dataclasses.replace(
            self.delta(
                3,
                tool_name="inspect_text",
                depends_on=(first.mutation_id,),
            ),
            entry_task_id=task_id,
            repo=repo,
        )
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            atomic_json(
                output / "frozen-inputs" / "evolve-60-manifest.json",
                evolve,
            )
            experiment = FakeP2GateExperiment(
                ExperimentConfig(
                    run_id="p2-gate",
                    experiment_seed=7,
                    arm="p2",
                    proposal_slots=2,
                    proposals_per_wave=2,
                    inter_task_delay_seconds=0,
                ),
                runtime_paths(output),
                progress_factory=lambda items, _description, _total: items,
            )
            parent_hash = experiment._write_artifact(
                lineage=(first, independent),
                parent_hash=None,
                mutation_record={"kind": "test parent"},
            )
            child_hash = experiment._write_artifact(
                lineage=(first, independent, interacting),
                parent_hash=parent_hash,
                mutation_record={"kind": "test child"},
            )
            gate = experiment._apply_p2_gate(
                parent_hash=parent_hash,
                child_hash=child_hash,
                mutation={
                    "probe_task_ids": (task_id,),
                    "repo": repo,
                },
                slot=0,
                evolve_manifest=evolve,
                dataset_path=Path(temporary) / "dataset.json",
                task_path=Path(temporary) / "tasks.json",
            )
            self.assertTrue(gate["accepted"])
            self.assertEqual(gate["terminal_state"], "RF_CLM_REPAIRED")
            self.assertEqual(
                gate["rf_clm"]["removed_mutation_ids"],
                (first.mutation_id,),
            )
            repaired = experiment._artifact_lineage(gate["artifact_hash"])
            self.assertEqual(repaired, (independent,))


class LedgerAndPreparationTest(unittest.TestCase):
    def test_cost_ledger_rejects_tampering_and_deduplicates_charge(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "ledger.jsonl"
            ledger = CostLedger(path)
            payload = {
                "budget_scope": "search",
                "reported_tokens": 11,
                "conservative_token_charge": 0,
                "active_seconds": 1.5,
                "api_calls": 1,
                "task_executions": 0,
            }
            ledger.append("call-1", payload)
            ledger.append("call-1", payload)
            self.assertEqual(len(path.read_text().splitlines()), 1)
            self.assertEqual(ledger.totals("search")["budget_counted_tokens"], 11)
            record = json.loads(path.read_text())
            record["payload"]["reported_tokens"] = 12
            path.write_text(json.dumps(record) + "\n")
            with self.assertRaisesRegex(ConfigurationError, "hash mismatch"):
                CostLedger(path)

    def test_duplicate_strategy_keeps_intrinsic_artifact_and_two_provenances(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            experiment = DgmPiExperiment(
                ExperimentConfig(
                    run_id="duplicate-artifact",
                    experiment_seed=7,
                    proposal_slots=2,
                    proposals_per_wave=2,
                ),
                runtime_paths(output),
                progress_factory=lambda items, _description, _total: items,
            )
            first = experiment._write_artifact(
                strategy="Inspect, edit, verify.",
                parent_hash="a" * 64,
                mutation_record={"kind": "fake", "slot": 0},
            )
            second = experiment._write_artifact(
                strategy="Inspect, edit, verify.",
                parent_hash="b" * 64,
                mutation_record={"kind": "fake", "slot": 1},
            )
            self.assertEqual(first, second)
            self.assertEqual(
                len(list((output / "artifact-proposals" / first).glob("*.json"))),
                2,
            )

    def test_prepare_materializes_only_evolve_content_for_search(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            config = ExperimentConfig(
                run_id="test-prepare",
                experiment_seed=7,
                proposal_slots=2,
                proposals_per_wave=2,
            )
            paths = runtime_paths(output)
            experiment = DgmPiExperiment(
                config,
                paths,
                progress_factory=lambda items, _description, _total: items,
            )
            experiment.prepare()
            result = experiment.preflight(require_paid_runtime=False)
            self.assertTrue(result["valid"])
            self.assertFalse(
                (output / "frozen-inputs" / "test-140-manifest.json").exists()
            )
            frozen_text = "\n".join(
                path.read_text()
                for path in (output / "frozen-inputs").glob("*.json")
            )
            full, full_hash = load_manifest(MANIFEST)
            _, test, _ = build_split_contract(full, full_hash)
            for entry in test["records"]:
                self.assertNotIn(entry["record"]["instance_id"], frozen_text)

    def test_fake_end_to_end_search_seals_before_endpoint_and_reports_gain(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            config = ExperimentConfig(
                run_id="fake-e2e",
                experiment_seed=7,
                proposal_slots=2,
                proposals_per_wave=2,
                search_token_cap=500_000,
                final_endpoint_token_cap=250_000,
                reference_endpoint_token_cap=250_000,
                per_task_token_cap=64_000,
                per_task_output_token_cap=16_384,
                mutation_token_cap=32_000,
                mutation_output_token_cap=8_192,
                inter_task_delay_seconds=0,
                smoke=True,
                smoke_small_tasks=1,
                smoke_medium_tasks=0,
                smoke_endpoint_tasks=2,
            )
            experiment = FakeDgmPiExperiment(
                config,
                runtime_paths(output),
                progress_factory=lambda items, _description, _total: items,
            )
            experiment.prepare()
            self.assertFalse(
                (output / "endpoints" / "frozen-inputs" / "test-140-manifest.json").exists()
            )
            seal = experiment.run_search()
            self.assertEqual(seal["completed_proposal_slots"], 2)
            self.assertEqual(seal["archive_entries"], 3)
            self.assertEqual(seal["search_cost"]["reported_tokens"], 50)
            self.assertEqual(seal["search_cost"]["budget_counted_tokens"], 50)
            self.assertTrue((output / "search-seal.json").exists())
            summary = experiment.run_endpoint()
            self.assertEqual(summary["tasks"], 2)
            self.assertEqual(summary["p0_reference"]["resolved"], 0)
            self.assertEqual(summary["final_harness"]["resolved"], 2)
            self.assertEqual(summary["paired"]["absolute_accuracy_difference"], 1.0)

    def test_invalid_mutations_without_error_field_advance_and_seal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            config = ExperimentConfig(
                run_id="invalid-mutations",
                experiment_seed=7,
                proposal_slots=2,
                proposals_per_wave=2,
                inter_task_delay_seconds=0,
                smoke=True,
                smoke_small_tasks=1,
                smoke_medium_tasks=0,
                smoke_endpoint_tasks=1,
            )
            experiment = InvalidMutationExperiment(
                config,
                runtime_paths(output),
                progress_factory=lambda items, _description, _total: items,
            )
            experiment.prepare()
            seal = experiment.run_search()
            self.assertEqual(seal["completed_proposal_slots"], 2)
            self.assertEqual(seal["archive_entries"], 1)
            self.assertEqual(
                json.loads(
                    (
                        output
                        / "search"
                        / "slots"
                        / "0000"
                        / "terminal.json"
                    ).read_text()
                )["reason"],
                "Mutation proposer exceeded its frozen token budget.",
            )


if __name__ == "__main__":
    unittest.main()
