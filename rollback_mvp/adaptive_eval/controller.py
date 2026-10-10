"""Top-level adaptive selection state machine; audit remains controller-private."""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence

from .audit_sampler import AuditSample, deterministic_audit, derive_audit_seed
from .coverage import facility_location_coverage, redundancy
from .diagnosis import validate_candidate_change_snapshots
from .paired_executor import FrozenTaskPlan, required_tqdm
from .schemas import (
    CatalogueManifest,
    ExperimentConfig,
    ValidationError,
    hash_json,
)
from .selector_agent import SelectorRound, SelectorToolLoop
from .state import AppendOnlyState, atomic_json, freeze_file_once


@dataclass(frozen=True, slots=True)
class SanitizedRoundPair:
    task_instance_id: str
    parent_resolved: bool
    child_resolved: bool
    pair_result_hash: str
    paired_identity_hash: str
    paired_identity_payload: dict[str, Any]

    def __post_init__(self) -> None:
        from .schemas import require_sha256

        require_sha256(self.pair_result_hash, "pair_result_hash")
        require_sha256(self.paired_identity_hash, "paired_identity_hash")
        if not isinstance(self.parent_resolved, bool) or not isinstance(
            self.child_resolved, bool
        ):
            raise ValidationError("Sanitized round pair outcomes must be boolean")
        if hash_json(self.paired_identity_payload) != self.paired_identity_hash:
            raise ValidationError("Round pair identity payload hash mismatch")


@dataclass(frozen=True, slots=True)
class RoundEvidence:
    round_id: int
    task_ids: tuple[str, ...]
    pairs: tuple[SanitizedRoundPair, ...]

    def __post_init__(self) -> None:
        if len(self.task_ids) != len(set(self.task_ids)):
            raise ValidationError("Round evidence task IDs contain duplicates")
        if tuple(pair.task_instance_id for pair in self.pairs) != self.task_ids:
            raise ValidationError(
                "Round evidence requires one ordered sanitized pair per task"
            )

    @property
    def public_summary(self) -> dict[str, Any]:
        return {
            "task_count": len(self.pairs),
            "child_only_wins": sum(
                not pair.parent_resolved and pair.child_resolved for pair in self.pairs
            ),
            "parent_only_wins": sum(
                pair.parent_resolved and not pair.child_resolved for pair in self.pairs
            ),
            "ties": sum(
                pair.parent_resolved == pair.child_resolved for pair in self.pairs
            ),
            "tasks": [
                {
                    "instance_id": pair.task_instance_id,
                    "parent_resolved": pair.parent_resolved,
                    "child_resolved": pair.child_resolved,
                }
                for pair in self.pairs
            ],
        }


class RoundEvaluator(Protocol):
    def evaluate_round(
        self, round_id: int, task_ids: Sequence[str]
    ) -> RoundEvidence: ...


@dataclass(frozen=True, slots=True)
class SelectionResult:
    rounds: tuple[SelectorRound, ...]
    audit: AuditSample
    frozen_plan: FrozenTaskPlan
    coverage: float
    redundancy: float
    selection_manifest_path: str
    selection_manifest_hash: str


