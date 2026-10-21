# Pre-Registration: DGM 200-Task Pi and RF-CLM Evaluation

Date frozen: 2026-09-25

## Research Question

Measure quality, model-token use, evaluator cost, and wall time for fixed
original Pi and the current RF-CLM recovery workflow on the exact 200
SWE-bench Verified tasks used by DGM.

The released DGM result is a historical reference, not a causal same-model
baseline. DGM used a different coding agent, model, search budget, and
multi-week evolution process.

## Frozen Data

- DGM source commit:
  `682eb38a3eb232f4396924cacd0a083bf1444cf8`
- DGM partitions: disjoint `small=10`, `medium=50`, `big=140`
- SWE-bench Verified revision:
  `c104f840cc67f8b6eec6f759ebc8b2693d585d4a`
- Execution order: source Verified row order filtered by DGM membership
- Ordered ID hash:
  `421c950302366954005dab020cdc89ca0d6ae1f0423e2b662637f7790a31d0d7`
- Frozen manifest:
  `dgm_swebench_verified_200.v1.json`
- Manifest hash:
  `3fb913fbc73a05c1f7cae3b708c976374632820b58377aab5de08b742f96c967`

The manifest contains the complete 13-field official rows. Agent workspaces
receive only `instance_id`, `repo`, `base_commit`, and `problem_statement`.
Gold patches, test patches, and official evaluator outcomes are never mounted
into an agent workspace.

## Protocols

### P1: Original Pi one-shot

- Package: `@earendil-works/pi-coding-agent@0.85.1`
- Model: `byteplus/deepseek-v4-flash-ga`
- One isolated Pi session per task
- Maximum 512,000 reported tokens and 3,600 seconds per task
- Exact base commit, no remote, no future Git refs
- File tools confined to the task workspace
- Shell commands run in the task image with `--network none`
- Tests and other excluded paths cannot enter the submitted patch
- No official evaluator result is returned to Pi

This is the primary standard SWE-bench arm and the only local arm placed in a
direct accuracy table beside DGM's published 200-task score.

### P2: Pi + RF-CLM, one evaluator-feedback recovery

P2 starts from P1. Only unresolved P1 tasks are eligible for one bounded
causal-slice repair call. The repair receives the task statement, rejected
patch, official failure evidence, and source files already selected by the P1
patch. The final combined patch is graded once under a content-addressed run
ID.

P2 is explicitly labeled **feedback-assisted recovery**. It is an operational
upper bound and is not a standard one-submission SWE-bench score. It must not
be presented as directly equivalent to DGM's reported 50%.

No second repair, manual edit, task-specific prompt, or post-hoc task exclusion
is allowed.

## Hypotheses

### H12: Fixed original-Pi endpoint

**Prediction.** P1 resolves 40%-60% of the 200 tasks. This range is based on
the prior 5/10 DGM-small pilot and is not a power-derived claim.

**Kill criterion.** Reject any conclusion about P1 if hidden evaluator
information, future Git history, external files, or network access reaches the
agent. Infrastructure/provider failures remain failures in the
intention-to-evaluate primary score; a separately labeled per-protocol
sensitivity analysis may exclude only failures proven unrelated to the patch.

### H13: RF-CLM recovery gain

**Prediction.** P2 improves absolute solve rate by 5-20 percentage points over
P1 with no more than 20% additional reported model tokens.

**Kill criterion.** The endpoint gain claim is rejected if the paired
task-level 95% bootstrap interval for `P2 - P1` includes zero. The low-cost
claim is rejected if recovery adds more than 20% reported model tokens, or if
it does not reduce cost relative to a quality-matched full Pi retry.

The quality-matched retry comparison is required before claiming that RF-CLM
is cheaper than retrying Pi. If no retry arm is run, only recovery overhead is
reported.

## Metrics

### Primary quality

- Resolved tasks and solve rate over all 200 frozen tasks
- Wilson 95% interval for each solve rate
- Paired task difference `P2 - P1`
- Paired bootstrap 95% interval, 10,000 resamples, seed `20260925`
- Exact McNemar/binomial test over discordant task outcomes

Because P2 is a recovery protocol, it should not make a resolved P1 task fail.
Any such regression is treated as a pipeline defect and reported.

### Cost and time

- Input, output, cache-read, cache-write, and total reported tokens
- Token mean, median, interquartile range, and p95 per task
- Agent summed duration and experiment elapsed wall time
- Evaluator summed runtime and build/runtime errors
- Tool calls, retries, timeouts, budget aborts, empty patches
- Recovery attempts, successes, success rate, and incremental overhead
- Estimated API cost only when externally verified per-token prices are
  supplied; the current model catalog's zero prices are not treated as free
  usage

