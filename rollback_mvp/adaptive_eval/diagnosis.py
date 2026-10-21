"""Bad-case construction from explicit, traceable diagnosis fields."""

from __future__ import annotations

from pathlib import Path

from .schemas import (
    BadCaseCard,
    CandidateChangeCard,
    CatalogueManifest,
    ValidationError,
    require_sha256,
    source_diff_hash,
    source_tree_hash,
)
from .trajectory import TrajectoryEvidence
from .trajectory import FORBIDDEN_EVIDENCE_KEYS


def _require_public_summary(value: str, field_name: str) -> None:
    normalized = value.lower()
    markers = FORBIDDEN_EVIDENCE_KEYS | {"hidden assertion", "grader log"}
    found = sorted(marker for marker in markers if marker in normalized)
    if found:
        raise ValidationError(
            f"{field_name} contains restricted evaluator markers: {found}"
        )


def build_bad_case_card(
    *,
    bad_case_id: str,
    parent_artifact_hash: str,
    instance_id: str,
    outcome: str,
    failure_taxonomy: str,
    trajectory_summary: str,
    tool_error_fingerprints: tuple[str, ...],
    changed_paths: tuple[str, ...],
    public_test_summary: str,
    created_at: str,
    trajectory: TrajectoryEvidence,
    catalogue: CatalogueManifest,
) -> BadCaseCard:
    """Build a card only from caller-supplied diagnosis; never invent missing text."""
    require_sha256(parent_artifact_hash, "parent_artifact_hash")
    if not trajectory_summary.strip():
        raise ValidationError("A bad case requires an explicit trajectory summary")
    _require_public_summary(trajectory_summary, "trajectory_summary")
    _require_public_summary(public_test_summary, "public_test_summary")
    if instance_id not in catalogue.by_id:
        raise ValidationError(f"Bad case has an unknown task ID: {instance_id}")
    return BadCaseCard(
        bad_case_id=bad_case_id,
        parent_artifact_hash=parent_artifact_hash,
        instance_id=instance_id,
        outcome=outcome,
        failure_taxonomy=failure_taxonomy,
        trajectory_summary=trajectory_summary,
        tool_error_fingerprints=tool_error_fingerprints,
        changed_paths=changed_paths,
        public_test_summary=public_test_summary,
        source_trace_hash=trajectory.source_trace_hash,
        created_at=created_at,
    )


def validate_candidate_change_snapshots(
    card: CandidateChangeCard, parent_snapshot: Path, child_snapshot: Path
) -> None:
    parent_hash = source_tree_hash(parent_snapshot)
    child_hash = source_tree_hash(child_snapshot)
    diff_hash = source_diff_hash(parent_snapshot, child_snapshot)
    if parent_hash != card.parent_artifact_hash:
        raise ValidationError("Parent snapshot hash differs from candidate change card")
    if child_hash != card.child_artifact_hash:
        raise ValidationError("Child snapshot hash differs from candidate change card")
    if diff_hash != card.diff_hash:
        raise ValidationError("Recomputed snapshot diff hash differs from change card")
