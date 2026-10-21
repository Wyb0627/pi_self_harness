# Experiment Log

## 2026-10-14

1. Inspected the production arbitration path. Coverage affects direct proposals only when they exceed capacity, and fills capacity when direct proposals underfill it.
2. Searched for real selector transcripts, a pinned embedding cache, a production selector adapter, and a trusted paired round evaluator. No runnable end-to-end adaptive experiment was available.
3. Added a hash-bound `coverage_selection_mode` with `greedy` and `agent_only` arms. Agent-only preserves direct proposal order, truncates at capacity, and never fills.
4. Replayed three fixed scripted selector traces over the frozen DGM-200 catalogue with synthetic orthogonal embeddings.
5. Observed identical exact-capacity IDs, different over-capacity arbitration, and a 2-to-1 task reduction in the under-capacity case. The isolation kill criterion did not trigger.
6. Repeated the replay and obtained a byte-identical `results.json` (SHA-256 17d2f6847872d9e9eb680160336ece0a9be50447d0900641ae7f46e490e51a3d).
7. Ran all 35 adaptive-eval unit tests successfully. Root `npm run check` passed formatting, then stopped on pre-existing unpinned dependencies inside generated DGM task workspaces. The remaining repository checks passed except `tsgo --noEmit`, which reported pre-existing model-catalog `unknown`/`never` errors across the AI package. No unrelated workspace files were modified.

## Decision

Keep both modes. The mechanism result supports running a paid endpoint ablation once the real selector, embedding sidecar, evaluator, and candidate runtime are available. It does not justify deleting greedy coverage yet.
