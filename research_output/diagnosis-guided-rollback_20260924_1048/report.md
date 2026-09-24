# Causal Lineage Minimization for pi Harness Rollback

Date: 2026-09-24

## Supersession Notice

This report records the failure-core-first phase through E8. Its selected
diagnosis algorithm and verification counts are superseded by the Repair-First
CLM experiments in
[`../clm_budgeted_evolution_20260924_125503/report.md`](../clm_budgeted_evolution_20260924_125503/report.md).

Repair-First CLM directly minimizes a sufficient patch-removal set instead of
first reconstructing a complete failure-inducing family. It passed all 7/7
pre-registered synthetic settings: repair success was 0.9700-1.0000 and probe
calls fell 42.86%-49.89% versus the previous failure-first path. This is the
selected algorithmic core. It still has not established an end-to-end
SWE-bench win over DGM or original Pi.

## Executive Conclusion

The original direction, "let one LLM choose a rollback ancestor from patch
descriptions and current scores," is not supported. Prompt-only ranking became
slower and less calibrated, while the original DGM oracle mixed incomparable
10/60/200-task scores.

The method that survives the evidence is **Causal Lineage Minimization (CLM)**:

1. Use an LLM and dependency metadata only to rank candidate historical patches.
2. Let executable counterfactual replay determine the failure-inducing patch
   set.
3. Roll back to the checkpoint before its earliest member.
4. Replay later gains only when they do not depend on, or overlap files changed
   by, removed patches.
5. Use sliced search only behind an audited cost gate; otherwise use full ddmin.

This gives a precise, conservative plugin design. It does not yet justify a
headline claim on real SWE-bench failures.

The pre-registered released-DGM pilot confirms that boundary verification can
repair selected delayed failures, but rejects the current low-cost claim:
CLM reached 12/12 repair at 1.5000 evaluator probes versus linear scan's
12/12 at 1.0833. DeepSeek's unverified top-1 choice was only 4/12. This is a
**REVISE** result, not evidence that CLM beats DGM or original Pi end to end.

## Diagnosis of the Performance Problem

| Evidence | Result | Consequence |
|---|---:|---|
| Static LLM fork ranking v1 | hit 0.4545; regret 0.0538 on the original oracle | No demonstrated advantage |
| Structured prompt v2 | hit 0.3636; regret 0.0797; ~42 min vs ~2 min | More reasoning did not improve calibration |
| DGM oracle audit | strict disagreement falls from 4/11 to 1/11 | Original fork claim withdrawn |
| Controlled attribution | full-evidence 1.0 on 12 cases | Positive control only because evidence reveals the injected mechanism |
| Corrected DGM census | 56/69 monotone; 13 non-monotone | Earlier 245/226 result omitted evaluator error IDs and is withdrawn |
| Corrected binary vs linear | 0.9710 vs 1.0000 exact; 1.7246 vs 1.4783 probes | Bisection is less accurate and more expensive over all corrected episodes |
| Synthetic full ddmin | clean exact 1.000 | Interaction-aware localization works in the declared model |
| Synthetic 40% slice | exact 1.000 clean, 0.967 at 5%/10% noise; 11%-14% saving | Universal low-cost claim rejected |
| Slice sensitivity | 26%-37% saving at <=30% slice and >=95% recall | This becomes the explicit cost gate |
| DGM CLM pilot | 1.0000 repair at 1.5000 probes vs linear 1.0000 at 1.0833 | E8 killed on cost; do not expand |

The root issue is therefore not insufficient prompt sophistication. A failed
trajectory does not uniquely identify its cause, and harness components interact
non-additively. A semantic guess must be converted into an executable
counterfactual.

## Released-DGM Benchmark Verdict

After fixing submitted-task accounting, the canonical D60 endpoints are:

| Released system | Fixed-D60 solved |
|---|---:|
| DGM initial agent | 12/60 (20.00%) |
| DGM best node | 30/60 (50.00%) |
| No open-ended exploration | 14/60 (23.33%) |
| No self-improvement | 23/60 (38.33%) |

These are single released runs. The DGM initial agent is not this repository's
current TypeScript Pi agent.

On all 41 corrected monotone delayed-regression episodes, no rollback and
rollback-1 repair 0%; a same-task score-only DGM proxy repairs 19.51%; exact
linear and binary search repair 100% at 1.0244 and 1.3659 mean probes.
The two 0% values are guaranteed by selecting current failures whose immediately
preceding scored state also fails; they are construction checks rather than
general policy estimates.

The deterministic 12-episode DeepSeek pilot covers only four unique tasks.
CLM repairs 100%, versus 0% for rollback-1 and 8.33% for the score-only proxy,
but uses 1.5000 probes versus linear's 1.0833. Three of 12 cases require the
verified fallback; shallow paths often bypass the semantic slice entirely.
Reported model usage is 52,754 input tokens, 181,072 output tokens, and 767.291
summed seconds over 12 calls.

Therefore CLM beats the weak recovery policies on this selected offline slice,
but does not beat the strongest recovery baseline on cost. Logged trajectories
cannot reveal the agents that CLM would have generated after choosing a
different parent, so this experiment cannot compare CLM's final task-solving
rate with DGM's fixed-D60 50%. No matching original-Pi predictions exist. The
pilot exercises only CLM's monotone boundary fast path, not interaction ddmin,
selective replay, or post-rollback evolution. Prompt aliases hide node and task
IDs, but memorization of public trajectory text remains a validity risk.

