# Rollback MVP: offline diagnosis-guided rollback on DGM's SWE tree

First version validating factors A+B (failure attribution + rollback point
selection) from `EVOLUTION_ROLLBACK_DIRECTION.md` (section 4.2, usage C).

We replay DGM's released SWE evolution tree offline. No Docker, no re-running:
we read DGM's literal tree and per-task scores from
`../DGM_results/swe_results/swe_dgm`.

## What it does

At each sibling fork (a parent with >= 2 scored children), a decider picks the
child that is the best *premise* to keep evolving from. We compare:

- `greedy` -- pick highest own accuracy. DGM-style score-based parent selection.
- `random` -- uniform random (Ours-minus-A ablation, no attribution).
- `llm`    -- deepseek-v4-flash reasons over each child's intent/diff/own results
              and predicts the most promising subtree. Forward-looking.

Each choice is scored against the **subtree-best oracle** (the child whose real
downstream subtree reaches the highest accuracy). Metrics: hit rate and mean
regret (oracle subtree-best minus chosen subtree-best).

### Information isolation (core rule)

The decider sees only decision-time info (child id, mutation intent, patch, own
per-task pass/fail). It never sees downstream subtree results. The oracle uses
real downstream, for scoring only. This keeps the method free of survivorship
bias; the oracle's survivorship bias is a known, documented limitation.

## Setup

```bash
python3 -m pip install openai   # only needed for the llm decider
```

The decision LLM (deepseek-v4-flash) goes through the aicolate OpenAI-compatible
gateway (see `config.py`). Override with `ROLLBACK_LLM_API_KEY` /
`ROLLBACK_LLM_MODEL` if needed.

## Run

```bash
python3 run.py --offline            # baselines only, no API calls
python3 run.py                      # includes the deepseek decider (11 forks, 5 votes each)
python3 run.py --only-disagreement  # restrict to greedy != oracle forks
python3 run_controlled.py --offline # controlled baselines only
python3 run_controlled.py           # controlled full/no-debug, 5 votes each
python3 dgm_clm_benchmark.py --max-episodes 0 \
  --output outputs/dgm_clm_benchmark_offline.json
```

Results are written to `outputs/results.jsonl`.

## Historical experiment record

Both runs used deepseek-v4-flash, all 11 forks, and five votes per fork.

| Prompt | All-fork hit / regret | Disagreement hit / regret | Outcome |
|---|---|---|---|
| v1, short forward reasoning | 0.4545 / 0.0538 | 0/4 / 0.1363 | Did not beat greedy |
| v2, structured per-child analysis | 0.3636 / 0.0797 | 1/4 / 0.1533 | Historical; oracle invalid |

The v2 prediction was at least 1/4 disagreement hits and mean regret below the
greedy baseline (0.1353). It reached 1/4 but regret worsened to 0.1533. All 55
responses had complete structured fields; this was not a JSON or fallback
failure. The run took about 42 minutes, versus roughly 2 minutes for v1, so the
prompt also imposed a large latency cost.

These headline numbers are withdrawn as accuracy evidence. The original oracle
compared raw accuracy across unequal 10/60/200-task staged subsets, and plurality
ties were resolved by insertion order. After recomputing every fork on one
common task set and treating tied maxima as sets, only 1/11 forks is a strict
greedy/oracle disagreement. The archived LLM outputs remain useful for auditing
prompt behavior, not for a performance claim or formal hypothesis rejection.

Archived outputs:

- `outputs/results_deepseek_prompt_v1.jsonl`
- `outputs/results_deepseek_prompt_v2.jsonl`
- `outputs/run_deepseek_prompt_v1.log`
- `outputs/run_deepseek_prompt_v2.log`

### Controlled delayed-failure result

We added 12 controlled histories: 10 delayed latent defects plus two controls
where the latest edge is the true cause. The oracle is the version immediately
before the earliest edge that introduced the latent condition. Deepseek sees
the evolution history and current failure; `llm-full` additionally sees
low-level debug evidence.

| Decider | Vote-level exact / clears | Case plurality exact / clears |
|---|---|---|
| rollback-1 | 0.1667 / 0.1667 | 0.1667 / 0.1667 |
| highest-score | 0.1667 / 0.1667 | 0.1667 / 0.1667 |
| llm-no-debug | 0.9500 / 0.9500 | 0.9167 / 0.9167 |
| llm-full | 1.0000 / 1.0000 | 1.0000 / 1.0000 |

This is a positive control only. Case identifiers, error text, and debug
evidence reveal the injected mechanism, and five calls over the same prompt/data
are not independent samples. The result validates the experiment plumbing and
structured output path; it does not establish real-distribution attribution
accuracy.

Raw decisions: `outputs/results_controlled.jsonl`. Baseline-only decisions are
kept separately in `outputs/results_controlled_baselines.jsonl`; offline runs
cannot overwrite the full result.

### Corrected DGM CLM benchmark

`dgm_clm_benchmark.py` includes evaluator `error_ids` in submitted-task sets
and recovers prediction IDs when release metadata is incomplete. This correction
supersedes the earlier 245-episode monotonicity/bisection statistics.

The corrected release contains 69 deduplicated start-pass/end-fail episodes:
56 monotone and 13 non-monotone. Of these, 41 are monotone delayed regressions
across 6 tasks and 18 leaves.

