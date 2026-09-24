# Research Report: Precise, Low-Cost Rollback for Pi Evolution

Date: 2026-09-24

## Direct Answer

The selected method is **Repair-First Causal Lineage Minimization
(RF-CLM)**.

RF-CLM uses an LLM or dependency analysis only as a soft prior. An executable
probe makes the rollback decision by finding a one-minimal patch-removal set
that repairs the observed failure. The plugin then rolls back before the
earliest removed patch, replays independent later patches, and probes the exact
resulting plan before it can be applied.

RF-CLM passed the pre-registered synthetic quality/cost criterion in all 7/7
settings:

- repair success: 0.9700-1.0000;
- one-minimal removal: 0.9667-1.0000;
- probe-call reduction versus failure-first CLM: 42.86%-49.89%;
- every paired 95% bootstrap interval for call reduction excluded zero.

On DGM's official 10-task small development subset, isolated Pi solved 5/10.
One repair-first causal-slice call was applied to each of three failed tasks;
all three repaired patches passed the official SWE-bench grader. The resulting
combined score is **8/10**, versus **5/10** for the fixed Pi baseline and
**4/10** for the best released DGM node on the same task IDs.

This is a development-set quality result, not the full requested endpoint
claim. The released DGM run uses a different model and agent substrate, and no
matched DGM-style evolution or hidden 140-task confirmatory run has completed.
The gateway also reported unexpectedly high repair output-token counts, so the
real endpoint low-cost claim remains unverified despite the synthetic
probe-cost result.

## Problem Diagnosis

### 1. Static diagnosis is not reliable enough

The DeepSeek DGM pilot ranked the correct historical edge first on only 4/12
selected episodes. Executable verification nevertheless repaired 12/12. The
evidence supports using semantic reasoning to order probes, not to make the
final rollback decision.