## Selected Method

### Inputs

- A linear checkpoint lineage for the active pi session branch.
- Content-addressed snapshots of explicitly configured harness artifacts.
- A failure bundle containing the observed failure, optional candidate slice,
  prior order, and reproducibility metadata.
- A configurable external probe that evaluates an arbitrary active patch set.

### Diagnosis

1. Verify that the current lineage fails and the baseline passes. Otherwise
   abstain.
2. Resolve the optional LLM prior and dependency slice. Never hard-prune from
   the prior alone.
3. Test the top-ranked singleton.
4. If needed, run ddmin on the slice only when:
   `slice_fraction <= 0.30` and `audited_recall >= 0.95`.
5. Run ddmin directly over removal sets. If removing the candidate slice does
   not repair the full lineage, fall back to full-lineage removal-ddmin.
6. Record a one-minimal sufficient removal set. Complete failure-family
   reconstruction is optional because it is not required to repair the
   observed failure.

### Rollback and Replay

The rollback checkpoint is the parent of the earliest removed patch. Later
patches are replayed in lineage order only when:

- they do not declare a dependency on a removed or skipped patch; and
- their changed files do not overlap files changed by a removed or skipped
  patch.

This is conservative. Full-file snapshots cannot prove that overlapping edits
commute, so ambiguous patches are skipped rather than silently merged.

## Plugin

The standalone package is in `pi-rollback/`.

Commands:

```text
/rollback checkpoint [label] [--depends id,id]
/rollback diagnose <failure-bundle.json>
/rollback status
/rollback apply [diagnosis-id]
/rollback apply [diagnosis-id] --execute
```

Key properties:

- Installable as a normal pi package through its `package.json` manifest.
- Dry-run by default; application requires configuration, `--execute`, and an
  interactive confirmation.
- No `git reset`, `git checkout`, or `git stash`.
- Restores only configured artifact paths.
- Rejects absolute paths, parent traversal, Git internals, symlinks, corrupted
  manifests, and corrupted snapshot files.
- Persists checkpoint/diagnosis state as pi `CustomEntry` records.
- Stores probe requests, raw output, latency, token/cost/retry telemetry,
  hashes, fallback state, and abstention reason under `.pi/rollback/runs/`.
- Restores artifact state before `navigateTree()` and `reload()`; pi's session
  tree alone does not restore files.

Verification completed:

- Plugin TypeScript and Biome checks pass.
- 15 plugin tests pass, covering interaction recovery, slice fallback, cost
  gating, baseline abstention, dependency-aware replay, exact final-plan
  verification, external probe telemetry, snapshot restore, path confinement,
  and corruption detection.
- 27 Python experiment tests pass.
- `npm pack --dry-run` includes the extension, source, fixtures, and README.

## Novelty Boundary

The broad idea of counterfactual replay is not novel. [GCJR](https://arxiv.org/html/2608.29228)
already studies graph-constrained joint replay and minimal repair families over
execution events. [DiagEval](https://arxiv.org/html/2605.17439) establishes the
single-trajectory identifiability gap and motivates information-value probes.
[SemLoc](https://arxiv.org/html/2603.29109v1) shows why semantic hypotheses need
executable grounding. [Time Travel](https://arxiv.org/html/2511.18854) documents
the limits of ordinary bisect under flaky or non-monotone behavior.

The narrower contribution available here is:

- moving counterfactual minimization from execution events to a persistent
  cross-generation harness patch lineage;
- producing a rollback-and-selective-replay plan rather than only a culprit
  rank;
- integrating artifact snapshots with pi session-tree navigation without
  forking pi core; and
- exposing an empirical cost gate that disables the fast path outside its
  validated operating region.

[Agentic Harness Engineering](https://arxiv.org/html/2604.25850v3) is especially
important positioning: it reports regression blindness and non-additive
component interactions, which motivate CLM but also reduce the novelty of broad
"harness observability" claims. [DGM](https://arxiv.org/html/2505.22954) remains
the parent-selection baseline, not evidence that rollback itself is solved.

## Required Real-World Validation

Before a performance-oriented GitHub release or paper claim:

1. Collect real pi harness regression lineages from held-out public tasks.
2. Freeze the evaluator, task split, prompt, model, and artifact schema.
3. Compare rollback-1, linear first-bad, full ddmin, and gated CLM.
4. Report repair success, earliest-cause distance, replay calls, wall time,
   token/cost, abstention, fallback rate, and preserved later gains.
5. Run a clean held-out test set once after method selection.

Kill criteria:

- Remove the precision claim if CLM repair success is below full ddmin.
- Remove the cost claim if gate-eligible lineages do not reduce total replay
  cost by at least 20%.
- Remove selective replay if dependency/overlap filtering loses more downstream
  gain than a full rollback baseline.

## Release Positioning

The defensible first release is an experimental, safety-first pi extension:
"auditable causal rollback with pluggable probes," not "proven low-cost
SWE-bench rollback." The deterministic fixture provides a zero-API demo; the
real differentiator should be a reproducible public benchmark trace added next.
