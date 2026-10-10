# Changelog

## [2026-10-09] Implement fail-closed adaptive evaluation controller
- **Change**: Added frozen catalogue/retrieval, strict embeddings, selector/audit, paired decision, artifacts, and container contract in `rollback_mvp/adaptive_eval/`.
- **Reason**: Mutation-specific evidence must preserve one auditable parent/child/counterfactual final manifest.
- **Debug**: Fixed BM25 and identity/evidence/output safety gaps; Docker remains blocked by denied Colima access and missing isolation attestation.

## [2026-10-09] Agentic adaptive evaluation design
- **Change**: Added the DGM-200 dynamic sampling, paired execution, independent
  audit, and full-candidate-isolation design in
  AGENTIC_ADAPTIVE_EVALUATION_DESIGN.md.
- **Reason**: Fixed hand-selected evaluation subsets can miss both mutation
  regressions and relevant repair cases, so online evolution needs an
  evidence-driven and reproducible selection protocol.
