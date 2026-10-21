# Research Memo

## Subproblem 1: Diagnose current performance

### Local experiment artifacts [P1-project evidence]
- Static subtree prediction showed no robust advantage; its original
  four-disagreement evaluation was invalidated by unequal staged task subsets.
- Structured prompting increased explanation detail but worsened regret.
- Controlled failure bundles were solved reliably when concrete debug evidence
  was present, but the cases are synthetic and highly diagnostic.
- After common-task-set correction, only 1/11 DGM forks is a strict
  greedy/oracle disagreement. The earlier 4/11 statistic is invalid.
- The submitted-task parser originally omitted evaluator `error_ids`; the
  resulting 245/226/92.24% lineage statistics are invalid. The corrected
  census is 69 failure episodes: 56 monotone and 13 non-monotone.
- On all corrected episodes, binary search is both less accurate and more
  expensive than linear scan (0.9710 vs 1.0000 exact; 1.7246 vs 1.4783 probes).
- Counterfactual ddmin recovered all clean synthetic 1-3 edge causes. A
  dependency slice is a cost win only when it covers <=30% of edges with
  audited cause recall >=95%.
- In the 12-episode released-DGM pilot, CLM repaired 12/12 but used 1.5000
  probes versus linear's 1.0833; DeepSeek top-1 was 4/12. The pre-registered
  low-cost hypothesis is killed.

### Local code audit [P1-project evidence]
- The original DGM oracle used raw accuracies from unequal 10/60/200 staged
  subsets; the corrected implementation uses one common task set and
  set-valued ties.
- Plurality ties are broken by dictionary insertion order and can flip the
  prompt-v2 kill conclusion.
- Controlled case IDs and directed observations leak semantic labels.
- The controlled benchmark validates latent implementation bugs, not the strong
  "individually correct but low-future-yield premise" claim.

### Agentic Harness Engineering [P1-paper] ([URL](https://arxiv.org/html/2604.25850v3))
- File-level component observability, layered trajectory evidence, and
  prediction manifests make harness edits auditable.
- Fix attribution can be reliable while regression attribution remains blind.
- Harness components interact non-additively.

## Subproblem 2: Low-cost rollback algorithms

### GCJR [P1-paper] ([URL](https://arxiv.org/html/2608.29228))
- Pointwise rankings cannot represent jointly necessary or alternative repairs.
- Dependency slicing + graph-feasible singleton/pair counterfactual replay
  recovers the complete minimal repair family in its declared domain.
- Reported replay savings are 52-55% versus exhaustive search.

### DiagEval [P1-paper] ([URL](https://arxiv.org/html/2605.17439))
- A single failed trajectory has an identifiability gap.
- Targeted probes ranked by information value outperform blind retry.
- Probe outcomes update attribution and support an explicit stopping rule.

### SemLoc [P1-paper] ([URL](https://arxiv.org/html/2603.29109v1))
- Free-form LLM localization is not verifiable.
- Semantic hypotheses become useful after grounding to executable constraints.
- Counterfactual verification adds 12 percentage points Top-1 in its benchmark.

### Time Travel [P1-paper] ([URL](https://arxiv.org/html/2511.18854))
- Ordinary bisect is logarithmic only with a deterministic monotone predicate.
- Flaky and non-monotone behavior breaks standard binary search.
- Semantic commit reasoning improves bisect but still localizes first-bad
  behavior, not necessarily an earlier interacting premise.

## Subproblem 3: pi extension and open-source workflow

### Emerging design
- LLM proposes a small candidate repair family; it does not make the verdict.
- A dependency slice removes irrelevant historical patches.
- Counterfactual replay verifies singleton candidates, then runs ddmin for
  interaction causes.
- An information-value gate stops early when a verified singleton suffices.
- The plugin must expose immutable manifests: prompt/data/model/git hash,
  replay count, token/cost/latency, raw response, and fallback/abstain state.
- The rollback plan targets the parent of the earliest causal patch, then
  topologically replays later patches that do not depend on the causal set.
- The plugin must store artifacts independently of pi's session tree:
  `navigateTree()` changes conversation state but does not restore files.

## Uncertain Points

- Whether real failure trajectories contain enough stable evidence for one-shot
  attribution.
- Whether failure behavior is monotone enough along a lineage for binary-search
  style probes.
- Whether partial task probes remain cheaper than proposal cost after accounting
  for repeated seeds and noise.
- Whether selective reversion can preserve later patches when they depend on the
  removed edge.
- Novelty relative to 2026 counterfactual-replay work is narrower than the
  original document claims.
- Real pi/SWE-bench failures have not yet validated attribution accuracy,
  repair success, or end-to-end cost savings.
- Released DGM trajectories cannot estimate the counterfactual agents CLM would
  generate after changing parent/mutation decisions, and no matching original
  Pi predictions are available.