class AdaptiveEvaluationController:
    def __init__(
        self,
        *,
        run_id: str,
        catalogue: CatalogueManifest,
        config: ExperimentConfig,
        selector_loop: SelectorToolLoop,
        round_evaluator: RoundEvaluator,
        vectors: Mapping[str, Sequence[float]],
        change_hash: str,
        parent_snapshot: Path,
        child_snapshot: Path,
        output_root: Path,
        progress_factory: Any = required_tqdm,
    ) -> None:
        output_root.mkdir(parents=True, exist_ok=True)
        atomic_json(
            output_root / "controller-preflight.json",
            {
                "schema_version": 1,
                "run_id": run_id,
                "catalogue_hash": catalogue.catalogue_hash,
                "dataset_manifest_hash": catalogue.dataset_manifest_hash,
                "config": dataclasses.asdict(config),
                "change": dataclasses.asdict(selector_loop.change),
                "parent_snapshot": str(parent_snapshot.resolve()),
                "child_snapshot": str(child_snapshot.resolve()),
            },
        )
        if not run_id:
            raise ValidationError("run_id must be non-empty")
        if selector_loop.catalogue != catalogue or selector_loop.config != config:
            raise ValidationError("Selector loop does not match controller catalogue/config")
        if change_hash != selector_loop.change.diff_hash:
            raise ValidationError("Controller change hash does not match selector change card")
        validate_candidate_change_snapshots(
            selector_loop.change, parent_snapshot, child_snapshot
        )
        if {key: tuple(value) for key, value in vectors.items()} != selector_loop.semantic_index.vectors:
            raise ValidationError("Controller coverage vectors differ from selector semantic vectors")
        self.run_id = run_id
        self.catalogue = catalogue
        self.config = config
        self.selector_loop = selector_loop
        self.round_evaluator = round_evaluator
        self.vectors = vectors
        self.change_hash = change_hash
        self.output_root = output_root
        self.progress_factory = progress_factory
        self.state = AppendOnlyState(output_root / "state")
        if self.state.events:
            raise ValidationError(
                "Existing adaptive state requires an explicit resume implementation; "
                "refusing to overwrite or infer state"
            )
        freeze_file_once(
            output_root / "controller-request.json",
            {
                "schema_version": 1,
                "run_id": run_id,
                "catalogue_hash": catalogue.catalogue_hash,
                "dataset_manifest_hash": catalogue.dataset_manifest_hash,
                "embedding_index_hash": catalogue.embedding_index_hash,
                "embedding_response_hash": catalogue.embedding_response_hash,
                "config": dataclasses.asdict(config),
                "config_hash": config.config_hash,
                "change": dataclasses.asdict(selector_loop.change),
                "bad_cases": [
                    dataclasses.asdict(card)
                    for card in sorted(
                        selector_loop.bad_cases.values(), key=lambda card: card.bad_case_id
                    )
                ],
            },
        )

    def run_selection(self) -> SelectionResult:
        try:
            return self._run_selection()
        except Exception as error:
            evidence = {
                "phase": "selection",
                "error_type": type(error).__name__,
                "message": str(error),
                "state_event_hashes": [event.event_hash for event in self.state.events],
                "selector_validation_failures": self.selector_loop.validation_failures,
                "selector_raw_turns": self.selector_loop.raw_turns,
            }
            atomic_json(self.output_root / "errors" / "selection-error.json", evidence)
            try:
                self.state.append("selection_error", evidence)
            except BaseException as persistence_error:
                raise ExceptionGroup(
                    "Selection failed and append-only error persistence also failed",
                    [error, persistence_error],
                ) from error
            raise

    def _run_selection(self) -> SelectionResult:
        rounds: list[SelectorRound] = []
        selected: list[str] = []
        summaries: dict[int, Mapping[str, Any]] = {}
        selector_tokens = 0
        selector_latency = 0.0
        terminal_reason = ""
        rounds_progress = self.progress_factory(
            range(self.config.max_rounds),
            "adaptive selector rounds",
            self.config.max_rounds,
        )
        for round_id in rounds_progress:
            if len(selected) >= self.config.task_budget:
                terminal_reason = "task_budget_exhausted"
                break
            round_record = self.selector_loop.run_round(
                round_id=round_id,
                selected_ids=selected,
                prior_round_summaries=summaries,
                prior_selector_tokens=selector_tokens,
                prior_selector_latency_seconds=selector_latency,
            )
            round_ids = tuple(
                selected_task.proposal.instance_id
                for selected_task in round_record.selected_tasks
            )
            if not round_ids:
                raise ValidationError("Selector round produced no executable tasks")
            self.state.append(
                "round_frozen",
                {
                    "round_id": round_id,
                    "selected_tasks": [
                        dataclasses.asdict(task) for task in round_record.selected_tasks
                    ],
                    "tool_calls": [
                        dataclasses.asdict(call) for call in round_record.tool_calls
                    ],
                    "prompts": round_record.prompts,
                    "stop_reason": round_record.stop_reason,
                    "stop_after_round": round_record.stop_after_round,
                },
            )
            evidence = self.round_evaluator.evaluate_round(round_id, round_ids)
            if evidence.round_id != round_id or evidence.task_ids != round_ids:
                raise ValidationError(
                    "Round evaluator returned evidence for a different immutable round"
                )
            for pair in evidence.pairs:
                identity = pair.paired_identity_payload
                card = self.catalogue.by_id[pair.task_instance_id]
                expected_identity_fields = {
                    "task_instance_id": pair.task_instance_id,
                    "task_repo": card.repo,
                    "task_base_commit": card.base_commit,
                    "parent_artifact_hash": self.selector_loop.change.parent_artifact_hash,
                    "child_artifact_hash": self.selector_loop.change.child_artifact_hash,
                    "dataset_manifest_hash": self.catalogue.dataset_manifest_hash,
                }
                for field, expected in expected_identity_fields.items():
                    if identity.get(field) != expected:
                        raise ValidationError(
                            f"Round pair identity {field} differs from controller request"
                        )
                expected_budgets = {
                    "timeout_seconds": self.config.per_task_timeout_seconds,
                    "token_budget": self.config.per_task_token_budget,
                    "retry_budget": self.config.per_task_retry_budget,
                    "tool_budget": self.config.per_task_tool_budget,
                }
                if identity.get("budgets") != expected_budgets:
                    raise ValidationError(
                        "Round pair execution budgets differ from frozen config"
                    )
            self.state.append(
                "round_pair_evidence", dataclasses.asdict(evidence)
            )
            summaries[round_id] = evidence.public_summary
            rounds.append(round_record)
            selected.extend(round_ids)
            selector_tokens += round_record.input_tokens + round_record.output_tokens
            selector_latency += round_record.latency_seconds
            if round_record.stop_after_round:
                terminal_reason = f"selector_stop:{round_record.stop_reason}"
                break
            if selector_tokens >= self.config.selector_token_budget:
                terminal_reason = "selector_token_budget_exhausted"
                break
            if selector_latency >= self.config.selector_time_limit_seconds:
                terminal_reason = "selector_time_budget_exhausted"
                break
        else:
            terminal_reason = "round_limit_exhausted"
        if not selected:
            raise ValidationError("Adaptive selector stopped without selecting any task")
        self.state.append(
            "pre_audit_frozen",
            {"task_ids": selected, "terminal_reason": terminal_reason},
        )

        audit_seed = derive_audit_seed(
            self.config.experiment_seed,
            self.selector_loop.change.parent_artifact_hash,
            self.selector_loop.change.child_artifact_hash,
            self.catalogue.catalogue_hash,
        )
        audit = deterministic_audit(
            self.catalogue.task_ids,
            selected,
            size=self.config.audit_size,
            seed_derivation=audit_seed,
        )
        final_ids = tuple(selected) + audit.audit_ids
        coverage_value = facility_location_coverage(
            final_ids, self.catalogue.task_ids, self.vectors
        )
        redundancy_report = redundancy(final_ids, self.vectors)
        selection_without_hash = {
            "schema_version": 1,
            "run_id": self.run_id,
            "parent_artifact_hash": self.selector_loop.change.parent_artifact_hash,
            "child_artifact_hash": self.selector_loop.change.child_artifact_hash,
            "dataset_manifest_hash": self.catalogue.dataset_manifest_hash,
            "catalogue_hash": self.catalogue.catalogue_hash,
            "change_hash": self.change_hash,
            "config_hash": self.config.config_hash,
            "selector_model_revision": self.config.selector_model_revision,
            "embedding_manifest_hash": self.config.embedding_manifest_hash,
            "embedding_index_hash": self.catalogue.embedding_index_hash,
            "embedding_response_hash": self.catalogue.embedding_response_hash,
            "config": dataclasses.asdict(self.config),
            "change": dataclasses.asdict(self.selector_loop.change),
            "embedding_index": {
                card.instance_id: {
                    "cache_key": card.embedding_id,
                    "vector_hash": card.embedding_vector_hash,
                }
                for card in self.catalogue.cards
            },
            "rounds": [
                {
                    "round_id": round_record.round_id,
                    "queries_and_tool_calls": [
                        dataclasses.asdict(call) for call in round_record.tool_calls
                    ],
                    "prompts": round_record.prompts,
                    "candidates": round_record.inspected_candidate_ids,
                    "proposals": [
                        dataclasses.asdict(item) for item in round_record.selected_tasks
                    ],
                    "pair_result_hashes": list(
                        next(
                            [
                                pair["pair_result_hash"]
                                for pair in event.payload["pairs"]
                            ]
                            for event in self.state.events
                            if event.event_type == "round_pair_evidence"
                            and event.payload["round_id"] == round_record.round_id
                        )
                    ),
                    "stop_reason": round_record.stop_reason,
                }
                for round_record in rounds
            ],
            "pre_audit_task_ids": selected,
            "audit_seed_derivation": audit.seed_derivation,
            "audit_candidate_ids": audit.candidate_ids,
            "audit_task_ids": audit.audit_ids,
            "final_task_ids": final_ids,
            "coverage": coverage_value,
            "redundancy": dataclasses.asdict(redundancy_report),
            "terminal_reason": terminal_reason,
        }
        selection_hash = hash_json(selection_without_hash)
        selection_manifest = selection_without_hash | {"manifest_hash": selection_hash}
        selection_path = self.output_root / "selection-manifest.json"
        freeze_file_once(selection_path, selection_manifest)
        self.state.append(
            "final_manifest_frozen",
            {
                "selection_manifest_hash": selection_hash,
                "final_task_ids": final_ids,
            },
        )
        plan = FrozenTaskPlan(
            schema_version=1,
            dataset_manifest_hash=self.catalogue.dataset_manifest_hash,
            catalogue_hash=self.catalogue.catalogue_hash,
            parent_artifact_hash=self.selector_loop.change.parent_artifact_hash,
            child_artifact_hash=self.selector_loop.change.child_artifact_hash,
            pre_audit_task_ids=tuple(selected),
            audit_task_ids=audit.audit_ids,
            final_task_ids=final_ids,
            selection_manifest_hash=selection_hash,
            config_hash=self.config.config_hash,
        )
        return SelectionResult(
            rounds=tuple(rounds),
            audit=audit,
            frozen_plan=plan,
            coverage=coverage_value,
            redundancy=redundancy_report.value,
            selection_manifest_path=str(selection_path),
            selection_manifest_hash=selection_hash,
        )