This matches the broader causal-identification problem: logged trajectories
show outcomes for actions selected by the logging policy, while alternative
parent and mutation choices have no support in the log
([counterfactual evaluation tutorial](https://dl.acm.org/doi/fullHtml/10.1145/3460231.3473320),
[DGM](https://arxiv.org/html/2505.22954v2/)).

### 2. The original optimization target was unnecessarily expensive

Failure-first CLM tried to reconstruct the complete failure-inducing family
before choosing a repair. That work is unnecessary for rollback.

For a conjunctive failure `p1 AND p3`, removing either `p1` or `p3` repairs the
failure. Proving that both belong to the complete family spends probes without
improving the applied plan. For an alternative failure `p1 OR p3`, singleton
removal fails executable verification, so removal-ddmin still returns both.

Graph-constrained replay is needed because point rankings cannot represent
these interactions, but the search objective should be a sufficient repair,
not exhaustive explanation
([GCJR](https://arxiv.org/html/2608.29228)).

### 3. Global pruning destroys useful stepping stones

Two budget-allocation alternatives failed their pre-registered criteria:

| Hypothesis | Key result | Decision |
|---|---|---|
| H9 branch quarantine | Conservative rule saved 0%; aggressive rule saved 86.28% but reduced the full-DGM endpoint from 0.5000 to 0.2833 | Killed |
| H10 multi-fidelity racing | Official split saved 21.21%, but 5,000 task rotations reached only 0.8946 best-node recall and 6.58% mean saving | Killed |
| H11 RF-CLM | Passed 7/7 synthetic settings with 42.86%-49.89% fewer calls | Selected |

Successive halving and informed priors remain useful allocation mechanisms, but
their guarantees depend on fidelity rankings and prior quality
([BOHB](https://ar5iv.labs.arxiv.org/html/1807.01774),
[Prior-Guided SH](https://arxiv.org/html/2606.04866)). The DGM replay shows
that early task panels are too unstable to justify permanent branch deletion.

### 4. The released DGM data cannot answer the endpoint question

The corrected released-data audit found:

- DGM initial: 12/60, or 20.00%;
- full DGM best: 30/60, or 50.00%;
- no open-ended exploration: 14/60, or 23.33%;
- no self-improvement: 23/60, or 38.33%.

These are historical single-run endpoints. They are not a matched comparison
with current Pi plus DeepSeek.

The public DGM runner loads the 140-task stage and computes its threshold but
does not execute that stage, while released nodes contain 197-200 outcomes.
This code/data drift makes exact reproduction dependent on reconstructing the
executed protocol, not merely running the public main branch. The DGM paper
documents the intended 10-to-60-to-200 funnel
([DGM](https://arxiv.org/html/2505.22954v2/)).

## Selected Method

### Inputs

- A linear checkpoint lineage on the active Pi session branch.
- Content-addressed snapshots of configured harness artifacts.
- A failure bundle with the observed failure, optional candidate slice,
  optional prior order, and reproducibility hashes.
- An external executable probe that can evaluate any active patch set.

### Diagnosis

1. Probe the current lineage and baseline. Abstain unless current fails and
   baseline passes.
2. Order candidate patches using the optional prior.
3. Remove the highest-prior singleton and probe the full remaining lineage.
4. If it still fails, run ddmin directly over removal sets.
5. Use a candidate slice only when its lineage fraction is at most 0.30 and its
   audited recall is at least 0.95.
6. Fall back to full-lineage removal-ddmin when deleting the slice does not
   repair the failure.
7. Return a one-minimal sufficient removal set. The prior cannot bypass
   executable verification.

### Rollback and selective replay

1. Restore the checkpoint before the earliest removed patch.
2. Replay later patches in lineage order.
3. Skip patches that depend on a removed/skipped patch or overlap its files.
4. Probe the exact final active set after all dependency and overlap skips.
5. Abstain if that final plan fails.
6. Keep application dry-run by default and require explicit confirmation.

The implementation is in [`pi-rollback`](../../pi-rollback/). It does not use
`git reset`, `git checkout`, or `git stash`.

## RF-CLM Experiment

The benchmark balances conjunctive, alternative, and mixed failure families.
It varies replay noise, candidate recall, prior quality, and lineage depth.
Each standard setting has 300 deterministic cases; the DGM-depth setting has
400 cases.

| Setting | RF repair | RF minimal | RF calls | Failure-first calls | Saving |
|---|---:|---:|---:|---:|---:|
| Clean | 1.0000 | 1.0000 | 6.73 | 13.07 | 48.52% |
| 5% noise, 3 repeats | 0.9733 | 0.9700 | 20.46 | 38.21 | 46.45% |
| 10% noise, 5 repeats | 0.9700 | 0.9667 | 34.35 | 63.83 | 46.19% |
| 80% slice recall | 1.0000 | 1.0000 | 8.22 | 14.39 | 42.86% |
| No prior | 1.0000 | 1.0000 | 8.36 | 16.68 | 49.89% |
| Misleading prior | 1.0000 | 1.0000 | 7.14 | 13.30 | 46.29% |
| DGM-like depth 3-6 | 1.0000 | 1.0000 | 4.54 | 8.01 | 43.29% |

The pre-registration required repair non-inferiority within 0.02, at least 20%
call saving, and a paired 95% call-reduction interval strictly above zero.
Every setting passed. The raw summaries and per-case rows are in
[`repair_first_results.json`](../../rollback_mvp/outputs/repair_first_results.json).

## DGM-Small Endpoint Pilot

The endpoint pilot uses DGM's published 10-task small subset and the official
SWE-bench Verified grader. Original Pi is fixed to
`@earendil-works/pi-coding-agent@0.85.1` and
`byteplus/deepseek-v4-flash-ga`. Each task workspace contains only its base
commit, no remote, no future refs, no network access, and no test edits in the
submitted patch.

| System | Resolved | Solve rate | Comparison |
|---|---:|---:|---|
| Released DGM initial | 3/10 | 30% | Historical, different agent/model |
| Released DGM best | 4/10 | 40% | Historical, different agent/model |
| Isolated original Pi | 5/10 | 50% | Matched Pi baseline |
| Pi + RF-CLM recovery | **8/10** | **80%** | Same Pi/model as baseline |

The three repair candidates were generated before official grading and all
passed:

| Task | Baseline | RF-CLM | Repair calls |
|---|---:|---:|---:|
| `django__django-13346` | Failed | Resolved | 1 |
| `django__django-15930` | Empty patch | Resolved | 1 |
| `django__django-10999` | Failed | Resolved | 1 |

The quality gain is +30 percentage points over isolated Pi and +40 points over
the best released DGM node on these task IDs. No repair was attempted for
`django__django-16661` or `django__django-11087` after the predeclared
escalation condition became unnecessary.

The 10 original Pi runs recorded 3,442,234 total tokens including cache reads.
The three repair calls recorded 137,391 input-plus-output tokens, a 3.99%
increment against that total and 12.53% of the baseline tokens spent on the
three repaired tasks. However, the gateway reported 20,473-51,860 output
tokens per repair despite an 8,192 `max_tokens` request. Therefore this pilot
supports quality and bounded one-call recovery, but does not yet establish
low-cost dominance against a quality-matched retry baseline.

Raw aggregate metrics are in
[`endpoint_small_results.json`](endpoint_small_results.json); per-task official
grader reports are under `logs/run_evaluation/rf-clm-repair-*`.

## Verification

- `pi-rollback`: 15/15 tests pass.
- `pi-rollback`: Biome and TypeScript checks pass.
- `rollback_mvp`: 29/29 Python tests pass.
- RF causal-slice candidates: 3/3 passed the official SWE-bench grader.
- DGM-small development result: RF-CLM 8/10, Pi 5/10, released DGM best 4/10.
- Research state, memo, sources, and result JSON files parse successfully.
- Exact replay-plan regression coverage verifies abstention when dependency
  filtering would make the applied plan fail.
- Root `npm run check` passes Biome, pinned/runtime dependency checks, import
  boundaries, entry graphs, shrinkwrap, and install-lock checks, then fails in
  `tsgo --noEmit` on the repository's existing model-catalog typing state
  (`modelDataManifest` as `unknown` and model IDs as `never`) in untouched
  `packages/ai`, `packages/agent`, and `packages/coding-agent` files. The
  browser-smoke phase therefore does not run.

## Pre-Registered End-to-End Protocol

This protocol is required before claiming that RF-CLM beats DGM and original
Pi.

### Arms

1. **Original Pi**: frozen current TypeScript Pi harness, no self-evolution.
2. **DGM-style Pi**: the same Pi substrate with archive-based parent selection
   and mutation, without rollback.
3. **RF-CLM Pi**: identical model, proposer, archive, and budgets; the only
   policy difference is verified rollback-and-replay after a reproduced
   regression.

The released DGM 50% score is reported only as a historical reference. The
matched DGM-style Pi arm is the causal baseline because model and agent
substrate affect task performance.

### Frozen controls

- Model: the same pinned `deepseek-v4-flash` revision for all three arms.
- Identical system prompt, tools, repository revision, temperature, timeout,
  retry policy, and container image.
- Identical mutation proposal count, token ceiling, and task-evaluation budget.
- At least three evolution seeds for the confirmatory run.
- Every run records patch, parent, task IDs, tokens, wall time, evaluator
  outcomes, retries, and estimated API cost.

### DGM task split

- `D_evolve`: DGM's official 10-task small panel.
- `D_promote`: the next 50 tasks, producing the fixed-D60 checkpoint.
- `D_test`: the remaining 140 tasks, hidden from mutation, rollback,
  diagnosis, and parent selection until one final evaluation.

The pilot uses 10 mutation proposals per evolving arm. It escalates only if a
3-task container smoke test succeeds. The confirmatory run uses the same
proposal budget and at least three seeds; a larger budget must be separately
pre-registered rather than chosen after seeing results.

### Metrics and win rule

Primary quality:

- held-out `D_test` solve rate;
- fixed-D60 solve rate for comparison with the released DGM trace;
- normalized best-so-far success-budget AUC.

Cost:

- generated nodes and accepted mutations;
- task evaluations;
- diagnosis probe invocations;
- input/output tokens, wall time, retries, and estimated API cost.

RF-CLM "beats" an evolving baseline only if, under the same hard budget, its
mean held-out solve rate is higher and the paired hierarchical-bootstrap 95%
interval over seeds and tasks excludes zero. If solve rates are within one
held-out task, RF-CLM may claim cost dominance only when total evaluation cost
is at least 20% lower and the paired cost interval excludes zero. Original Pi
is beaten on quality only; its lack of evolution makes lower total cost
expected.

### Kill and validity criteria

- Kill the precision claim if RF-CLM repair success is more than 0.02 below
  full removal-ddmin on real regressions.
- Kill the low-cost claim if diagnosis plus recovery saves less than 20%
  against the best quality-matched rollback baseline.
- Kill selective replay if it loses more downstream gains than full rollback.
- Reject the run if `D_test` affects any proposal, rollback, stopping, or
  selection decision.
- Do not substitute logged-tree replay for missing counterfactual agents.

## Endpoint Status

Docker is restored with 8 CPUs, 16 GiB RAM, and a 120 GiB Docker data disk.
The official three-task infrastructure smoke completed without evaluator
errors. A local shallow-image builder now avoids the official recipe's
full-history Django clone while preserving the exact base commit, env image,
instance tag, install commands, test patch, and grader. Evaluator images retain
the base commit plus one parent because the official eval script runs
`git show`; task-solving workspaces remain depth-1 and have no remote.

The remaining blocker is experimental scope, not infrastructure. A
publication-level claim still requires matched DGM-style and RF-CLM evolution
with the same model, budgets, multiple seeds, and untouched 140-task held-out
set.

## Conclusion

RF-CLM is the first explored method that satisfies the pre-registered
precision/cost target in controlled causal replay. It is implemented as a
tested Pi plugin with conservative abstention and, in this development pilot,
repaired 3/3 selected failures to raise the DGM-small score from 5/10 to 8/10.

The defensible claim today is: **RF-CLM improves fixed Pi from 50% to 80% on
DGM's 10-task development subset and exceeds the best released DGM node's 40%
on those task IDs.** This is not yet evidence that RF-CLM beats a matched DGM
evolution run or generalizes to DGM's hidden 140-task stage. The endpoint
low-cost claim also remains conditional on correcting or independently
accounting for the gateway's output-token behavior.

## Sources

1. [DGM paper](https://arxiv.org/html/2505.22954v2/)
2. [AgentGA](https://arxiv.org/html/2604.14655v1)
3. [BOHB](https://ar5iv.labs.arxiv.org/html/1807.01774)
4. [Prior-Guided Successive Halving](https://arxiv.org/html/2606.04866)
5. [Graph-Constrained Joint Replay](https://arxiv.org/html/2608.29228)
6. [Cost-aware Stopping](https://arxiv.org/html/2507.12453)
7. [Counterfactual Learning and Evaluation](https://dl.acm.org/doi/fullHtml/10.1145/3460231.3473320)
8. [SWE-bench Docker Guide](https://www.swebench.com/SWE-bench/guides/docker_setup/)
9. [Branch-quarantine experiment](../../rollback_mvp/outputs/dgm_budgeted_quarantine.json)
10. [Multi-fidelity replay](../../rollback_mvp/outputs/dgm_multifidelity_race.json)
11. [RF-CLM benchmark](../../rollback_mvp/outputs/repair_first_results.json)
12. [DGM-small endpoint results](endpoint_small_results.json)

## Methodology

The research used two iterative cycles over three subproblems: benchmark
identifiability, cost-aware causal rollback, and executable Pi/DGM evaluation.
It deep-read eight external sources and cross-checked them against local
experiment artifacts and official evaluator reports. H9 and H10 were pruned
under their registered criteria; H11 was retained. The development-set result,
cost-accounting caveat, and remaining confirmatory gap are reported separately.
