"""Controller-owned audit derivation, isolated from the selector."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .schemas import ValidationError, canonical_json_bytes, require_sha256, sha256_bytes


@dataclass(frozen=True, slots=True)
class AuditSample:
    seed_derivation: str
    candidate_ids: tuple[str, ...]
    audit_ids: tuple[str, ...]


def derive_audit_seed(
    experiment_seed: str,
    parent_artifact_hash: str,
    child_artifact_hash: str,
    catalogue_hash: str,
) -> str:
    if not experiment_seed:
        raise ValidationError("experiment_seed must be non-empty")
    for name, value in (
        ("parent_artifact_hash", parent_artifact_hash),
        ("child_artifact_hash", child_artifact_hash),
        ("catalogue_hash", catalogue_hash),
    ):
        require_sha256(value, name)
    return sha256_bytes(
        canonical_json_bytes(
            {
                "protocol": "adaptive-eval-audit-v1",
                "experiment_seed": experiment_seed,
                "parent_artifact_hash": parent_artifact_hash,
                "child_artifact_hash": child_artifact_hash,
                "catalogue_hash": catalogue_hash,
            }
        )
    )


def deterministic_audit(
    eligible_ids: Sequence[str],
    selected_ids: Sequence[str],
    *,
    size: int,
    seed_derivation: str,
) -> AuditSample:
    require_sha256(seed_derivation, "seed_derivation")
    if size < 0:
        raise ValidationError("Audit size cannot be negative")
    eligible = tuple(eligible_ids)
    selected = tuple(selected_ids)
    if len(eligible) != len(set(eligible)) or len(selected) != len(set(selected)):
        raise ValidationError("Eligible and selected audit IDs must be unique")
    unknown_selected = set(selected) - set(eligible)
    if unknown_selected:
        raise ValidationError(f"Selected IDs are not eligible: {sorted(unknown_selected)}")
    candidates = tuple(instance_id for instance_id in eligible if instance_id not in set(selected))
    if size > len(candidates):
        raise ValidationError("Audit size exceeds remaining candidate count")
    ranked = sorted(
        candidates,
        key=lambda instance_id: (
            sha256_bytes(f"{seed_derivation}\0{instance_id}".encode()),
            instance_id,
        ),
    )
    return AuditSample(
        seed_derivation=seed_derivation,
        candidate_ids=candidates,
        audit_ids=tuple(ranked[:size]),
    )
