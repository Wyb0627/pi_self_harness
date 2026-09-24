# Exploration Log: Diagnosis-Guided Rollback

This log records hypotheses before experiments, implementation changes, results,
and reasons for success or failure. Metrics and labels are not rewritten after
results; corrections are appended with their justification.

## Existing Evidence

### E0: Static subtree prediction, prompt v1

- Setup: DGM released SWE tree, 11 sibling forks, deepseek-v4-flash, five votes.
- Result: all-fork hit 0.4545 / regret 0.0538; disagreement hit 0/4 / regret 0.1363.
- Interpretation: intent, patch, and current score are insufficient for reliable
  prediction of the best future subtree.
- Audit status: historical only. The oracle mixed unequal staged task subsets;
  these values are not valid performance estimates.

### E1: Static subtree prediction, prompt v2

- Change: force per-child analysis of coupling, generality, composability, and
  future repair cost.
- Pre-run prediction: at least 1/4 disagreement hits and regret below greedy
  0.1353.
- Kill criterion: 0/4 hits or regret not below 0.1353.
- Result: 1/4 hits, regret 0.1533. Kill criterion met.
- Failure reason: better-looking analysis did not improve calibration. The prompt
  over-rewarded modular/low-coupling changes and changed two previously correct
  choices into high-regret errors. Two plurality ties also exposed unstable
  tie-breaking.
- Audit status: historical only. The corrected common-task-set oracle leaves
  insufficient disagreement cases for this confirmatory test.

### E2: Controlled delayed-failure attribution

- Setup: 12 controlled histories, including 10 delayed latent defects and two
  latest-edge controls. Five votes per condition.
- Result: rollback-1 exact 0.1667; highest-score exact 0.1667; LLM no-debug
  vote exact 0.9500 and case exact 0.9167; LLM full-evidence exact 1.0000.
- Positive-control audit: one original oracle labeled the activating gate rather
  than the earlier latent parser defect. The label was corrected to match the
  project's strong definition, then the full experiment was independently rerun.
- Interpretation: explicit runtime evidence can support accurate historical
  attribution in controlled cases. This is a mechanism smoke test, not evidence
  of accuracy on real failures.

## Hypothesis Tree

### H1: Static Predictive Ranking

- HYPOTHESIS: A single LLM can predict the most productive future subtree from
  mutation intent, diff, and current score.
- MECHANISM: architectural reasoning recognizes toxic stepping stones before
  downstream failures occur.
- COMPARISON: greedy current-score parent selection.
- KILL CRITERION: no lower regret than greedy on DGM disagreement forks.
- STATUS: NOT SUPPORTED. E0/E1 did not show an advantage, but their original
  oracle was later invalidated; the hypothesis is not claimed as statistically
  falsified.

### H2: Evidence-Conditioned One-Shot Attribution

- HYPOTHESIS: Given a real failure bundle, one LLM call can identify the earliest
  latent culprit edge with materially higher exact accuracy than rollback-1.
- MECHANISM: runtime evidence links observed behavior to a historical code change.
- COMPARISON: rollback-1, highest-score ancestor, and no-debug ablation.
- KILL CRITERION: exact rollback <= rollback-1, or full evidence does not improve
  over no-debug.
- CHEAPEST TEST: controlled delayed-failure histories.
- STATUS: PASSED controlled smoke test E2; unvalidated on real failures.

### H3: Evidence-Gated Active Rollback

- HYPOTHESIS: An LLM prior plus adaptively selected verification probes can match
  exhaustive ancestor evaluation while using substantially fewer task runs.
- MECHANISM: failure evidence produces a probability distribution over culprit
  edges; a probe is run only when uncertainty is high, selecting the
  version/task pair with highest expected information gain.
- COMPARISON: rollback-1, highest-score parent, one-shot LLM, linear ancestor
  scan, and full evaluation.
- PRE-RUN PREDICTION: exact rollback >= 0.80 on held-out controlled/noisy cases,
  with median probe count <= ceil(log2(path length)); on real DGM replay, lower
  decision regret than one-shot LLM at <50% of linear-scan probe cost.
- KILL CRITERION: no accuracy gain over one-shot LLM, or probe cost >= linear
  scan on median, or performance collapses under 10% probe noise.
- CHEAPEST TEST: offline simulated probes using hidden per-version outcomes,
  before Docker/SWE-bench execution.
- STATUS: PARTIALLY SUPPORTED by E3-E7. Counterfactual minimization is accurate
  in the synthetic declared domain, but neither shallow-lineage bisection nor
  40%-slice ddmin provides a universal cost win. The retained method uses hard
  cost gates and full-search fallback.