### Historical DGM reference

- Initial agent: 20% on the paper's 60-task development evaluation
- Best released 200-task node: `100/200 = 50%`
- Evolution duration: approximately two weeks
- Reported total evolution cost: approximately `$22,000`
- Reported baseline cost: approximately `$10,000`
- Reported 60-task Claude evaluation: approximately `$350`
- DGM input/output token counts: not reported

Missing DGM token or single-200-evaluation cost values remain `not reported`;
they are not inferred from dollar totals.

## Execution and Stopping

- Tasks run in the frozen Verified order.
- Concurrency defaults to one.
- State is written atomically after every phase and is resumable.
- Evaluator run IDs hash the protocol, manifest, model, instance, and patch.
- A global reported-token cap and elapsed-time cap are checked between tasks.
- Paid execution requires an explicit command-line confirmation value.
- The cheapest killing test is a no-model validation followed by one
  infrastructure-only task. Full 200-task model execution starts only after
  the projected token/time budget is reviewed and approved.

## Scope Limits

This run has 200 paired tasks but only one stochastic generation pass per
system. Task-level intervals do not estimate model-run variance. A
publication-level stochastic superiority claim requires at least three
independent generation seeds or repeats under the same protocol and budget.

The experiment evaluates fixed Pi plus a feedback recovery workflow. It does
not reproduce DGM's open-ended self-evolution search and cannot attribute any
difference to RF-CLM versus DGM's evolutionary mechanism.

## Post-Start Operational Amendments

At task 5 (`astropy__astropy-13453`), the gateway rejected the initial model
request with `RATE_LIMIT_TPM_EXCEEDED` before returning any usage or patch.
This attempt was quarantined under `dgm200_run/invalid_attempts/` and is
excluded from all metrics. It will be rerun from the frozen input without
receiving evaluator feedback from the invalid attempt.

Starting with that rerun, a fixed 90-second delay is inserted between tasks to
keep sequential requests below the externally imposed 1,000,000 TPM limit.
This changes only request pacing, not prompts, model settings, task order,
per-task budgets, grading, or either protocol's information access.

The task-5 rerun later reached the same TPM limit after producing 487,145
reported tokens and a valid patch. That patch passed the official evaluator,
so the attempt remains in the primary results. Starting after task 5, the
stateless SSE adapter also retries only upstream HTTP 429 responses, at most
three times with at least 65 seconds between attempts. The retried request body
is identical. Proxy hashes and the exact applicability boundary are recorded
in `dgm200_run/runtime_amendments.json`.

Task 6 then encountered two pre-generation image-build failures caused by
15-second PyPI read/TLS timeouts. Starting with the task-6 retry, Docker builds
set build-only `PIP_DEFAULT_TIMEOUT=120` and `PIP_RETRIES=20` arguments. This
changes network failure tolerance only; dependency specifications, source
commits, image platforms, and runtime environments remain unchanged. The
builder hashes and applicability boundary are recorded in the same amendment
file.

The first resumed pass encountered another PyPI index failure on task 7 and
then stopped after task 8 because the repair model returned an `old` string
that occurred three times. Task 8's P1 result is valid. Its sole P2 call is
retained as a failed repair attempt; it is not retried. The pre-amendment
repair runner raised before persisting that response's usage, so exact token
telemetry for this one call is unavailable. A conservative 512,000-token
charge is applied to the global cap, while reported-token distributions mark
the sample missing rather than imputing fabricated input/output counts.

Starting after this incident, repair telemetry is persisted before edit
application, and exact-edit validation failures are terminal P2 failures
rather than infrastructure errors. This changes failure accounting and
resumability only; it does not change prompts, model calls, eligibility,
official grading, or the one-repair limit. Official evaluator failures remain
infrastructure errors. Exact hashes and the task-level accounting record are
in `dgm200_run/runtime_amendments.json`.

Task 12 then reproduced the same transient PyPI index failure while resolving
unchanged Astropy build dependencies. Its no-model attempt was discarded.
Starting with the task-12 retry, those exact PyPI wheels are read from a local,
SHA-256-manifested wheelhouse with `PIP_NO_INDEX=1`. The same wheelhouse remains
available to the official evaluator because it repeats the editable install
inside the task container. It contains only public third-party build
dependencies, no task source, patches, tests, or evaluator outcomes. The
builder also retries image-only failures twice. Completed-task skips no longer
incur the 90-second model pacing delay, and the wall-time cap is measured from
the original run start across resumptions. None of these changes affects model
inputs, dependency versions, task source, or evaluator commands. The wheel
hashes and image verification are recorded in
`dgm200_run/runtime_amendments.json`.
