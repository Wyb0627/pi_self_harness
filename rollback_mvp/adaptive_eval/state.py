"""Hash-chained append-only events and immutable selection manifests."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from .schemas import ValidationError, canonical_json_bytes, hash_json, sha256_bytes


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as file:
            temporary = Path(file.name)
            file.write(content)
            file.flush()
            os.fsync(file.fileno())
        temporary.replace(path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def atomic_json(path: Path, value: Any) -> None:
    atomic_write(
        path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True).encode() + b"\n"
    )


@dataclass(frozen=True, slots=True)
class StateEvent:
    sequence: int
    event_type: str
    payload: dict[str, Any]
    previous_hash: str
    event_hash: str


class AppendOnlyState:
    """One immutable file per event, linked by content hashes."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.events_dir = root / "events"
        self.events_dir.mkdir(parents=True, exist_ok=True)
        self._events = self._load_events()

    @property
    def events(self) -> tuple[StateEvent, ...]:
        return tuple(self._events)

    def _load_events(self) -> list[StateEvent]:
        paths = sorted(self.events_dir.glob("*.json"))
        events: list[StateEvent] = []
        previous_hash = "0" * 64
        for expected_sequence, path in enumerate(paths):
            if path.name != f"{expected_sequence:06d}.json":
                raise ValidationError(f"Non-contiguous state event path: {path}")
            try:
                raw = json.loads(path.read_text())
            except (OSError, json.JSONDecodeError) as error:
                raise ValidationError(f"Cannot load state event {path}: {error}") from error
            if not isinstance(raw, dict):
                raise ValidationError(f"State event is not an object: {path}")
            event_hash = raw.get("event_hash")
            unhashed = {key: value for key, value in raw.items() if key != "event_hash"}
            if event_hash != hash_json(unhashed):
                raise ValidationError(f"State event hash mismatch: {path}")
            if raw.get("sequence") != expected_sequence:
                raise ValidationError(f"State event sequence mismatch: {path}")
            if raw.get("previous_hash") != previous_hash:
                raise ValidationError(f"State event chain mismatch: {path}")
            if not isinstance(raw.get("payload"), dict):
                raise ValidationError(f"State event payload is invalid: {path}")
            event = StateEvent(
                sequence=expected_sequence,
                event_type=str(raw.get("event_type")),
                payload=raw["payload"],
                previous_hash=previous_hash,
                event_hash=event_hash,
            )
            events.append(event)
            previous_hash = event_hash
        return events

    def append(self, event_type: str, payload: dict[str, Any]) -> StateEvent:
        if not event_type or not isinstance(payload, dict):
            raise ValidationError("State event requires a type and object payload")
        sequence = len(self._events)
        previous_hash = self._events[-1].event_hash if self._events else "0" * 64
        unhashed = {
            "sequence": sequence,
            "event_type": event_type,
            "payload": payload,
            "previous_hash": previous_hash,
        }
        event_hash = hash_json(unhashed)
        record = {**unhashed, "event_hash": event_hash}
        path = self.events_dir / f"{sequence:06d}.json"
        try:
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError as error:
            raise ValidationError(f"State event already exists: {path}") from error
        try:
            content = json.dumps(
                record, ensure_ascii=False, indent=2, sort_keys=True
            ).encode() + b"\n"
            with os.fdopen(descriptor, "wb") as file:
                file.write(content)
                file.flush()
                os.fsync(file.fileno())
            directory_fd = os.open(self.events_dir, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except BaseException:
            path.unlink(missing_ok=True)
            raise
        event = StateEvent(
            sequence=sequence,
            event_type=event_type,
            payload=payload,
            previous_hash=previous_hash,
            event_hash=event_hash,
        )
        self._events.append(event)
        return event

    def require_event_order(self, allowed_transitions: dict[str | None, set[str]]) -> None:
        previous: str | None = None
        for event in self._events:
            if event.event_type not in allowed_transitions.get(previous, set()):
                raise ValidationError(
                    f"Invalid state transition {previous!r} -> {event.event_type!r}"
                )
            previous = event.event_type


def freeze_file_once(path: Path, value: dict[str, Any]) -> str:
    content = json.dumps(
        value, ensure_ascii=False, indent=2, sort_keys=True
    ).encode() + b"\n"
    digest = sha256_bytes(canonical_json_bytes(value))
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as file:
            temporary = Path(file.name)
            file.write(content)
            file.flush()
            os.fsync(file.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            try:
                existing = json.loads(path.read_text())
            except (OSError, json.JSONDecodeError) as error:
                raise ValidationError(f"Cannot validate frozen file {path}: {error}") from error
            if existing != value:
                raise ValidationError(
                    f"Frozen file already exists with different content: {path}"
                )
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return digest


def hash_event_chain(events: Sequence[StateEvent]) -> str:
    return hash_json([event.event_hash for event in events])