Because the benchmark selects current failures and then delayed regressions,
`no rollback=0` and `rollback-1=0` follow from the cohort definition. They are
construction checks, not estimates of broad policy performance.

| Method | Full 41 exact / repair | Mean probes |
|---|---:|---:|
| no rollback | 0.0000 / 0.0000 | 0 |
| rollback-1 | 0.0000 / 0.0000 | 0 |
| score-only DGM proxy | 0.1951 / 0.1951 | 0 |
| linear boundary scan | 1.0000 / 1.0000 | 1.0244 |
| binary boundary search | 1.0000 / 1.0000 | 1.3659 |

The pre-registered DeepSeek pilot used a deterministic 12-episode sample
(4 unique tasks, 10 leaves):

| Method | Pilot exact / repair | Mean probes |
|---|---:|---:|
| rollback-1 | 0.0000 / 0.0000 | 0 |
| score-only DGM proxy | 0.0833 / 0.0833 | 0 |
| linear boundary scan | 1.0000 / 1.0000 | 1.0833 |
| CLM + DeepSeek prior | 1.0000 / 1.0000 | 1.5000 |

DeepSeek's top-ranked edge was correct on 4/12 calls; executable verification
and fallback produced the 12/12 repair result. The run used 12 calls and
reported 52,754 input tokens, 181,072 output tokens, and 767.291 summed seconds.
Because CLM used more probes than linear scan, the pre-registered low-cost
criterion failed and the three-repeat expansion was stopped.

This is an offline recovery benchmark, not an end-to-end task-solving
comparison. On a fixed canonical 60-task set, the released DGM initial agent is
12/60 and full DGM reaches 30/60. No matching original-Pi predictions are
available, so the result does not establish that CLM beats DGM or original Pi.
It tests CLM's monotone boundary fast path, not interaction ddmin, selective
patch replay, or counterfactual agent generation.

Artifacts:

- `outputs/dgm_clm_benchmark_offline.json`
- `outputs/dgm_clm_benchmark_deepseek.json`

### Repair-first CLM

The selected algorithm now minimizes a sufficient **removal set** directly:
first verify whether removing the highest-prior patch repairs the full lineage,
then run ddmin over removals when one patch is insufficient. This avoids paying
to reconstruct a complete failure-inducing family when one verified removal
already fixes the observed failure.

On balanced conjunctive, alternative, and mixed failure families:

| Setting | Repair-first repair / minimal | Calls | Saving vs previous CLM |
|---|---:|---:|---:|
| clean | 1.0000 / 1.0000 | 6.73 | 48.52% |
| 5% noise, 3 repeats | 0.9733 / 0.9700 | 20.46 | 46.45% |
| 10% noise, 5 repeats | 0.9700 / 0.9667 | 34.35 | 46.19% |
| 80% slice recall | 1.0000 / 1.0000 | 8.22 | 42.86% |
| no prior | 1.0000 / 1.0000 | 8.36 | 49.89% |
| misleading prior | 1.0000 / 1.0000 | 7.14 | 46.29% |
| DGM-like depth 3-6 | 1.0000 / 1.0000 | 4.54 | 43.29% |

All paired 95% bootstrap intervals for absolute call reduction exclude zero.
This passes the synthetic quality/cost criterion, including alternative causes
that require multiple removals. It is not evidence of a higher SWE-bench
endpoint; fresh same-model evolution runs remain required.

Two rejected alternatives are retained for audit:

- Direct branch quarantine saved 0% on full DGM under a conservative rule; an
  aggressive rule saved 86.28% but cut the best endpoint from 0.5000 to 0.2833.
- Stability-gated multi-fidelity promotion worked on the official split, but
  reached only 89.46% best-node recall and 6.58% savings across 5,000 hash task
  rotations.

Artifacts:

- `outputs/repair_first_results.json`
- `outputs/dgm_budgeted_quarantine.json`
- `outputs/dgm_multifidelity_race.json`

## Files

- `config.py`   -- paths and LLM gateway settings
- `evo_tree.py` -- parse DGM tree; subset-intersection comparison; subtree-best
- `scenarios.py`-- build fork decision points; compute oracle labels
- `deciders.py` -- greedy / random / llm deciders (llm prompt lives here)
- `llm_client.py` -- LLM call + JSON parsing
- `scorer.py`   -- hit rate + regret against the oracle
- `run.py`      -- orchestration and comparison report
- `controlled_cases.json` -- controlled histories and hidden oracle labels
- `controlled_experiment.py` -- controlled prompt, deciders, and scoring
- `run_controlled.py` -- full/no-debug controlled experiment runner
- `dgm_clm_benchmark.py` -- corrected endpoint, recovery-policy, and CLM pilot
  benchmark
- `dgm_budgeted_quarantine.py` -- chronological branch-pruning kill test
- `dgm_multifidelity_race.py` -- 10/60/200 promotion sensitivity benchmark
- `run_repair_first.py` -- repair-first interaction/noise/prior benchmark

## Known limits (see EVOLUTION_ROLLBACK_DIRECTION.md 4.2)

- Nodes are DGM's coding-agent code, not pi harness: this validates the rollback
  decider, not a pi harness loop.
- Tree is shallow (83 nodes, 53 leaves); after common-subset correction only
  1/11 forks is a strict disagreement case.
- Factor C (re-evolution after rollback) is not testable offline; it needs real
  runs (Docker), deferred to the main-result stage.
