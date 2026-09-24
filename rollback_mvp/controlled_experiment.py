"""Controlled delayed-failure scenarios for rollback-point selection.

Unlike the DGM subtree replay, these cases have a known injected toxic edge.
The LLM sees only the evolution history and current failure evidence. The
oracle is loaded separately and is never rendered into the prompt.
"""

from __future__ import annotations

import json
import os
import random
import hashlib
from dataclasses import dataclass

from config import REPO_ROOT
from llm_client import LLMClient

CONTROLLED_CASES_PATH = os.path.join(
    REPO_ROOT,
    "rollback_mvp",
    "controlled_cases.json",
)

SYSTEM_PROMPT = """You diagnose delayed failures in a self-evolving coding-agent harness.

You receive a linear version history and a failure observed in the current
version. An earlier change may have introduced a latent defect even if that
version passed its original evaluation. Later changes may merely expose or
amplify the defect.

Select the exact rollback target:
- Identify the earliest edge that is necessary for the observed failure.
- Roll back to the version immediately before that edge.
- Do not automatically choose the previous version or highest-scoring version.
- Do not roll back farther than the evidence requires.
- Distinguish the root cause from later changes that only expose it.

Use only the supplied history and failure evidence. Return concise, auditable
diagnostic evidence, not hidden reasoning.

Reply with strict JSON:
{
  "culprit_edge": "<from_version->to_version>",
  "rollback_to": "<version_id>",
  "evidence": ["<specific observation>", "<specific history link>"],
  "confidence": <number from 0 to 1>
}"""


@dataclass(frozen=True)
class Version:
    id: str
    score: float
    change: str
    patch: str


@dataclass(frozen=True)
class Failure:
    error: str
    observations: tuple[str, ...]
    debug: tuple[str, ...]


@dataclass(frozen=True)
class Oracle:
    culprit_edge: str
    rollback_to: str
    explanation: str


@dataclass(frozen=True)
class ControlledCase:
    id: str
    title: str
    task_family: str
    versions: tuple[Version, ...]
    failure: Failure
    oracle: Oracle

    @property
    def current(self) -> Version:
        return self.versions[-1]

    @property
    def rollback_candidates(self) -> tuple[Version, ...]:
        return self.versions[:-1]


@dataclass(frozen=True)
class ControlledDecision:
    case_id: str
    decider: str
    repeat: int
    choice: str
    culprit_edge: str
    reason: str
    exact: int
    clears_toxicity: int
    distance: int
    over_rollback: int
    under_rollback: int
    attribution_hit: int


def load_controlled_cases(path: str = CONTROLLED_CASES_PATH) -> list[ControlledCase]:
    with open(path) as f:
        raw = json.load(f)
    if raw.get("schema_version") != 1:
        raise ValueError("Unsupported controlled-case schema version.")

    cases: list[ControlledCase] = []
    seen: set[str] = set()
    for item in raw["cases"]:
        versions = tuple(Version(**version) for version in item["versions"])
        case = ControlledCase(
            id=item["id"],
            title=item["title"],
            task_family=item["task_family"],
            versions=versions,
            failure=Failure(
                error=item["failure"]["error"],
                observations=tuple(item["failure"]["observations"]),
                debug=tuple(item["failure"]["debug"]),
            ),
            oracle=Oracle(**item["oracle"]),
        )
        _validate_case(case, seen)
        seen.add(case.id)
        cases.append(case)
    return cases


def _validate_case(case: ControlledCase, seen: set[str]) -> None:
    if case.id in seen:
        raise ValueError(f"Duplicate controlled case id: {case.id}")
    if len(case.versions) < 3:
        raise ValueError(f"{case.id}: expected at least three versions.")
    ids = [version.id for version in case.versions]
    if len(ids) != len(set(ids)):
        raise ValueError(f"{case.id}: duplicate version ids.")
    if case.oracle.rollback_to not in ids[:-1]:
        raise ValueError(f"{case.id}: oracle rollback target is not an ancestor.")
    oracle_index = ids.index(case.oracle.rollback_to)
    expected_edge = f"{ids[oracle_index]}->{ids[oracle_index + 1]}"
    if case.oracle.culprit_edge != expected_edge:
        raise ValueError(
            f"{case.id}: culprit edge {case.oracle.culprit_edge} "
            f"does not follow rollback target {case.oracle.rollback_to}."
        )


