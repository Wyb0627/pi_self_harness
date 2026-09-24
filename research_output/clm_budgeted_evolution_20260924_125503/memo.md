# Research Memo: Budgeted Causal Lineage Evolution

## 1. Comparable End-to-End Evaluation

### DGM paper and release [P1]

- The paper reports SWE-bench improvement from 20.0% to 50.0% through
  self-modification and archive-based open-ended search.
- The intended evaluation funnel is 10 tasks, then 60, then 200 for leading
  candidates.
- The public runner loads the 140-task panel and computes a full-evaluation
  threshold but never executes that third stage. Released results nevertheless
  include 197-200-task nodes, so the public code and executed experiment differ.
- Source: [DGM paper](https://arxiv.org/html/2505.22954v2/), local source
  `/tmp/dgm-clm-eval`.

### Identifiability [P1]

- Logged DGM trajectories contain outcomes only for generated children.
- A different parent or mutation policy would create absent counterfactual
  children; no unbiased final-score estimate is possible from the release.
- This is the standard deficient-support problem in off-policy evaluation.
- Sources: [OPE tutorial](https://dl.acm.org/doi/fullHtml/10.1145/3460231.3473320),
  [DGM paper](https://arxiv.org/html/2505.22954v2/).

### Fair comparison contract

- Run original Pi, DGM-style Pi evolution, and CLM evolution on one Pi
  substrate.
- Freeze model revision, prompt, tools, task split, seeds, timeout, proposal
  count, task-evaluation budget, and token budget.
- Keep `D_test` invisible until one final evaluation.
- Report held-out solve rate and success-budget AUC separately from diagnosis
  accuracy.

## 2. Method Evidence

### Multi-fidelity allocation [P1]

- Successive halving spends cheap budgets broadly and promotes only competitive
  candidates; BOHB adds model-guided proposal for stronger final performance.
- Prior-guided SH can reduce sample cost, but robustness requires reverting to
  prior-free evidence when the prior is wrong.
- Sources: [BOHB](https://ar5iv.labs.arxiv.org/html/1807.01774),
  [Prior-Guided SH](https://arxiv.org/html/2606.04866).

### Cost-aware stopping [P1]

- The correct objective combines solution regret and cumulative heterogeneous
  evaluation cost.
- A probe should run only when its expected reduction in downstream loss
  exceeds its cost.
- Source: [Cost-aware Stopping](https://arxiv.org/html/2507.12453).

### Set-valued causal replay [P1]

- Pointwise rankings cannot represent conjunctive and alternative repairs.
- Graph-constrained replay can reduce calls while retaining exactness inside a
  declared search domain.
- Sources: [GCJR](https://arxiv.org/html/2608.29228),
  local controlled replay experiments.

## 3. Experiment Outcomes

### H9: Branch quarantine

- Conservative rule: full DGM endpoint 0.5000, cost saving 0%.
- Aggressive rule: saving 86.28%, endpoint falls to 0.2833.
- Reason for failure: safe signals appear on leaves after cost is already paid;
  aggressive pruning removes productive stepping stones.
- Decision: killed.

### H10: Multi-fidelity candidate promotion

- Official panel: 0.5000 retained at 520 versus 660 task evaluations.
- 5,000 hash task rotations: best-node recall 0.8946 and saving 6.58%.
- Reason for failure: low-fidelity rankings are panel-sensitive.
- Decision: killed.

### H11: Repair-First CLM

- Target changed from complete failure-family reconstruction to a one-minimal
  sufficient patch-removal set.
- Balanced conjunctive, alternative, and mixed families:
  - clean: 1.000 repair at 48.52% fewer calls;
  - 5% noise: 0.9733 repair, -0.0100 versus previous CLM, 46.45% fewer calls;
  - 10% noise: 0.9700 repair, -0.0067, 46.19% fewer calls;
  - low-recall slice: 1.000 repair, 42.86% fewer calls;
  - no/misleading prior: 1.000 repair, 49.89%/46.29% fewer calls;
  - DGM-like depth 3-6: 1.000 repair, 43.29% fewer calls.
- Every paired bootstrap 95% interval for call reduction excludes zero.
- Decision: selected algorithmic core.

### DGM-small development endpoint

- Isolated Pi 0.85.1 with DeepSeek resolves 5/10 under depth-1, no-remote,
  no-network task isolation.
- Three one-call causal-slice repairs all pass the official SWE-bench grader:
  13346, 15930, and 10999.
- Combining the retained Pi successes and verified repairs resolves 8/10,
  versus 4/10 for the best released DGM node on the same task IDs.
- Repair overhead is 137,391 reported tokens: 3.99% of all baseline Pi tokens,
  or 12.53% of baseline tokens for the three repaired tasks.
- Source:
  [`endpoint_small_results.json`](endpoint_small_results.json) and its linked
  official grader reports.

## Uncertain Points

- Natural Pi regressions may violate the synthetic failure-family model.
- Full dependency-safe replay can differ from the simple removal intervention;
  the plugin now verifies the exact planned active set and abstains on failure.
- The DGM release cannot establish counterfactual evolution performance.
- Original Pi has no predictions on the released DGM run.
- The released DGM comparison is not same-model or same-agent; matched
  multi-seed evolution and the hidden 140-task evaluation remain outstanding.
- The endpoint gateway reported more output tokens than the requested
  `max_tokens`, so billable-token and monetary-cost claims are not reliable.
