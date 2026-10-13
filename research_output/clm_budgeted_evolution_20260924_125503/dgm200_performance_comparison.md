# DGM-200 Performance Comparison and Time Audit

Date: 2026-10-13

## Executive Summary

The earlier "about two weeks" description is a calendar-span observation, not
the benchmark's execution time. The DGM-200 run spanned 18.23 calendar days,
but 16.99 days are explicitly recorded as paused: user pauses, host/Docker
recovery, offline dependency repair, credential restoration, and wall-clock
cap approval. The protocol-recorded active wall time is **29.89 hours**.

The directly instrumented execution time is smaller:

- Original Pi: **8.75 hours** of agent plus official-evaluator time.
- Feedback-assisted RF-CLM increment: **4.82 hours** of repair, recovery
  evaluation, and feedback-probe evaluation time.
- Combined direct execution: **13.57 hours**.

The remaining active time is accounted for by successful evaluator-image
builds (4.58 hours), deliberate inter-task pacing, orchestration, and failed
or retried pre-model builds. It must not be interpreted as continuous model
execution.

On the fixed 200-task manifest, original Pi solved 100 tasks (50.0%) and
feedback-assisted RF-CLM solved 139 (69.5%), a paired improvement of 39 tasks
or 19.5 percentage points. The feedback arm used one round of hidden official
evaluator feedback and is therefore a recovery upper bound, not a standard
one-submission SWE-bench result.

## Scope and Comparison Rules

The P1 and P2 rows use the same frozen 200-task DGM-200 manifest. Their
accuracy, reported-token, and instrumented-time fields are directly
comparable.

The original DGM paper is a historical reference only. Its 50% headline,
approximately two-week evolution duration, and approximately USD 22,000
evolution cost are paper-reported values. The paper does not report token
counts. A local release audit finds that 30/60 = 50% is the directly
release-verifiable endpoint; the public runner loads but does not execute its
final 140-task stage. Consequently, this report does not present DGM's
100/200 headline as a reproduced local result.

## Three-Metric Comparison

| System | Task completion accuracy | Reported tokens | Time metric |
|---|---:|---:|---:|
| P1: original Pi one-shot | 100/200 = **50.0%** | **70.725M** | **8.75 h** direct agent + official evaluator |
| P2: Pi + feedback-assisted RF-CLM | 139/200 = **69.5%** | **76.639M** total; +5.803M (+8.19%) versus P1 | **13.57 h** cumulative P1 + P2 direct execution; P2 increment **4.82 h** |
| Original DGM paper headline | 100/200 = 50% reported | Not reported | Approximately two weeks of evolution reported |
| Original DGM release audit | 30/60 = 50% directly verifiable | Not reported | Not separately reported |

For budget enforcement, two completed model calls lacked token telemetry.
Applying the pre-registered conservative charge yields **77.663M**
budget-counted tokens. The 76.639M value is the sum of telemetry actually
reported by the provider, including cache-read tokens; neither figure is a
verified API billing total.

### Relative View of the Comparable Arms

```text
Accuracy (200 frozen tasks)
P1  50.0% | ####################
P2  69.5% | ############################

Reported tokens
P1  70.725M | #####################################
P2  76.639M | ########################################

Direct execution time
P1   8.75 h | ##########################
P2  13.57 h | ########################################
```

P2's extra 4.82 direct-execution hours and 5.803M reported tokens produced 39
additional solved tasks. That is approximately 7.4 additional direct-execution
minutes and 0.149M incremental reported tokens per additional solved task.
This is a descriptive marginal calculation, not a claim that P2's feedback
protocol is comparable to a one-shot benchmark submission.

## Time Audit

### Calendar Span Versus Active Time

| Quantity | Seconds | Hours | Days |
|---|---:|---:|---:|
| First start to final completion, raw calendar span | 1,574,798.832 | 437.444 | 18.227 |
| Explicitly excluded paused intervals | 1,468,126.210 | 407.813 | 16.992 |
| Raw span less explicit pauses | 106,672.622 | 29.631 | 1.235 |
| Protocol-recorded active wall time | 107,588.622 | **29.886** | **1.245** |

