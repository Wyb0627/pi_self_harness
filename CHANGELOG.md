# Changelog

## [2026-10-10] Pre-register cold-start dynamic-sampling evaluation
- **Change**: Added DYNAMIC_SAMPLING_60_140_EXPERIMENT_PROTOCOL.md with clean-P0 isolation, DGM 10+50/140 roles, A0-A2 MVP controls, Phase-2-gated A3 rollback, P0 reference endpoints, fixed-policy/statistical/failure locks, and an all-in cost ledger.
- **Reason**: The dynamic paired sampler must be compared against a fixed DGM-compatible policy without contaminating the held-out endpoint or hiding parent-evaluation cost.
- **Debug**: No experiment was run; role-filtered catalogue isolation, production adapters, an attested runtime, and prior runs reaching normal terminal state with exited processes remain required.

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