## Search Iterations

### Iteration 0

- Initialized three subproblems and four parallel investigations.
- Firecrawl/Exa MCPs were unavailable; research uses WebSearch/WebFetch fallback.
- Next: audit current code/results, perform three-query-variant prior-work search,
  then choose the cheapest H3 killing test.

### Iteration 1

#### Credibility audit

- **P0: unequal-subset oracle.** `subtree_best_accuracy` and greedy selection use
  raw 10/60/200-task accuracies. The documented task-intersection rule is not
  applied to the premise-selection oracle. Existing DGM v1/v2 numbers are
  suspended until this is fixed.
- **P0: tie-sensitive conclusion.** `run.py` resolves plurality ties by insertion
  order. In prompt v2, selecting the other tied candidate at `initial` would
  materially improve the reported disagreement regret. The prompt-v2 kill
  conclusion is therefore not stable.
- **P0: controlled semantic leakage.** Case IDs such as
  `compaction-drops-contract` and some debug statements identify the mechanism.
  The 1.0 controlled score is a positive-control result, not an accuracy
  estimate.
- **P1: claim mismatch.** The DGM fork task predicts a productive sibling and is
  not failure attribution. Controlled cases mostly contain latent implementation
  bugs, not individually correct toxic premises.
- **P1: weak baselines.** Hand-authored monotone scores make rollback-1 and
  highest-score identical in all controlled cases.
- **P1: missing cost telemetry.** LLM token usage, latency, retry count, and
  estimated cost are discarded.
- **Security:** the experiment copied an effective gateway credential into
  source. It was removed; LLM runs now require `ROLLBACK_LLM_API_KEY`.

#### Prior-work impact

- GCJR directly establishes that pointwise attribution misses joint and
  alternative repairs; graph-constrained replay recovers minimal repair
  families with about 52-55% fewer calls than exhaustive search.
- DiagEval establishes the single-trajectory identifiability gap and uses
  information-value probes instead of blind retry.
- SemLoc supports the design pattern "LLM proposes structured hypotheses;
  executable counterfactuals decide."
- Time Travel shows ordinary bisect is invalid under flaky/non-monotone
  predicates.
- AHE independently reports regression blindness and non-additive harness
  component interactions.

#### Candidate method: staged active counterfactual rollback

1. Build a soft prior over lineage edges from LLM diagnosis, change impact, and
   historical branch credit. Never hard-prune from this prior.
2. For an apparently monotone regression, query the posterior-median version
   (probabilistic bisection), maximizing expected entropy reduction per unit
   probe cost.
3. Estimate probe noise at known good/bad endpoints and update the edge posterior
   with explicit false-positive/false-negative rates.
4. On non-monotone evidence or suspected interactions, switch to a small
   dependency-sliced window and run counterfactual `ddmin` over patch subsets.
5. Return a minimal causal edge set (hyperedge) plus the earliest member as the
   rollback recommendation. Preserve alternative repair sets when they exist.
6. Stop when posterior confidence is high and boundary verification passes;
   retain periodic audit probes.

This is narrower and more defensible than "LLM chooses the rollback point." The
LLM generates and prioritizes hypotheses; replay certifies them.

## Experiments

### E3: Is a bisect fast path viable on the real DGM tree?

- HYPOTHESIS: Most per-task outcome sequences along a DGM lineage have one
  pass-to-fail transition, so logarithmic probing is useful as a fast path.
- COMPARISON: observed task outcomes along every scored root-to-leaf path.
- PRE-RUN PREDICTION: at least 80% of eligible sequences are monotone.
- KILL CRITERION: fewer than 70% are monotone, which would make bisection a
  poor default.
- CHEAPEST TEST: read existing DGM per-node task outcomes; no API or benchmark
  execution.
- RESULT: 245 eligible leaf/task episodes; 226 monotone (92.24%), 19
  non-monotone (7.76%). All non-monotone episodes had three observed
  transitions such as pass-fail-pass-fail.
- INTERPRETATION: the fast path is justified but cannot be the only path.
  A non-monotonicity detector and interaction-capable fallback are mandatory.
- STATUS: HYPOTHESIS SUPPORTED within this released tree. This measures visible
  task behavior, not earliest latent-cause correctness.

### E4: Can dependency-sliced ddmin recover interacting lineage causes cheaply?

- HYPOTHESIS: On lineages with one 1-3-edge conjunctive cause set,
  dependency-sliced ddmin with safety fallback matches full ddmin while reducing
  replay cost.
