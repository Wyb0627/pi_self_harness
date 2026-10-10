"""Frozen DGM-200 catalogue validation and deterministic task cards."""

from __future__ import annotations

import dataclasses
import re
from collections import Counter
from pathlib import Path
from typing import Mapping, Sequence

from .schemas import (
    EXPECTED_DATASET_MANIFEST_SHA256,
    EXPECTED_ORDERED_IDS_SHA256,
    EXPECTED_REPOSITORY_COUNTS,
    EXPECTED_TASK_COUNT,
    CatalogueManifest,
    TaskCard,
    ValidationError,
    canonical_json_bytes,
    hash_json,
    load_strict_json,
    ordered_ids_hash,
    sha256_bytes,
)


TOKEN_PATTERN = re.compile(
    r"[A-Za-z_][A-Za-z0-9_.:/-]*|[A-Z][A-Za-z]+(?:Error|Exception|Warning)"
)
SAFE_RECORD_FIELDS = ("instance_id", "repo", "base_commit", "problem_statement")


def task_text(instance_id: str, repo: str, base_commit: str, problem_statement: str) -> str:
    return (
        f"Instance: {instance_id}\nRepository: {repo}\nBase commit: {base_commit}\n"
        f"Issue:\n{problem_statement}"
    )


def lexical_terms(text: str) -> tuple[str, ...]:
    """Return unique lower-case exact tokens in first-occurrence order."""
    seen: set[str] = set()
    terms: list[str] = []
    for match in TOKEN_PATTERN.finditer(text):
        term = match.group(0).lower()
        if term not in seen:
            seen.add(term)
            terms.append(term)
    return tuple(terms)


def structured_tags(repo: str, instance_id: str) -> tuple[str, ...]:
    owner, separator, project = repo.partition("/")
    if not separator or not owner or not project:
        raise ValidationError(f"Invalid repository in {instance_id}: {repo}")
    return (f"repo:{repo}", f"owner:{owner}", f"project:{project}")


def _validate_manifest_shape(manifest: object) -> list[dict[str, object]]:
    if not isinstance(manifest, dict):
        raise ValidationError("Dataset manifest must be a JSON object")
    if manifest.get("schema_version") != 1:
        raise ValidationError("Dataset manifest schema_version must be 1")
    if manifest.get("name") != "dgm-swebench-verified-200":
        raise ValidationError("Unexpected dataset manifest name")
    ordering = manifest.get("ordering")
    if not isinstance(ordering, dict):
        raise ValidationError("Dataset manifest ordering is missing")
    if ordering.get("count") != EXPECTED_TASK_COUNT:
        raise ValidationError("Dataset manifest must contain exactly 200 tasks")
    if ordering.get("instance_ids_sha256") != EXPECTED_ORDERED_IDS_SHA256:
        raise ValidationError("Dataset manifest declares the wrong ordered-ID hash")
    records = manifest.get("records")
    if not isinstance(records, list) or len(records) != EXPECTED_TASK_COUNT:
        raise ValidationError("Dataset manifest records must contain exactly 200 rows")
    if not all(isinstance(entry, dict) for entry in records):
        raise ValidationError("Dataset manifest records contain a non-object row")
    return records


