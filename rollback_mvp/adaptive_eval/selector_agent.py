"""Fail-closed selector tool loop with deterministic proposal arbitration."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import time
from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence

from .coverage import greedy_by_marginal_coverage, marginal_coverage
from .retrieval import LexicalIndex, RetrievalHit, SemanticIndex
from .schemas import (
    BadCaseCard,
    CandidateChangeCard,
    CatalogueManifest,
    ExperimentConfig,
    RetrievalRole,
    SelectedTask,
    SelectorError,
    TaskProposal,
    ValidationError,
)
from .trajectory import require_public_text


TOOL_SCHEMAS: tuple[dict[str, Any], ...] = (
    {"name": "search_lexical", "required": {"query": "string", "filters": "object", "limit": "positive_integer"}},
    {"name": "search_semantic", "required": {"query": "string", "limit": "positive_integer"}},
    {"name": "get_task", "required": {"instance_id": "string"}},
    {"name": "get_bad_case", "required": {"bad_case_id": "string"}},
    {"name": "get_change", "required": {}},
    {
        "name": "marginal_coverage",
        "required": {"candidate_ids": "string_array", "selected_ids": "string_array", "universe": "string_array"},
    },
    {"name": "inspect_round_results", "required": {"round_id": "nonnegative_integer"}},
    {"name": "propose_tasks", "required": {"proposals": "proposal_array"}},
    {"name": "finish_round", "required": {"stop_reason": "string", "stop_after_round": "boolean"}},
)
TOOL_BY_NAME = {tool["name"]: tool for tool in TOOL_SCHEMAS}


@dataclass(frozen=True, slots=True)
class SelectorTurn:
    raw_response: str
    model_revision: str
    input_tokens: int
    output_tokens: int
    cost: float
    latency_seconds: float

    def __post_init__(self) -> None:
        if any(
            not math.isfinite(value) or value < 0
            for value in (self.input_tokens, self.output_tokens, self.cost, self.latency_seconds)
        ):
            raise SelectorError("Selector usage values cannot be negative")
        if not self.raw_response:
            raise SelectorError("Selector returned an empty response")


class SelectorClient(Protocol):
    def next_action(
        self,
        prompt: Mapping[str, Any],
        tools: Sequence[Mapping[str, Any]],
        *,
        timeout_seconds: float,
    ) -> SelectorTurn: ...


class ScriptedSelectorClient:
    def __init__(self, turns: Sequence[SelectorTurn]) -> None:
        self.turns = list(turns)
        self.prompts: list[dict[str, Any]] = []
        self.tool_schemas: list[tuple[Mapping[str, Any], ...]] = []

    def next_action(
        self,
        prompt: Mapping[str, Any],
        tools: Sequence[Mapping[str, Any]],
        *,
        timeout_seconds: float,
    ) -> SelectorTurn:
        if timeout_seconds <= 0:
            raise SelectorError("Scripted selector received an exhausted timeout")
        self.prompts.append(dict(prompt))
        self.tool_schemas.append(tuple(tools))
        if not self.turns:
            raise SelectorError("Scripted selector has no remaining turn")
        return self.turns.pop(0)


@dataclass(frozen=True, slots=True)
class ToolCallRecord:
    call_id: str
    tool: str
    arguments: dict[str, Any]
    result: Any
    prompt_hash: str
    raw_response: str
    response_hash: str
    input_tokens: int
    output_tokens: int
    cost: float
    latency_seconds: float


@dataclass(frozen=True, slots=True)
class SelectorRound:
    round_id: int
    selected_tasks: tuple[SelectedTask, ...]
    tool_calls: tuple[ToolCallRecord, ...]
    prompts: tuple[dict[str, Any], ...]
    inspected_candidate_ids: tuple[str, ...]
    stop_reason: str
    stop_after_round: bool
    input_tokens: int
    output_tokens: int
    cost: float
    latency_seconds: float


def _result_payload(hit: RetrievalHit) -> dict[str, Any]:
    return dataclasses.asdict(hit)


def _parse_action(turn: SelectorTurn, expected_revision: str) -> tuple[str, dict[str, Any]]:
    if turn.model_revision != expected_revision:
        raise SelectorError(
            f"Selector model revision mismatch: expected {expected_revision}, "
            f"found {turn.model_revision}"
        )
    try:
        action = json.loads(turn.raw_response)
    except json.JSONDecodeError as error:
        raise SelectorError(f"Selector response is invalid JSON: {error}") from error
    if not isinstance(action, dict) or set(action) != {"tool", "arguments"}:
        raise SelectorError("Selector action must contain exactly tool and arguments")
    tool = action["tool"]
    arguments = action["arguments"]
    if tool not in TOOL_BY_NAME:
        raise SelectorError(f"Unknown selector tool: {tool!r}")
    if not isinstance(arguments, dict):
        raise SelectorError("Selector tool arguments must be an object")
    required = set(TOOL_BY_NAME[tool]["required"])
    if set(arguments) != required:
        raise SelectorError(
            f"{tool} arguments must be exactly {sorted(required)}, found {sorted(arguments)}"
        )
    type_contract = TOOL_BY_NAME[tool]["required"]
    for name, expected_type in type_contract.items():
        value = arguments[name]
        valid = {
            "string": isinstance(value, str) and bool(value),
            "object": isinstance(value, dict),
            "positive_integer": (
                isinstance(value, int) and not isinstance(value, bool) and value > 0
            ),
            "nonnegative_integer": (
                isinstance(value, int) and not isinstance(value, bool) and value >= 0
            ),
            "string_array": (
                isinstance(value, list)
                and all(isinstance(item, str) and item for item in value)
            ),
            "proposal_array": isinstance(value, list),
            "boolean": isinstance(value, bool),
        }[expected_type]
        if not valid:
            raise SelectorError(f"{tool}.{name} must be {expected_type}")
    return tool, arguments


class SelectorToolLoop:
    def __init__(
        self,
        *,
        catalogue: CatalogueManifest,
        lexical_index: LexicalIndex,
        semantic_index: SemanticIndex,
        vectors: Mapping[str, Sequence[float]],
        change: CandidateChangeCard,
        bad_cases: Sequence[BadCaseCard],
        config: ExperimentConfig,
        client: SelectorClient,
    ) -> None:
        self.catalogue = catalogue
        if any(
            not card.embedding_id or not card.embedding_vector_hash
            for card in catalogue.cards
        ):
            raise ValidationError(
                "Selector requires a catalogue bound to validated embedding cache entries"
            )
        if not catalogue.embedding_index_hash or not catalogue.embedding_response_hash:
            raise ValidationError("Selector catalogue lacks embedding index identity")
        self.lexical_index = lexical_index
        self.semantic_index = semantic_index
        self.vectors = vectors
        if catalogue.task_ids != tuple(semantic_index.vectors):
            raise ValidationError("Semantic index order/IDs differ from the catalogue")
        if vectors is not semantic_index.vectors and {key: tuple(value) for key, value in vectors.items()} != semantic_index.vectors:
            raise ValidationError("Coverage vectors differ from the semantic index")
        self.change = change
        for field_name in (
            "dependency_change",
            "mutation_summary",
            "source_revision",
        ):
            require_public_text(getattr(change, field_name), f"change.{field_name}")
        for value in (*change.changed_paths, *change.changed_symbols):
            require_public_text(value, "change path/symbol")
        self.bad_cases = {card.bad_case_id: card for card in bad_cases}
        if len(self.bad_cases) != len(bad_cases):
            raise ValidationError("Duplicate bad_case_id values")
        if any(card.parent_artifact_hash != change.parent_artifact_hash for card in bad_cases):
            raise ValidationError("Bad case belongs to a different parent artifact")
        for card in bad_cases:
            for field_name in (
                "outcome",
                "failure_taxonomy",
                "trajectory_summary",
                "public_test_summary",
            ):
                require_public_text(getattr(card, field_name), f"bad_case.{field_name}")
            for value in (*card.tool_error_fingerprints, *card.changed_paths):
                require_public_text(value, "bad_case fingerprint/path")
        self.config = config
        if config.embedding_manifest_hash != semantic_index.client.spec.sidecar_manifest_hash:
            raise ValidationError("Config embedding manifest hash differs from semantic sidecar")
        if config.embedding_model_revision != semantic_index.client.spec.model_revision:
            raise ValidationError("Config embedding revision differs from semantic sidecar")
        self.client = client
        self.validation_failures: list[dict[str, Any]] = []
        self.raw_turns: list[dict[str, Any]] = []

    def public_prompt(
        self,
        *,
        round_id: int,
        selected_ids: Sequence[str],
        prior_round_summaries: Mapping[int, Mapping[str, Any]],
        call_history: Sequence[ToolCallRecord],
    ) -> dict[str, Any]:
        """Build selector-visible state. Audit material is deliberately absent."""
        return {
            "protocol": "agentic-adaptive-selector-v1",
            "round_id": round_id,
            "catalogue_hash": self.catalogue.catalogue_hash,
            "eligible_task_ids": self.catalogue.task_ids,
            "selected_task_ids": tuple(selected_ids),
            "change": dataclasses.asdict(self.change),
            "bad_case_ids": tuple(sorted(self.bad_cases)),
            "prior_round_summaries": dict(prior_round_summaries),
            "call_history": [
                {
                    "call_id": call.call_id,
                    "tool": call.tool,
                    "arguments": call.arguments,
                    "result": call.result,
                    "response_hash": call.response_hash,
                }
                for call in call_history
            ],
            "remaining_task_budget": self.config.task_budget - len(selected_ids),
            "remaining_rounds": self.config.max_rounds - round_id,
        }

    def run_round(
        self,
        *,
        round_id: int,
        selected_ids: Sequence[str],
        prior_round_summaries: Mapping[int, Mapping[str, Any]],
        prior_selector_tokens: int = 0,
        prior_selector_latency_seconds: float = 0.0,
    ) -> SelectorRound:
        if not 0 <= round_id < self.config.max_rounds:
            raise SelectorError(f"round_id exceeds configured rounds: {round_id}")
        selected = tuple(selected_ids)
        if len(selected) != len(set(selected)) or set(selected) - set(self.catalogue.task_ids):
            raise SelectorError("Selected task state is invalid")
        remaining_capacity = self.config.task_budget - len(selected)
        if remaining_capacity <= 0:
            raise SelectorError("Selector called after task budget exhaustion")
        if prior_selector_tokens < 0 or prior_selector_latency_seconds < 0:
            raise SelectorError("Prior selector usage cannot be negative")
        if prior_selector_tokens >= self.config.selector_token_budget:
            raise SelectorError("Selector token budget was exhausted before this round")
        if prior_selector_latency_seconds >= self.config.selector_time_limit_seconds:
            raise SelectorError("Selector time budget was exhausted before this round")

        records: list[ToolCallRecord] = []
        prompts: list[dict[str, Any]] = []
        inspected: list[str] = []
        proposed: tuple[TaskProposal, ...] | None = None
        stop_reason = ""
        stop_after_round = False
        total_input = total_output = 0
        total_cost = total_latency = 0.0

        wall_started = time.monotonic()
        for call_index in range(self.config.max_tool_calls_per_round):
            prompt = self.public_prompt(
                round_id=round_id,
                selected_ids=selected,
                prior_round_summaries=prior_round_summaries,
                call_history=records,
            )
            prompts.append(prompt)
            remaining_seconds = (
                self.config.selector_time_limit_seconds
                - prior_selector_latency_seconds
                - (time.monotonic() - wall_started)
            )
            if remaining_seconds <= 0:
                raise SelectorError("Selector time budget exceeded before model call")
            turn = self.client.next_action(
                prompt, TOOL_SCHEMAS, timeout_seconds=remaining_seconds
            )
            self.raw_turns.append(
                {
                    "round_id": round_id,
                    "call_index": call_index,
                    "prompt": prompt,
                    "raw_response": turn.raw_response,
                    "model_revision": turn.model_revision,
                    "input_tokens": turn.input_tokens,
                    "output_tokens": turn.output_tokens,
                    "cost": turn.cost,
                    "reported_latency_seconds": turn.latency_seconds,
                }
            )
            measured_latency = time.monotonic() - wall_started
            total_input += turn.input_tokens
            total_output += turn.output_tokens
            total_cost += turn.cost
            total_latency += turn.latency_seconds
            if (
                prior_selector_tokens + total_input + total_output
                > self.config.selector_token_budget
            ):
                raise SelectorError("Selector token budget exceeded")
            if (
                prior_selector_latency_seconds + measured_latency
                > self.config.selector_time_limit_seconds
            ):
                raise SelectorError("Selector time budget exceeded")
            try:
                tool, arguments = _parse_action(turn, self.config.selector_model_revision)
            except SelectorError as error:
                self.validation_failures.append(
                    {
                        "round_id": round_id,
                        "call_index": call_index,
                        "prompt": prompt,
                        "raw_response": turn.raw_response,
                        "error": str(error),
                    }
                )
                raise
            call_id = f"round-{round_id}-call-{call_index}"
            result: Any
            candidate_ids: tuple[str, ...] = ()

            if proposed is not None and tool != "finish_round":
                raise SelectorError("Only finish_round may follow propose_tasks")
            if tool == "search_lexical":
                hits = self.lexical_index.search(
                    arguments["query"],
                    filters=arguments["filters"],
                    limit=arguments["limit"],
                )
                result = [_result_payload(hit) for hit in hits]
                candidate_ids = tuple(hit.instance_id for hit in hits)
            elif tool == "search_semantic":
                hits = self.semantic_index.search(
                    arguments["query"], limit=arguments["limit"]
                )
                result = [_result_payload(hit) for hit in hits]
                candidate_ids = tuple(hit.instance_id for hit in hits)
            elif tool == "get_task":
                instance_id = arguments["instance_id"]
                card = self.catalogue.by_id.get(instance_id)
                if card is None:
                    raise SelectorError(f"Unknown task ID: {instance_id}")
                result = dataclasses.asdict(card)
                candidate_ids = (instance_id,)
            elif tool == "get_bad_case":
                bad_case_id = arguments["bad_case_id"]
                if bad_case_id not in self.bad_cases:
                    raise SelectorError(f"Unknown bad case ID: {bad_case_id}")
                result = dataclasses.asdict(self.bad_cases[bad_case_id])
            elif tool == "get_change":
                result = dataclasses.asdict(self.change)
            elif tool == "marginal_coverage":
                candidate_values = tuple(arguments["candidate_ids"])
                selected_values = tuple(arguments["selected_ids"])
                universe_values = tuple(arguments["universe"])
                if selected_values != selected:
                    raise SelectorError("marginal_coverage selected_ids differ from controller state")
                if universe_values != self.catalogue.task_ids:
                    raise SelectorError("marginal_coverage universe must be the frozen catalogue")
                result = {
                    candidate: marginal_coverage(
                        candidate, selected, self.catalogue.task_ids, self.vectors
                    )
                    for candidate in candidate_values
                }
                candidate_ids = candidate_values
            elif tool == "inspect_round_results":
                inspected_round_id = arguments["round_id"]
                if inspected_round_id not in prior_round_summaries:
                    raise SelectorError(
                        f"Round result is unavailable or restricted: {inspected_round_id}"
                    )
                result = dict(prior_round_summaries[inspected_round_id])
            elif tool == "propose_tasks":
                proposed = self._parse_proposals(arguments["proposals"], records, selected)
                result = {"accepted_for_validation": len(proposed)}
            elif tool == "finish_round":
                if proposed is None:
                    raise SelectorError("finish_round requires a prior propose_tasks call")
                stop_reason = arguments["stop_reason"]
                stop_after_round = arguments["stop_after_round"]
                if not isinstance(stop_reason, str) or not stop_reason.strip():
                    raise SelectorError("finish_round requires a non-empty stop_reason")
                if not isinstance(stop_after_round, bool):
                    raise SelectorError("stop_after_round must be boolean")
                if stop_after_round and not stop_reason.startswith("evidence_saturation:"):
                    raise SelectorError(
                        "Selector stop requires an evidence_saturation: rationale"
                    )
                result = {"finished": True}
            else:
                raise AssertionError(f"Unhandled selector tool: {tool}")

            for candidate in candidate_ids:
                if candidate not in inspected:
                    inspected.append(candidate)
            response_hash = hashlib.sha256(turn.raw_response.encode()).hexdigest()
            records.append(
                ToolCallRecord(
                    call_id=call_id,
                    tool=tool,
                    arguments=arguments,
                    result=result,
                    prompt_hash=hashlib.sha256(
                        json.dumps(prompt, sort_keys=True, separators=(",", ":")).encode()
                    ).hexdigest(),
                    raw_response=turn.raw_response,
                    response_hash=response_hash,
                    input_tokens=turn.input_tokens,
                    output_tokens=turn.output_tokens,
                    cost=turn.cost,
                    latency_seconds=turn.latency_seconds,
                )
            )
            if tool == "finish_round":
                break
        else:
            raise SelectorError("Selector tool-call budget exhausted before finish_round")

        assert proposed is not None
        chosen = self._arbitrate(
            proposed=proposed,
            inspected_ids=tuple(inspected),
            selected_ids=selected,
            remaining_capacity=remaining_capacity,
            records=records,
        )
        return SelectorRound(
            round_id=round_id,
            selected_tasks=chosen,
            tool_calls=tuple(records),
            prompts=tuple(prompts),
            inspected_candidate_ids=tuple(inspected),
            stop_reason=stop_reason,
            stop_after_round=stop_after_round,
            input_tokens=total_input,
            output_tokens=total_output,
            cost=total_cost,
            latency_seconds=time.monotonic() - wall_started,
        )

    def _parse_proposals(
        self,
        raw: object,
        records: Sequence[ToolCallRecord],
        selected_ids: Sequence[str],
    ) -> tuple[TaskProposal, ...]:
        if not isinstance(raw, list) or not raw:
            raise SelectorError("propose_tasks requires a non-empty proposal list")
        references = {record.call_id for record in records}
        candidates_by_reference: dict[str, set[str]] = {}
        for record in records:
            candidates: set[str] = set()
            if record.tool == "get_task":
                candidates.add(record.arguments["instance_id"])
            elif isinstance(record.result, list):
                candidates.update(
                    item["instance_id"]
                    for item in record.result
                    if isinstance(item, dict) and isinstance(item.get("instance_id"), str)
                )
            elif record.tool == "marginal_coverage":
                candidates.update(record.arguments["candidate_ids"])
            candidates_by_reference[record.call_id] = candidates
        proposals: list[TaskProposal] = []
        for index, item in enumerate(raw):
            if not isinstance(item, dict):
                raise SelectorError(f"Proposal {index} must be an object")
            required = {
                "instance_id",
                "retrieval_role",
                "evidence_reference",
                "expected_signal",
                "rationale",
                "necessary_distinct_reason",
            }
            if set(item) != required:
                raise SelectorError(f"Proposal {index} fields must be exactly {sorted(required)}")
            try:
                proposal = TaskProposal(
                    instance_id=item["instance_id"],
                    retrieval_role=RetrievalRole(item["retrieval_role"]),
                    evidence_reference=item["evidence_reference"],
                    expected_signal=item["expected_signal"],
                    rationale=item["rationale"],
                    necessary_distinct_reason=item["necessary_distinct_reason"],
                )
            except (ValueError, ValidationError) as error:
                raise SelectorError(f"Invalid proposal {index}: {error}") from error
            if proposal.instance_id not in self.catalogue.by_id:
                raise SelectorError(f"Unknown proposed task ID: {proposal.instance_id}")
            if proposal.instance_id in selected_ids:
                raise SelectorError(f"Task was already selected: {proposal.instance_id}")
            if proposal.evidence_reference not in references:
                raise SelectorError(
                    f"Proposal evidence reference does not name a prior tool call: "
                    f"{proposal.evidence_reference}"
                )
            if proposal.instance_id not in candidates_by_reference[proposal.evidence_reference]:
                raise SelectorError(
                    f"Proposal evidence does not contain task {proposal.instance_id}: "
                    f"{proposal.evidence_reference}"
                )
            if proposal.instance_id not in candidates_by_reference[proposal.evidence_reference]:
                raise SelectorError(
                    f"Proposal evidence does not contain task {proposal.instance_id}: "
                    f"{proposal.evidence_reference}"
                )
            proposals.append(proposal)
        ids = [proposal.instance_id for proposal in proposals]
        if len(ids) != len(set(ids)):
            raise SelectorError("Selector proposal contains duplicate task IDs")
        return tuple(proposals)

    def _arbitrate(
        self,
        *,
        proposed: Sequence[TaskProposal],
        inspected_ids: Sequence[str],
        selected_ids: Sequence[str],
        remaining_capacity: int,
        records: Sequence[ToolCallRecord],
    ) -> tuple[SelectedTask, ...]:
        target = min(remaining_capacity, self.config.max_tasks_per_round)
        direct = [
            proposal
            for proposal in proposed
            if proposal.retrieval_role
            in {RetrievalRole.REPAIR_CAUSE, RetrievalRole.REGRESSION}
        ]
        proposal_by_id = {proposal.instance_id: proposal for proposal in proposed}
        if len(direct) <= target:
            direct_ranked_list: list[tuple[str, float]] = []
            direct_selected = list(selected_ids)
            for proposal in direct:
                gain = marginal_coverage(
                    proposal.instance_id,
                    direct_selected,
                    self.catalogue.task_ids,
                    self.vectors,
                )
                direct_ranked_list.append((proposal.instance_id, gain))
                direct_selected.append(proposal.instance_id)
            direct_ranked = tuple(direct_ranked_list)
        else:
            direct_ranked = greedy_by_marginal_coverage(
                [proposal.instance_id for proposal in direct],
                selected_ids,
                self.catalogue.task_ids,
                self.vectors,
                target,
            )
        chosen: list[SelectedTask] = []
        running_selected = list(selected_ids)
        for instance_id, gain in direct_ranked:
            proposal = proposal_by_id[instance_id]
            if math.isclose(gain, 0.0, abs_tol=1e-15) and not proposal.necessary_distinct_reason.strip():
                raise SelectorError(
                    f"Zero-gain direct hypothesis lacks a distinct-probe reason: {instance_id}"
                )
            chosen.append(
                SelectedTask(
                    proposal=proposal,
                    marginal_coverage=gain,
                    selection_source="direct_hypothesis",
                )
            )
            running_selected.append(instance_id)

        capacity = target - len(chosen)
        if capacity:
            candidate_pool = [
                instance_id
                for instance_id in inspected_ids
                if instance_id not in running_selected
            ]
            if not candidate_pool:
                candidate_pool = [
                    instance_id
                    for instance_id in self.catalogue.task_ids
                    if instance_id not in running_selected
                ]
            ranked = greedy_by_marginal_coverage(
                candidate_pool,
                running_selected,
                self.catalogue.task_ids,
                self.vectors,
                capacity,
            )
            evidence_by_candidate = {
                candidate: record.call_id
                for record in records
                for candidate in (
                    [record.arguments["instance_id"]]
                    if record.tool == "get_task"
                    else [
                        item["instance_id"]
                        for item in record.result
                        if isinstance(item, dict) and isinstance(item.get("instance_id"), str)
                    ]
                    if isinstance(record.result, list)
                    else record.arguments.get("candidate_ids", [])
                    if record.tool == "marginal_coverage"
                    else []
                )
            }
            for instance_id, gain in ranked:
                proposal = proposal_by_id.get(instance_id)
                if proposal is None:
                    proposal = TaskProposal(
                        instance_id=instance_id,
                        retrieval_role=RetrievalRole.REPRESENTATIVE_COVERAGE,
                        evidence_reference=evidence_by_candidate.get(
                            instance_id, "deterministic:frozen-catalogue"
                        ),
                        expected_signal="Increase facility-location coverage of the frozen universe.",
                        rationale="Highest marginal semantic coverage among inspected candidates.",
                    )
                if math.isclose(gain, 0.0, abs_tol=1e-15):
                    raise SelectorError(f"Zero-gain coverage completion is invalid: {instance_id}")
                chosen.append(
                    SelectedTask(
                        proposal=proposal,
                        marginal_coverage=gain,
                        selection_source="coverage_completion",
                    )
                )
                running_selected.append(instance_id)
        return tuple(chosen)
