"""Strict public-trajectory loading with raw evidence hashes."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .schemas import ValidationError, sha256_bytes


FORBIDDEN_EVIDENCE_KEYS = {
    "patch",
    "test_patch",
    "gold_patch",
    "private_tests",
    "fail_to_pass",
    "pass_to_pass",
    "official_grader",
}
FORBIDDEN_TEXT_MARKERS = {
    "test_patch",
    "gold_patch",
    "private_tests",
    "official_grader",
    "hidden assertion",
    "grader log",
    "fail_to_pass",
    "pass_to_pass",
}


def require_public_text(value: str, field_name: str) -> None:
    normalized = value.lower()
    found = sorted(marker for marker in FORBIDDEN_TEXT_MARKERS if marker in normalized)
    if found:
        raise ValidationError(
            f"{field_name} contains restricted evaluator markers: {found}"
        )


def _reject_private_keys(value: Any, path: str) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = key.lower() if isinstance(key, str) else str(key).lower()
            if normalized in FORBIDDEN_EVIDENCE_KEYS:
                raise ValidationError(
                    f"Trajectory contains restricted evaluator field at {path}.{key}"
                )
            _reject_private_keys(nested, f"{path}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _reject_private_keys(nested, f"{path}[{index}]")


@dataclass(frozen=True, slots=True)
class TrajectoryEvidence:
    source_path: str
    source_trace_hash: str
    events: tuple[dict[str, Any], ...]


def load_public_trajectory(path: Path) -> TrajectoryEvidence:
    try:
        content = path.read_bytes()
    except OSError as error:
        raise ValidationError(f"Cannot read trajectory {path}: {error}") from error
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValidationError(
                f"Malformed trajectory JSON at {path}:{line_number}: {error}"
            ) from error
        if not isinstance(event, dict):
            raise ValidationError(
                f"Trajectory event at {path}:{line_number} must be an object"
            )
        _reject_private_keys(event, f"event[{line_number}]")
        events.append(event)
    if not events:
        raise ValidationError(f"Trajectory contains no events: {path}")
    return TrajectoryEvidence(
        source_path=str(path.resolve()),
        source_trace_hash=sha256_bytes(content),
        events=tuple(events),
    )