- COMPARISON: rollback-1, prefix linear scan, prefix binary search, full ddmin,
  and sliced ddmin.
- PRE-RUN PREDICTION:
  - deterministic exact cause-set recovery >= 0.99;
  - with 5% probe noise and three paired repeats, exact recovery >= 0.95;
  - median replay calls at least 40% lower than full ddmin when the dependency
    slice retains all causes and 40% of distractors.
- KILL CRITERION: deterministic exact < 0.99, noisy exact < 0.95, or call
  reduction < 20%.
- CHEAPEST TEST: generated lineages with 8/16/32 edges, hidden cause sets of
  size 1-3, controlled slice recall, and seeded noisy replay.
- RESULT:
  - clean: full ddmin exact 1.000 at 8.87 calls; sliced ddmin exact 1.000
    at 7.83 calls (11.8% saving);
  - 5% noise, 3 repeats: sliced exact 0.967, repair success 0.990, 14.2%
    call saving;
  - 10% noise, 5 repeats: sliced exact 0.967, repair success 0.993, 11.0%
    call saving;
  - 80% per-cause slice recall: safety fallback preserves exact 1.000 but call
    saving falls to 5.4%; fallback activates on 31.3% of cases.
- INTERPRETATION: accuracy and noise criteria pass, but the pre-registered cost
  criterion fails. ddmin is already efficient; slice verification and fallback
  consume much of the theoretical saving.
- STATUS: COST HYPOTHESIS KILLED; retain slicing for relevance/safety, not as
  the primary cost claim.

### E5: Can prior-first singleton verification reduce ddmin cost?

- HYPOTHESIS: Test the top two prior-ranked singleton causes before ddmin, then
  fall back to sliced ddmin for interactions.
- COMPARISON: full ddmin and sliced ddmin under the same generated cases.
- PRE-RUN PREDICTION: exact-set recovery remains >=0.99 clean and >=0.95 at
  5% noise; mean calls fall at least 20% below full ddmin.
- KILL CRITERION: either accuracy threshold fails or call saving remains below
  20%.
- CHEAPEST TEST: reuse E4 cases and oracle; change only the probe schedule.
- RESULT:
  - clean: exact 1.000, 18.4% call saving;
  - 5% noise: exact 0.967, 24.6% saving;
  - 10% noise: exact 0.967, 20.6% saving;
  - 80% slice recall: exact 1.000 through fallback, 16.2% saving.
- A sweep over singleton budgets 0-4 found `k=1` best in clean cases
  (19.0% saving) and `k=2` best under noise (20.6-24.6%); neither satisfies
  the clean 20% criterion robustly.
- STATUS: KILLED as a universal >=20% saving claim. Prior-first probing remains
  useful under noisy repeated replay, but is not the primary clean-case win.

### E6: What slice precision/recall is required for a real cost win?

- PURPOSE: sensitivity analysis, not a new confirmatory hypothesis.
- METHOD: sweep candidate-slice fraction and per-cause recall with the safety
  fallback enabled; use singleton budget k=1.
- DECISION RULE: retain slicing as a claimed cost lever only in regions with
  exact >=0.99, fallback <=0.15, and call saving >=0.20.
- RESULT (clean replay, k=1):
  - slice 20%, recall 100/95/80%: saving 38.9/36.8/27.3%, fallback
    0/5.5/27.0%;
  - slice 30%, recall 100/95/80%: saving 28.1/26.3/20.2%;
  - slice 40%, recall 100/95/80%: saving 20.0/18.9/15.6%;
  - slice 60% never exceeds 14.6% saving.
- DECISION: the cost claim is gated on an empirically audited slice covering
  <=30% of lineage edges with >=95% cause recall. Outside that region, use full
  ddmin or report no expected saving.
- STATUS: CONDITIONAL SUPPORT. Exactness comes from safety fallback; savings
  depend on slice quality.

### E7: How accurate is prefix bisection on real DGM task histories?

- HYPOTHESIS: Standard binary search identifies the first observed failing
  version on at least 90% of eligible DGM lineage/task episodes while using
  less than half the probes of forward linear scan.
- COMPARISON: exact forward scan over the same observed version sequence.
- PRE-RUN PREDICTION: exact >=0.90 and mean call saving >=0.40.
- KILL CRITERION: either threshold fails.
- NOTE: this targets the first visible bad edge, not the earliest latent cause.
- RESULT: 245 eligible episodes; exact first-bad localization 0.9918 overall
  and 0.8947 on the 19 non-monotone episodes. Mean calls were 1.39 for binary
  versus 1.51 for forward linear scan, only 8.1% saving.