def load_frozen_catalogue(
    manifest_path: Path,
    *,
    embedding_metadata: Mapping[str, tuple[str, str]] | None = None,
) -> CatalogueManifest:
    """Validate the literal frozen file before exposing public task fields."""
    try:
        manifest_bytes = manifest_path.read_bytes()
    except OSError as error:
        raise ValidationError(f"Cannot read dataset manifest {manifest_path}: {error}") from error
    manifest_hash = sha256_bytes(manifest_bytes)
    if manifest_hash != EXPECTED_DATASET_MANIFEST_SHA256:
        raise ValidationError(
            "Dataset manifest hash mismatch: "
            f"expected {EXPECTED_DATASET_MANIFEST_SHA256}, found {manifest_hash}"
        )
    manifest = load_strict_json(manifest_path)
    records = _validate_manifest_shape(manifest)

    ids: list[str] = []
    rows: list[tuple[dict[str, object], dict[str, object]]] = []
    for ordinal, entry in enumerate(records):
        if entry.get("ordinal") != ordinal:
            raise ValidationError(f"Non-contiguous manifest ordinal at row {ordinal}")
        row = entry.get("record")
        if not isinstance(row, dict):
            raise ValidationError(f"Manifest row {ordinal} has no record object")
        if any(not isinstance(row.get(field), str) or not row[field] for field in SAFE_RECORD_FIELDS):
            raise ValidationError(f"Manifest row {ordinal} lacks a required public field")
        source_hash = entry.get("source_row_sha256")
        if source_hash != sha256_bytes(canonical_json_bytes(row)):
            raise ValidationError(f"Manifest row {ordinal} source hash mismatch")
        instance_id = str(row["instance_id"])
        ids.append(instance_id)
        rows.append((entry, row))

    if len(ids) != len(set(ids)):
        raise ValidationError("Dataset manifest contains duplicate task IDs")
    actual_order_hash = ordered_ids_hash(ids)
    if actual_order_hash != EXPECTED_ORDERED_IDS_SHA256:
        raise ValidationError(
            f"Ordered-ID hash mismatch: expected {EXPECTED_ORDERED_IDS_SHA256}, "
            f"found {actual_order_hash}"
        )
    if ids != sorted(ids):
        raise ValidationError("Frozen manifest task IDs are not in Verified source order")
    counts = Counter(str(row["repo"]).split("/")[-1] for _, row in rows)
    if dict(sorted(counts.items())) != EXPECTED_REPOSITORY_COUNTS:
        raise ValidationError(f"Repository distribution mismatch: {dict(counts)}")

    if embedding_metadata is not None:
        missing = set(ids) - set(embedding_metadata)
        extra = set(embedding_metadata) - set(ids)
        if missing or extra:
            raise ValidationError(
                f"Embedding metadata task mismatch: missing={sorted(missing)}, extra={sorted(extra)}"
            )

    cards: list[TaskCard] = []
    for entry, row in rows:
        instance_id = str(row["instance_id"])
        repo = str(row["repo"])
        base_commit = str(row["base_commit"])
        statement = str(row["problem_statement"])
        text = task_text(instance_id, repo, base_commit, statement)
        embedding_id, vector_hash = ("", "")
        if embedding_metadata is not None:
            embedding_id, vector_hash = embedding_metadata[instance_id]
        cards.append(
            TaskCard(
                instance_id=instance_id,
                repo=repo,
                base_commit=base_commit,
                problem_statement=statement,
                lexical_terms=lexical_terms(text),
                structured_tags=structured_tags(repo, instance_id),
                task_text_hash=sha256_bytes(text.encode()),
                embedding_id=embedding_id,
                embedding_vector_hash=vector_hash,
                catalogue_revision=manifest_hash,
            )
        )
    catalogue_payload = {
        "schema_version": 1,
        "dataset_manifest_hash": manifest_hash,
        "ordered_ids_hash": actual_order_hash,
        "cards": [dataclasses.asdict(card) for card in cards],
    }
    return CatalogueManifest(
        source_path=str(manifest_path.resolve()),
        dataset_manifest_hash=manifest_hash,
        ordered_ids_hash=actual_order_hash,
        catalogue_hash=hash_json(catalogue_payload),
        task_ids=tuple(ids),
        cards=tuple(cards),
    )


def require_task_ids(catalogue: CatalogueManifest, task_ids: Sequence[str]) -> tuple[str, ...]:
    values = tuple(task_ids)
    if len(values) != len(set(values)):
        raise ValidationError("Task ID list contains duplicates")
    unknown = sorted(set(values) - set(catalogue.task_ids))
    if unknown:
        raise ValidationError(f"Unknown task IDs: {unknown}")
    return values