def build_controlled_prompt(case: ControlledCase, include_debug: bool) -> str:
    display_ids = _display_ids(case)
    lines = [
        f"Task family: {case.task_family}",
        f"Current version: {display_ids[case.current.id]}",
        "",
        "Evolution history:",
    ]
    for index, version in enumerate(case.versions):
        prefix = (
            "baseline"
            if index == 0
            else (
                f"edge {display_ids[case.versions[index - 1].id]}"
                f"->{display_ids[version.id]}"
            )
        )
        lines += [
            f"--- {display_ids[version.id]} ({prefix}) ---",
            f"Acceptance score at that time: {version.score:.3f}",
            f"Change: {_mask_version_ids(version.change, display_ids)}",
            f"Patch excerpt:\n{_mask_version_ids(version.patch, display_ids)}",
        ]

    lines += [
        "",
        "Current failure:",
        _mask_version_ids(case.failure.error, display_ids),
        "",
        "Reproduction observations:",
    ]
    lines.extend(
        f"- {_mask_version_ids(observation, display_ids)}"
        for observation in case.failure.observations
    )
    if include_debug:
        lines += ["", "Debug evidence:"]
        lines.extend(
            f"- {_mask_version_ids(item, display_ids)}"
            for item in case.failure.debug
        )

    candidates = ", ".join(
        display_ids[version.id] for version in case.rollback_candidates
    )
    lines += [
        "",
        f"Valid rollback targets: {candidates}",
        "Choose exactly one target and one edge from this history.",
    ]
    return "\n".join(lines)


def llm_controlled_decider(
    case: ControlledCase,
    client: LLMClient,
    *,
    include_debug: bool,
) -> tuple[str, str, str]:
    display_ids = _display_ids(case)
    reverse_ids = {display: raw for raw, display in display_ids.items()}
    result = client.complete_json(
        SYSTEM_PROMPT,
        build_controlled_prompt(case, include_debug),
    )
    display_choice = _normalize_choice(
        str(result.get("rollback_to", "")).strip(),
        [display_ids[version.id] for version in case.rollback_candidates],
    )
    choice = reverse_ids.get(display_choice, "")
    display_edge = str(result.get("culprit_edge", "")).strip()
    edge = _unmask_edge(display_edge, reverse_ids)
    evidence = result.get("evidence", [])
    reason = json.dumps(
        {
            "evidence": evidence if isinstance(evidence, list) else [str(evidence)],
            "confidence": result.get("confidence"),
        },
        ensure_ascii=False,
    )
    if not choice:
        choice = highest_score_decider(case)
        reason = f"[fallback] {reason}"
    return choice, edge, reason


def previous_version_decider(case: ControlledCase) -> str:
    return case.versions[-2].id


def highest_score_decider(case: ControlledCase) -> str:
    return max(case.rollback_candidates, key=lambda version: version.score).id


def random_controlled_decider(case: ControlledCase, rng: random.Random) -> str:
    return rng.choice(case.rollback_candidates).id


def judge_controlled(
    case: ControlledCase,
    *,
    decider: str,
    repeat: int,
    choice: str,
    culprit_edge: str,
    reason: str,
) -> ControlledDecision:
    ids = [version.id for version in case.versions]
    oracle_index = ids.index(case.oracle.rollback_to)
    choice_index = ids.index(choice)
    return ControlledDecision(
        case_id=case.id,
        decider=decider,
        repeat=repeat,
        choice=choice,
        culprit_edge=culprit_edge,
        reason=reason,
        exact=int(choice == case.oracle.rollback_to),
        clears_toxicity=int(choice_index <= oracle_index),
        distance=abs(choice_index - oracle_index),
        over_rollback=max(oracle_index - choice_index, 0),
        under_rollback=max(choice_index - oracle_index, 0),
        attribution_hit=int(culprit_edge == case.oracle.culprit_edge),
    )


def _normalize_choice(raw: str, valid_ids: list[str]) -> str:
    if raw in valid_ids:
        return raw
    matches = [
        version_id
        for version_id in valid_ids
        if version_id.startswith(raw) or raw.startswith(version_id)
    ]
    return matches[0] if len(matches) == 1 else ""


def _display_ids(case: ControlledCase) -> dict[str, str]:
    return {
        version.id: "r_" + hashlib.sha256(
            f"{case.id}|{version.id}".encode()
        ).hexdigest()[:8]
        for version in case.versions
    }


def _mask_version_ids(text: str, display_ids: dict[str, str]) -> str:
    masked = text
    for raw, display in sorted(display_ids.items(), key=lambda item: -len(item[0])):
        masked = masked.replace(raw, display)
    return masked


def _unmask_edge(edge: str, reverse_ids: dict[str, str]) -> str:
    if "->" not in edge:
        return edge
    left, right = (part.strip() for part in edge.split("->", 1))
    raw_left = reverse_ids.get(left)
    raw_right = reverse_ids.get(right)
    if raw_left is None or raw_right is None:
        return edge
    return f"{raw_left}->{raw_right}"