The 916-second difference between "raw span less explicit pauses" and the
protocol wall-clock counter is retained rather than discarded. It represents
direct evaluator-image verification around pause boundaries and avoids
retroactively classifying completed work as idle time.

### Active-Time Attribution

| Component | Seconds | Hours | Meaning |
|---|---:|---:|---|
| P1 agent execution | 25,664.589 | 7.129 | 200 original Pi attempts |
| P1 official evaluator | 5,828.599 | 1.619 | 150 official evaluation runs |
| P2 repair execution | 13,343.128 | 3.706 | 87 telemetry-bearing repair calls |
| P2 recovery evaluator | 2,313.483 | 0.643 | 57 recovery evaluations |
| P2 feedback-probe evaluator | 1,701.259 | 0.473 | 39 feedback-probe evaluations |
| All direct execution above | **48,851.058** | **13.570** | Agent and official evaluator runtime |
| Successful image builds | 16,503.061 | 4.584 | 195 completed builds |
| Other active overhead | 42,234.503 | 11.732 | Pacing, orchestration, failed/retried pre-model builds |
| Protocol active wall total | **107,588.622** | **29.886** | Sum of active categories |

This establishes that a normal uninterrupted execution should be described as
roughly **30 active wall-clock hours** under this protocol, not two weeks.
The two-week DGM number is also not a matched time baseline: it describes an
open-ended multi-iteration evolution process with a different model and agent
substrate.

## Accuracy Detail

The paired comparison is stronger than a comparison of independent rates:

| Statistic | Value |
|---|---:|
| P1 solved | 100/200 = 50.0% |
| P2 solved | 139/200 = 69.5% |
| Paired gain | +39 tasks; +19.5 percentage points |
| Paired bootstrap 95% interval | [+14.0, +25.0] percentage points |
| P2-only solves | 39 |
| P1-only solves | 0 |

Stage-level results are 5/10 to 7/10 on the small stage, 23/50 to 30/50 on
the medium stage, and 72/140 to 102/140 on the big stage. These values should
be read as an effect of evaluator-feedback-assisted recovery, not as evidence
that P2 beats a standard DGM evolution run.

## Token Detail

| Token accounting field | P1 | P2 incremental | P2 cumulative |
|---|---:|---:|---:|
| Input tokens | 6.829M | 3.415M | 10.244M |
| Output tokens | 2.866M | 2.388M | 5.254M |
| Cache-read tokens | 61.031M | 0 | 61.031M |
| Total reported tokens | **70.725M** | **5.803M** | **76.639M** |
| Missing-telemetry conservative charge | 0.512M | 0.512M | 1.024M |

The P1 and P2 telemetry each have one completed attempt without provider token
telemetry. The stated budget count treats each as 512,000 tokens. No token
equivalent is available for original DGM, so a three-way token efficiency
ranking cannot be made.

## Repository Archive Policy

The committed benchmark record should contain:

- the frozen task manifest and task ordering;
- run configuration, pause accounting, runtime amendments, and final summary;
- the benchmark exploration log and this comparison report;
- the existing tracked per-task state needed to close the final task record;
- the benchmark wrapper and small configuration files that define the protocol.

The following are intentionally ignored going forward because they are
reproducible from the retained configuration and summary, or are local
machine-specific build artifacts:

- evaluator and image-build logs;
- per-call generated prediction/evaluation JSON files;
- raw task workspaces and future per-task generated output directories;
- invalid-attempt artifacts and direct image-verification directories;
- wheelhouses and runtime authentication state.

No existing local artifact is deleted by this policy.

## Evidence

- [Final benchmark summary](dgm200_run/summary.json)
- [Run state and pause accounting](dgm200_run/run_state.json)
- [Runtime amendments](dgm200_run/runtime_amendments.json)
- [Frozen DGM-200 manifest](dgm_swebench_verified_200.v1.json)
- [Experiment exploration log](exploration_log.md)
- [Local DGM release audit](report.md)
- [DGM paper](https://arxiv.org/html/2505.22954v2)