- INTERPRETATION: accuracy passes but the cost criterion fails because released
  DGM paths are shallow and the first observed failure is usually close to the
  root. Asymptotic logarithmic savings do not materialize here.
- STATUS: COST HYPOTHESIS KILLED for current DGM-scale lineages. Enable
  probabilistic bisection only above a depth/cost threshold.

#### E3/E7 data audit correction

- The original parser omitted evaluator `error_ids` from each node's submitted
  task set. It could therefore construct task intersections and lineage
  episodes from incomplete submission records. The E3/E7 `245`, `226`,
  `92.24%`, `0.9918`, and `8.1%` figures are superseded and must not be cited.
- With `resolved | unresolved | emptypatch | error` IDs, plus prediction-file
  recovery when metadata counts are incomplete, the released tree contains 69
  deduplicated start-pass/end-fail episodes across 9 tasks and 22 leaves:
  56 monotone and 13 non-monotone.
- Across all 69 corrected episodes, linear scan is exact on 1.0000 at 1.4783
  mean probes; binary search is exact on 0.9710 at 1.7246 probes. On the 13
  non-monotone episodes, binary exactness falls to 0.8462.
- The E8 target subset contains 41 monotone delayed regressions across 6 tasks
  and 18 leaves. Linear scan is exact on 1.0000 at 1.0244 probes; binary search
  is exact on 1.0000 at 1.3659 probes. The corrected evidence strengthens the
  decision to disable bisection on shallow lineages.

### Iteration 2

#### Corrected evidence boundary

- The original DGM `4/11` disagreement claim is withdrawn. It compared raw
  accuracies from unequal staged task sets. Recomputing every sibling and
  descendant score on one common task set per fork, and treating tied maxima as
  a set-valued oracle, leaves only 1 strict greedy/oracle disagreement among 11
  forks.
- The controlled `llm-full=1.0` result is classified as a positive control.
  Case identifiers, error text, and debug evidence reveal the injected
  mechanism, and five samples from one prompt/data pair are not independent.
- Consequently, no current experiment establishes real-distribution LLM
  attribution accuracy. LLM output is retained only as a soft candidate prior.

#### Final candidate method: Causal Lineage Minimization

1. Persist immutable checkpoint manifests and content-addressed artifact
   snapshots for each harness mutation.
2. Rank historical patches using an optional external diagnoser plus explicit
   dependency metadata. Rankings never hard-prune candidates.
3. Verify the failure at the current artifact. If it does not reproduce,
   abstain.
4. Probe the top-ranked singleton first. If it is insufficient, run ddmin on a
   dependency slice only when `slice_fraction <= 0.30` and audited
   `cause_recall >= 0.95`; otherwise run full ddmin.
5. Verify the proposed repair against the full patch context. On failure,
   expand to the full lineage.
6. Return the one-minimal causal patch set, roll back to the parent of its
   earliest member, and replay later patches that do not depend on the cause
   set. Applying the plan requires explicit user confirmation.

#### Why this candidate survived

- It handles latent interactions that first-bad search cannot represent.
- Every diagnosis is certified by executable replay rather than prose.
- Safety fallback preserved exact recovery in the clean synthetic experiments.
- Its cost claim is explicit and auditable: the fast path is enabled only in
  the E6-supported operating region. Outside that region it chooses accuracy
  over a false savings claim.

#### Remaining kill test

- Run the plugin on real pi/SWE-bench harness failures with isolated artifacts.
- Required evidence: repair success no worse than full ddmin, lower mean replay
  cost in gate-eligible lineages, and successful replay of independent later
  gains.
- Failure of any criterion removes the corresponding headline claim; synthetic
  results alone are insufficient for release-quality performance claims.

### E8: DGM released-data comparison against score-only and no-rollback policies

- HYPOTHESIS: On monotone delayed-regression episodes from DGM's released SWE
  tree, CLM with a deepseek-v4-flash prior plus executable boundary
  verification achieves at least 0.90 exact rollback, higher repair success
  than rollback-1 and a score-only DGM ancestor-selection proxy, while using no
  more evaluator probes than a forward linear scan.
- MECHANISM: Semantic evidence prioritizes the defect-introducing macro-edge,
  while recorded per-task outcomes verify the proposed pass-to-fail boundary.
- COMPARISON:
  - `no-rollback`: retain the current failing state;
  - `rollback-1`: return to the immediately preceding scored state;
  - `dgm-score-proxy`: choose the highest aggregate-score prior state, using a
    common task set for every state in the episode;
  - `linear`: exact forward scan;
  - `clm-deepseek`: prior-first boundary checks with verified fallback.
- PRIMARY DATA: Every deduplicated monotone episode whose first observed bad
  state is at least two scored transitions before the failing endpoint.
- PREDICTION: exact rollback >=0.90; repair success exceeds both non-oracle
  baselines; mean evaluator calls <= linear.
- KILL CRITERION: exact rollback <0.90, no repair-success advantage over either
  baseline, or mean evaluator calls > linear.
- INTERPRETATION LIMIT: This evaluates failure recovery on logged trajectories,
  not counterfactual agent generation. It cannot establish that CLM's final
  SWE-bench score exceeds DGM's released fixed-D60 50%.
- STAGED EXECUTION RULE: First run a deterministic hash-selected 12-episode
  pilot with one DeepSeek call per episode. Expand to all episodes and three
  model repeats only if the pilot does not already meet a kill criterion. This
  amendment was recorded after a one-case API smoke test showed 95 s latency and
  20.8k output tokens per call, before inspecting the 12-case result.
- DATA AUDIT: The submitted-task parser was corrected before the confirmatory
  run to include evaluator `error_ids` and recover prediction IDs when metadata
  counts are incomplete. The DGM initial node then contains its canonical 60
  submitted tasks rather than an incomplete subset.
- ENDPOINT SANITY CHECK on that fixed D60 task set:
  - released DGM initial agent: 12/60 = 20.00%;
  - released full DGM best node: 30/60 = 50.00%;
  - no-open-ended ablation: 14/60 = 23.33%;
  - no-self-improve ablation: 23/60 = 38.33% (one missing canonical task
    counted as failure; raw release score 23/59 = 38.98%).
  These are single released runs, not confidence intervals. The DGM initial
  agent is not the current TypeScript Pi agent.
- CORRECTED FULL OFFLINE BASELINES on all 41 delayed-monotone episodes:
  `no-rollback=0`, `rollback-1=0`, and `dgm-score-proxy=0.1951` repair/exact;
  linear and binary both reach 1.0000, at 1.0244 and 1.3659 mean probes.
- PILOT SAMPLE: deterministic hash-selected 12 episodes, but only 4 unique
  tasks and 10 unique leaves. On this sample, `rollback-1=0`,
  `no-rollback=0`, `dgm-score-proxy=0.0833`, linear=1.0000 at 1.0833 probes,
  and binary=1.0000 at 1.4167 probes.
- SELECTION EFFECT: `no-rollback=0` follows from selecting current failures,
  and `rollback-1=0` follows from selecting delayed regressions whose immediately
  preceding scored state already fails. Those two numbers are construction
  checks, not empirical evidence of broad superiority.
- DEEPSEEK RESULT: CLM exact/repair=1.0000 at 1.5000 mean evaluator probes,
  with fallback on 3/12 episodes. The semantic prior's top-1 edge was correct
  on only 4/12 calls. For paths shorter than four edges, the 30% slice gate
  admitted no semantic candidate, so boundary verification, rather than the
  LLM, supplied the answer.
- TELEMETRY: 12 model calls, 52,754 reported input tokens, 181,072 reported
  output tokens, 767.291 summed seconds, and no retries. The gateway did not
  materially honor the requested 1,200-token cap, which further weakens the
  low-cost case.
- DECISION: **H8 KILLED on cost.** Accuracy and repair thresholds pass, and
  repair exceeds both non-oracle baselines, but 1.5000 probes is greater than
  linear's 1.0833 on the same sample. Per the staged rule, do not expand to
  three repeats or all episodes.
- CLAIM BOUNDARY: This supports only the statement that verified rollback can
  repair selected logged delayed failures better than no rollback,
  rollback-one, and a score-only ancestor proxy. It does not show that CLM
  exceeds DGM's fixed-D60 50% task-solving endpoint, and it provides no
  original-Pi comparison because no matching Pi predictions were released.
  It exercises CLM's monotone boundary fast path, not interaction ddmin,
  selective replay, or post-rollback agent generation. Edge/node IDs were
  aliased in the prompt, but memorization of public trajectory text cannot be
  ruled out.
- STATUS: REVISE. Retain executable verification and full-search fallback;
  remove DeepSeek ranking and shallow-lineage bisection from the default
  low-cost path unless a future gate predicts positive net savings.
