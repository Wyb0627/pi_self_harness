# Exploration Log: Budgeted Causal Lineage Evolution

Date: 2026-09-24

This log is append-only for hypotheses, experiments, outcomes, and audit
corrections. A method is not accepted because it improves one proxy metric; it
must satisfy the pre-registered joint quality and cost criteria.

## Inherited Evidence

- E8 tested CLM's monotone boundary fast path on 12 hash-selected released-DGM
  recovery episodes. Repair/exact was 1.0000, but mean evaluator probes were
  1.5000 versus linear scan's 1.0833. DeepSeek top-1 was 4/12. The low-cost
  hypothesis was killed.
- The released DGM tree supports logged failure replay and fixed-D60 endpoint
  accounting. It does not contain the counterfactual children that another
  parent/mutation policy would have generated.
- The DGM initial agent is not the current TypeScript Pi agent, and no matching
  original-Pi predictions are present in the release.

## Main Evaluation Contract

- Same frozen task IDs and held-out split for every method.
- Same foundation model, model parameters, tool permissions, timeout, and
  maximum proposal/evaluation budget.
- Baselines: original Pi, reproduced DGM-style evolution, and CLM evolution.
- Primary metrics: held-out solve rate and normalized success-budget AUC.
- Cost metrics: generated nodes, task evaluations, model input/output tokens,
  wall time, and estimated API cost.
- A result "beats" a baseline only if its held-out score is higher at an equal
  budget, or equal within a predeclared equivalence margin while total cost is
  lower. Logged-tree proxy results cannot satisfy this endpoint claim.

## H9: Risk-Adjusted Successive Halving with Branch Quarantine

- HYPOTHESIS: Combining executable rollback evidence with confidence-bound
  staged promotion can reduce total evaluated-node cost while preserving or
  improving the best held-out agent found under a fixed budget.
- MECHANISM:
  1. evaluate every new child on a small common task panel;
  2. promote only candidates whose lower confidence bound is competitive;
  3. when paired regressions reproduce, assign lineage hazard to the verified
     causal patch set and quarantine only dependent descendants;
  4. replay independent later gains on the rollback checkpoint;
  5. reserve a fixed exploration floor so misleading early panels cannot
     permanently eliminate novel branches.
- COMPARISON: DGM score-plus-child-count parent sampling, latest-parent
  evolution, original Pi without evolution, and CLM without quarantine.
- PRIMARY PREDICTION: On a same-model held-out pilot, H9 has higher
  success-budget AUC than both Pi and DGM-style search, while reaching at least
  their final solve rate with at least 20% fewer task evaluations.
- KILL CRITERION: Kill or revise H9 if any of the following occurs:
  - held-out solve rate is below either baseline at the matched budget;
  - normalized success-budget AUC is not higher than both baselines;
  - task-evaluation saving versus the best-quality baseline is below 20%;
  - quarantine removes a branch that later contains the best held-out node in
    more than 5% of replayable trials;
  - rollback/replay fails to preserve an independent later gain.
- CHEAPEST TEST: chronological logged-candidate replay over the released DGM
  tree, explicitly labeled as a proposal-pool benchmark rather than an
  end-to-end policy estimate.
- ESCALATION RULE: Only after the logged-candidate test passes, run a 3-task
  Docker smoke test; only after that passes, run the frozen 10-task DGM small
  subset with at least three independent evolution seeds.
- RESULT:
  - Full DGM baseline: fixed-D60 best 0.5000, cost 3622 task-equivalents,
    normalized quality-cost AUC 0.3948.
  - `confirmed-no-new-gain`: preserved 0.5000 but saved 0.00% and changed AUC
    by 0.0000. It quarantined five nodes, all leaves, so it prevented no future
    work.
  - `net-loss-2`: saved 86.28% but reduced the best endpoint to 0.2833 and AUC
    by 0.1158. It pruned a stepping stone on the path to the 0.5000 agent.
  - No-open-ended: the primary rule again saved 0.00%; the aggressive rule
    reduced the endpoint from 0.2333 to 0.2000.
  - No-self-improve: the primary rule preserved 0.3833 and saved 46.89%, but a
    method must satisfy the criterion across all three released runs.
- INTERPRETATION: Direct child regressions are not a useful global quarantine
  signal. Conservative rules fire only after a branch is already dead;
  aggressive rules destroy the stepping-stone behavior that DGM was designed
  to preserve. The correct use of rollback evidence is local repair-plan
  construction and budget allocation, not permanent subtree deletion from one
  negative edge.
- STATUS: **KILLED.** The primary rule passes 1/3 released runs and fails the
  pre-registered 20% saving criterion on the full DGM run. Do not escalate H9
  to Docker.

## H10: Multi-Fidelity Repair-Plan Racing

- HYPOTHESIS: Treat complete rollback-and-selective-replay plans as arms and
  allocate task evaluations with paired confidence-bound successive halving.
  This can preserve the best plan while spending at least 20% fewer task
  evaluations than DGM's fixed 10->60->200 promotion schedule.
- MECHANISM: CLM/GCJR generates executable repair plans; low-fidelity paired
  tasks estimate each plan's gain over its parent; only statistically
  competitive plans receive larger task panels. A misleading semantic prior
  may change initial allocation but cannot eliminate an arm without evaluator
  evidence.
- COMPARISON: uniform full evaluation, DGM 10->60->200 thresholding, and
  prior-free successive halving.
- CHEAPEST TEST: use the eight released DGM candidates with 197-200 recorded
  task outcomes as a fully observed promotion benchmark. This tests allocation,
  not counterfactual generation or rollback quality.
- KILL CRITERION: across deterministic task-order rotations, select the
  released 0.5000 best node in at least 95% of trials and reduce mean task
  evaluations by at least 20% versus reproduced DGM staging. Any use of full
  outcomes to construct the low-fidelity order invalidates the test.
- RESULT:
  - Candidate set: the eight released nodes with 197-200 recorded outcomes;
    missing/error outcomes count as failures.
  - On the official 10/50/140 panel split, the stability gate retains the
    0.5000 best node and spends 520 task evaluations versus 660 for documented
    DGM threshold-plus-top-2 staging, a 21.21% saving.
  - Across 5,000 SHA-256 task-order rotations, documented DGM staging contains
    the global-best node in 84.52% of trials at 599.6 mean task evaluations.
    The stability gate reaches 89.46% at 560.2 evaluations, a 6.58% saving.
  - Uniform full evaluation is exact at 1,600 evaluations. Fixed top-5/top-2
    reaches 89.94% at 610; top-1-after-60 reaches 85.54% at 520.
- INTERPRETATION: H10 improves both accuracy and cost over the reproduced DGM
  schedule in the rotation sensitivity analysis, but misses the required 95%
  best-arm recall and 20% saving. Its official-split success is not robust to
  panel composition. The eight candidates are also selected survivors rather
  than independent plans, so this cannot support an endpoint claim.
- STATUS: **KILLED.** Do not promote a single full-evaluation candidate merely
  because the leader is stable between 30 and 60 tasks.

## H11: Cost-Aware Probe-or-Commit CLM

- HYPOTHESIS: A controller that explicitly compares the expected reduction in
  post-rollback recovery cost against the next probe cost can default to direct
  commit or linear verification on shallow lineages, while reserving
  graph-constrained replay for sparse interactions. It will match full CLM
  repair success within a 2-point non-inferiority margin and reduce total
  diagnosis-plus-recovery cost by at least 20%.
- MECHANISM:
  - direct commit when a verified singleton repair has high confidence;
  - linear first-bad on shallow monotone lineages;
  - graph-constrained singleton/pair replay for interaction evidence;
  - stop probing when expected continuation-cost reduction is no larger than
    probe cost;
  - never permanently quarantine a branch from a single regression.
- COMPARISON: current CLM, linear scan, full ddmin, DGM-style reselection, and
  the H9/H10 methods rejected above.
- CHEAPEST TEST: synthetic stochastic lineages with heterogeneous probe cost
  and explicit post-rollback descendant cost, followed by released-DGM
  recovery episodes. End-to-end claims still require fresh Pi evolution runs.
- KILL CRITERION: repair success falls by more than 0.02 versus full CLM, or
  the paired 95% confidence interval for total-cost reduction includes zero.
- IMPLEMENTATION CHANGE: Reframe the diagnostic target from the complete
  failure-inducing patch family to a **one-minimal sufficient removal set**.
  The evaluator now tests `full_lineage - proposed_removals` directly. A
  high-prior singleton is committed only after that removal repairs the full
  failure. Otherwise ddmin minimizes the removal set, with the same
  slice-recall gate and full-lineage fallback.
- WHY THIS IS NOT A METRIC TRICK: For a conjunctive failure `p1 AND p3`,
  proving both patches form the complete failure core is unnecessary for
  rollback. Removing either one is a cardinality-one sufficient repair and
  preserves more later work. For alternative independent failures
  `p1 OR p3`, singleton removal fails verification and repair-ddmin correctly
  returns both removals.
- SYNTHETIC RESULT over 300 cases per setting, lineage lengths 8/16/32:
  - clean: repair-first repair/minimal=1.000/1.000 at 2.39 probes versus
    active failure-set CLM repair=1.000 at 7.19 probes, a 66.8% reduction;
  - 5% noise with three repeats: 0.997/0.997 at 7.17 probes versus
    0.990 at 18.68, a 61.6% reduction;
  - 10% noise with five repeats: 1.000/0.993 at 11.82 probes versus
    0.993 at 32.97, a 64.1% reduction;
  - 80% slice recall: 1.000/1.000 at 2.68 probes versus 1.000 at 6.97,
    a 61.5% reduction; verified fallback activates on 12.7%.
- PLUGIN RESULT: `pi-rollback` now implements removal-first singleton
  verification and `sliced/full-repair-ddmin`. Its AND and OR interaction
  tests, artifact safety tests, and replay tests all pass (13/13).
- LIMIT: The current synthetic generator contains one conjunctive cause family
  per case. The TypeScript OR test verifies the algorithmic branch, but a
  larger stochastic alternative-family benchmark is still required.
- STATUS: **SUPPORTED on synthetic repair cost; not yet an end-to-end DGM/Pi
  win.** This is the first method in the search that clears the 20% cost bar
  without sacrificing repair success.

### H11 follow-up: alternative and mixed repair families

- DATA: 300 cases per setting over lineage lengths 8/16/32, balanced among:
  one three-edge conjunctive failure, three alternative singleton failures,
  and a mixed pair-plus-singleton family. Four settings cover clean replay,
  5% noise with three repeats, 10% noise with five repeats, and 80% candidate
  slice recall.
- COMPARISON: the previous plugin's failure-core-first repair sequence versus
  full removal-ddmin and repair-first CLM. The primary target is sufficient,
  one-minimal, minimum-cardinality removal, not complete failure-family
  enumeration.
- RESULT:
  - clean: repair-first repair/minimal/optimal = 1.000/1.000/1.000 at
    6.73 probes, versus failure-first 1.000 at 13.07; saving 48.52%;
  - 5% noise: 0.9733/0.9700/0.9700 at 20.46 versus failure-first repair
    0.9833 at 38.21; repair delta -0.0100, saving 46.45%;
  - 10% noise: 0.9700/0.9667/0.9667 at 34.35 versus failure-first repair
    0.9767 at 63.83; repair delta -0.0067, saving 46.19%;
  - 80% slice recall: 1.000/1.000/1.000 at 8.22 versus 1.000 at 14.39;
    saving 42.86%.
- UNCERTAINTY: paired bootstrap 95% intervals for absolute call reduction are
  strictly positive in every setting: clean [5.58, 7.03], noise-05
  [15.81, 19.90], noise-10 [26.25, 32.95], slice-recall-80 [5.22, 7.18].
- PRIOR SENSITIVITY: with an uninformative prior, repair-first remains
  1.000 repair/minimal/optimal and saves 49.89% calls; with a deliberately
  misleading prior it remains 1.000/1.000/1.000 and saves 46.29%. Executable
  verification prevents the prior from changing correctness.
- DGM-DEPTH SENSITIVITY: on lengths 3/4/5/6, matching the released tree's
  shallow regime, repair-first remains 1.000 repair/minimal/optimal and uses
  4.54 probes versus failure-first's 8.01, saving 43.29% with paired call
  reduction CI [3.26, 3.67].
- DECISION: **H11 PASSES the synthetic pre-registration in all 7/7 settings.**
  Repair-first CLM becomes the selected algorithmic core. The endpoint claim
  remains unproven until fresh same-model Pi/DGM-style evolution runs exist.

## E12: Integration Verification and Endpoint Gate

- PLUGIN VERIFICATION:
  - `npm test` in `pi-rollback`: 15/15 passed;
  - `npm run check` in `pi-rollback`: Biome and TypeScript passed;
  - the final-plan test confirms that diagnosis abstains when dependency-safe
    replay skips additional patches and thereby exposes another failure.
- EXPERIMENT VERIFICATION:
  - `python3 -m unittest discover -s rollback_mvp -p 'test_*.py' -v`:
    27/27 passed;
  - `state.json`, `memo.json`, `sources.json`, and
    `outputs/repair_first_results.json` parse as valid JSON.
- ROOT VERIFICATION:
  - Biome, pinned/runtime dependency checks, import boundaries, entry graphs,
    shrinkwrap, and install-lock checks pass;
  - `tsgo --noEmit` fails on untouched model-catalog code because manifests are
    inferred as `unknown` and model IDs as `never`; browser-smoke is not reached.
- ENDPOINT PROTOCOL:
  - compare frozen original Pi, matched DGM-style Pi, and RF-CLM Pi on one Pi
    substrate with the same DeepSeek revision and hard budgets;
  - use the official 10-task small panel for evolution, the next 50 for
    promotion/fixed-D60 reporting, and keep the remaining 140 hidden until one
    final evaluation;
  - run a 3-task smoke test before the 10-proposal pilot, then at least three
    seeds for a confirmatory claim.
- BLOCKER:
  - the local Docker VM was stopped during an attempted resize from 2 CPU /
    about 2 GiB to the SWE-bench recommendation of 8 CPU / 16 GB / 120 GB;
  - the sandbox cannot write `~/.colima`, so it cannot restart the VM;
  - host-side recovery requires
    `colima start --cpu 8 --memory 16 --disk 120`.
- STATUS: **ALGORITHM COMPLETE; ENDPOINT EXPERIMENT BLOCKED.** Do not claim a
  DGM/Pi win until the fresh matched runs complete.

## E13: Docker Recovery and Endpoint Smoke

- ENVIRONMENT:
  - Colima reports 8 CPUs and 16 GiB memory.
  - The 120 GiB data disk is mounted at `/var/lib/docker`; the 20 GiB root
    filesystem is not the Docker image store.
  - The shell's default Docker socket was stale, so all benchmark commands use
    `DOCKER_HOST=unix:///Users/bytedance/.colima/default/docker.sock`.
- SWE-BENCH SMOKE:
  - official source revision: `dc4c087c2b9e4cefebf2e3d201d27e362d899e0f`;
  - tasks: the first three DGM-small IDs;
  - deliberately non-solving patch: add one inert text file;
  - result: 3/3 patches applied, 3/3 evaluations completed, 0 evaluator errors,
    0 residual containers, and 0/3 resolved as expected;
  - ARM64 base and Django environment images are now cached.
- PI SUBSTRATE:
  - repository source execution is blocked by missing generated provider JSON
    files, consistent with the root model-catalog type failures;
  - fixed published `@earendil-works/pi-coding-agent@0.85.1` is used instead;
  - DeepSeek's endpoint buffers streaming responses. A local stateless adapter
    converts the buffered Chat Completions result to standard SSE without
    changing prompts, tool calls, tokens, or model parameters.
- INVALIDATED PILOT:
  - the first checkout retained `origin/main`; on task
    `django__django-12754`, Pi searched future Git history and found the later
    fixing commit;
  - every result from those worktrees is quarantined under
    `endpoint_runs/invalid-future-history/` and excluded from all metrics;
  - reruns use per-task depth-1 fetches of only the base commit, with no
    configured remote or future refs.
- STATUS: infrastructure smoke passed; leak-free Pi task generation is next.

## E14: Isolated Pi Baseline and Repair-First DGM-Small Pilot

- ISOLATION:
  - fixed `@earendil-works/pi-coding-agent@0.85.1` and
    `byteplus/deepseek-v4-flash-ga`;
  - each task-solving workspace fetched only its exact base commit at depth 1,
    removed the remote, blocked network/package installation/Git-history
    commands, and excluded tests from submitted patches;
  - the per-task total-token ceiling was 512,000, counting input, output,
    cache-read, and cache-write tokens.
- ORIGINAL PI RESULT:
  - resolved 5/10: 10880, 10973, 11066, 12754, and 13279;
  - failed patches: 10999 and 13346;
  - no patch before the budget stop: 11087, 15930, and 16661;
  - aggregate telemetry: 3,442,234 reported tokens, 214 tool calls, and
    898.908 seconds.
- REPAIR PROTOCOL:
  - three failed tasks were selected before official repair grading;
  - one DeepSeek JSON repair call per task used only the task statement,
    rejected patch/failure evidence, and a bounded source slice;
  - exact-replacement edits were applied only when the old text occurred once;
  - every candidate was submitted to the unchanged official SWE-bench grader.
- REPAIR RESULTS:
  - 13346: `django/db/models/fields/json.py`, resolved;
  - 15930: `django/db/models/expressions.py`, resolved;
  - 10999: `django/utils/dateparse.py`, resolved;
  - total: 3/3 repair successes from 3 calls, raising the combined score to
    8/10.
- COMPARISON:
  - released DGM initial resolves 3/10 on the same task IDs;
  - released DGM best node `20250402_233611_093918` resolves 4/10;
  - isolated Pi resolves 5/10;
  - Pi plus RF-CLM recovery resolves 8/10.
- COST:
  - repairs recorded 24,084 input and 113,307 output tokens, 137,391 total;
  - this is 3.99% of all baseline Pi reported tokens and 12.53% of the
    baseline tokens spent on the three repaired tasks;
  - the gateway reported 20,473-51,860 output tokens despite an 8,192
    `max_tokens` request, so billable-token efficiency is not yet established.
- EVALUATOR IMAGE FIX:
  - the official instance recipe's full Django clone remained in `index-pack`
    after 12 minutes;
  - replacing it with a local depth-2 fetch reduced the 13346 instance build
    to 46.4 seconds while preserving the exact base commit, empty remote,
    official env image, install commands, image tag, test patch, and grader;
  - depth 2 is required only in evaluator images because the official eval
    script invokes `git show`; depth 1 makes the base look like a root commit
    and emits the whole tree, including binary locale files;
  - 15930 is listed in the harness `USE_X86` set. The legacy Docker builder
    initially selected the local ARM Ubuntu variant despite the old
    `linux/x86_64` label. Pinning a platform-specific source alias and
    normalizing to `linux/amd64` produced verified amd64 base, env, and instance
    images.
- DECISION:
  - the small-set quality gate passes, so no repair calls are added for 16661
    or 11087;
  - do not claim a matched full DGM/Pi win: released DGM uses another
    model/agent, and the multi-seed D60 plus hidden-140 protocol remains
    unexecuted;
  - do not claim endpoint cost dominance until the gateway token-limit anomaly
    is resolved or independently priced.
- STATUS: **DGM-SMALL DEVELOPMENT QUALITY PASSED; CONFIRMATORY AND ENDPOINT
  COST CLAIMS REMAIN OPEN.**

## E15: Evaluator-Feedback Audit Correction and DGM-200 Freeze

- AUDIT CORRECTION:
  - the three RF-CLM repair prompts consumed hidden failure information from
    the official SWE-bench evaluator after the original Pi patches were
    graded;
  - therefore the 8/10 result is a one-round evaluator-feedback recovery upper
    bound, not a standard one-submission SWE-bench score;
  - the earlier direct 8/10 versus DGM 4/10 framing is withdrawn as a
    protocol-matched comparison.
- FROZEN DATA:
  - DGM source commit:
    `682eb38a3eb232f4396924cacd0a083bf1444cf8`;
  - disjoint task panels: 10 small, 50 medium, 140 big;
  - SWE-bench Verified revision:
    `c104f840cc67f8b6eec6f759ebc8b2693d585d4a`;
  - ordered 200-task ID hash:
    `421c950302366954005dab020cdc89ca0d6ae1f0423e2b662637f7790a31d0d7`;
  - frozen manifest hash:
    `3fb913fbc73a05c1f7cae3b708c976374632820b58377aab5de08b742f96c967`;
  - manifest order exactly matches the released DGM 200-task
    `submitted_ids`.
- PROTOCOL:
  - P1 is original Pi one-shot with no official evaluator feedback;
  - P2 is Pi plus exactly one RF-CLM official evaluator-feedback repair and is
    always labeled feedback-assisted;
  - P2 is not placed in a direct standard-score table beside DGM's 50%.
- ISOLATION AUDIT:
  - Pi 0.85.1's built-in file tools accept absolute paths, parent traversal,
    home expansion, and external symlinks;
  - the benchmark runner now replaces them with workspace-confined tools and
    executes shell commands inside the task image with no network;
  - any excluded-path modification is retained as a protocol violation and
    omitted from the submitted patch.
- STATUS: **DATA AND PROTOCOL FROZEN; PAID 200-TASK EXECUTION NOT STARTED.**

## E16: DGM-200 Launch and TPM Pacing Amendment

- AUTHORIZATION: user approved an 80,000,000 reported-token cap and
  concurrency one.
- INFRASTRUCTURE: Colima verified at 8 CPU and approximately 16 GB RAM;
  the Docker root is `/var/lib/docker`. A no-network task-image smoke passed
  before paid execution.
- EARLY VALIDATION:
  - tasks 1-3 completed with official evaluator results;
  - original Pi resolved 1/3;
  - feedback-assisted RF-CLM resolved 3/3, repairing both unresolved tasks;
  - one initial recovery attempt failed before model invocation because the
    temporary SWE-bench venv lacked `openai`; installing the existing
    environment's exact `openai==2.48.0` fixed the runtime, and the task was
    resumed without repeating its original Pi call or evaluator.
- TPM INCIDENT:
  - task 5 (`astropy__astropy-13453`) received
    `RATE_LIMIT_TPM_EXCEEDED` with zero reported usage and no patch;
  - the gateway reported a 1,000,000 TPM limit and current TPM of 1,106,521;
  - the entire invalid task directory was moved to
    `dgm200_run/invalid_attempts/astropy__astropy-13453.tpm429-20260925T022019Z`;
  - the invalid attempt is excluded and will be rerun from its frozen input.
- AMENDMENT: add a fixed 90-second delay between tasks. This is an operational
  pacing change only; prompts, model, information boundaries, task order,
  per-task budgets, and official grading remain unchanged.
- INTRA-TASK TPM FOLLOW-UP:
  - the valid task-5 rerun produced 487,145 reported tokens and a patch before
    a later request received another TPM 429;
  - the existing patch passed the official evaluator, so this attempt remains
    in P1 rather than being quarantined;
  - starting after task 5, the local SSE adapter retries only HTTP 429
    responses up to three times, waiting at least 65 seconds and replaying the
    identical request body;
  - `dgm200_run/runtime_amendments.json` records the proxy hashes and exact
    applicability boundary.
- IMAGE-BUILD NETWORK FOLLOW-UP:
  - task 6 (`astropy__astropy-13579`) had two pre-generation Docker build
    failures after repeated 15-second PyPI read/TLS timeouts;
  - no model call occurred in either failed build attempt;
  - starting with the task-6 retry, prerequisite and instance Dockerfiles use
    build-only `PIP_DEFAULT_TIMEOUT=120` and `PIP_RETRIES=20` arguments;
  - dependency versions, source commits, target architectures, and runtime
    behavior are unchanged.
- STATUS: **RUNNING.** Do not analyze endpoint quality until all 200 tasks
  have valid P1 and P2 terminal states.

### E16 follow-up: terminal repair-error accounting

- The resumed pass reused tasks 1-5, then recorded PyPI-only image-build
  failures for tasks 6 and 7. Task 6's image completed in a separate
  prebuild process and is now cached; task 7 remains queued for a no-model
  prebuild retry.
- Task 8 completed P1 with an empty patch after 512,000 budget-counted tokens.
  Its inert feedback probe completed, but the single repair response proposed
  an exact replacement whose `old` text appeared three times. The repair is a
  P2 failure, not an evaluator or Docker failure, and no second repair call is
  permitted.
- The old runner raised before writing the response usage. Exact input/output
  tokens for this one call are irrecoverable from local evidence. The run
  reserves 512,000 conservative tokens against the global cap and marks the
  repair-token distribution incomplete instead of imputing values.
- The runner now persists model telemetry before applying edits. The
  orchestrator treats `repair_error` as a completed unresolved P2 outcome;
  only evaluator and execution failures trigger infrastructure retry/stop
  logic. This is a bookkeeping and resumability correction, not an algorithm
  or prompt change.
- Verification after the correction: 44/44 Python tests passed; Python
  compilation and `git diff --check` passed.

### E16 follow-up: deterministic image dependency cache

- Task 12 reproduced the PyPI empty-index failure before any model request.
  A local wheelhouse was populated from official PyPI for the exact Astropy
  Python 3.9 ARM64 build requirements and frozen with a SHA-256 manifest.
- Instance setup and the official evaluator now use that wheelhouse with
  `PIP_NO_INDEX=1`. The evaluator repeats the editable install, so the
  wheelhouse remains in the image for that step. It contains only public build
  dependencies, never task source or hidden evaluation data.
- The task-13 verification image built in 48.457 seconds, had ARM64
  architecture, exact base commit
  `a3f4ae6cd24d5ecdf49f213d77b3513dd509a06c`, no Git remote, and all
  wheelhouse hashes verified inside the no-network container.
- The orchestrator now retries image-only failures twice, does not sleep after
  already-completed task skips, and measures the wall cap from the original
  run start across resumptions.
- Verification: 45/45 Python tests, Python compilation, and
  `git diff --check` passed. Root checks again passed through all pre-tsgo
  gates and failed only on the existing model-catalog `unknown`/`never`
  errors.

### E16 follow-up: commit-specific Cython wheel

- Task 16 (`astropy__astropy-14995`) pins `Cython==0.29.34`; the frozen
  wheelhouse contained only Cython 0.29.30, so all three image-build attempts
  failed before model invocation.
- Execution was stopped before task 17. The exact CPython 3.9 ARM64 wheel was
  identified from PyPI release metadata, downloaded through the Tsinghua PyPI
  mirror, and verified against PyPI's published SHA-256
  `5718319a01489688fdd22ddebb8e2fcbbd60be5f30de4336ea7063c3ae29fbe5`.
- The wheelhouse manifest now hashes to
  `bbc5cc9269f4e705fbebdb6b0a9d4d5a15b257817481fb1ec85957710767b07e`;
  all listed artifacts pass `shasum -a 256 -c`.
- This supplies the task's already-pinned public build dependency. It does not
  change task source, dependency resolution, prompts, model calls, or grading,
  and the infrastructure attempts remain excluded from quality metrics.

### E16 follow-up: Astropy 1.3 x86_64 compatibility images

- Tasks 17-20 share an Astropy 1.3 environment that pins Python 3.6 and
  `setuptools==38.2.4`. SWE-bench selected ARM64 from the ARM64 host, but that
  exact setuptools build is unavailable on current ARM64 Conda channels.
- SWE-bench architecture selection is host-dependent: the same TestSpec uses
  x86_64 on an x86_64 host. A temporary wrapper therefore prebuilt only these
  four evaluator images as x86_64, preserving their official setup scripts,
  pinned dependencies, source commits, and evaluator commands.
- The official evaluator independently regenerates TestSpecs. A persisted
  Python launcher with SHA-256
  `127ffd035fce1fb43401de94aaa21032430e56326bb60e222c6fdaa9d7edb82c`
  applies the same x86_64 host report only when `run_evaluation` receives one
  of these four IDs; every other Python invocation and task is unchanged.
- QEMU produced random GCC signal-11 failures. One temporary `CFLAGS=-O1`
  attempt also failed and produced no image. Colima was restarted with
  Virtualization.framework Rosetta support; all final images then used the
  standard `-O3` compiler flags.
- Final image verification confirmed amd64 architecture, exact base commits,
  no Git remotes, and valid wheelhouse hashes for all four tasks. No model call
  occurred during failed or successful prebuild attempts.
- The user-paused interval from Unix `1790316408` to `1791514558`
  (1,198,150 seconds) is excluded from the 86,400-second active wall-time cap.
  The original start time remains recorded in `run_state.json`; token limits,
  prompts, task order, and per-task timeouts are unchanged.
- Accuracy results remain protocol-comparable. Runtime results will be
  reported by architecture/emulation stratum because x86_64 Rosetta and
  native ARM64 evaluator timings are not directly interchangeable.

### E16 follow-up: task-17 user interruption

- The first valid-image attempt for task 17 was externally terminated with
  exit `-9` before `result.json` was atomically written. Its 12 completed
  turns report 101,767 tokens; an in-flight request has no recoverable usage.
- The entire attempt is quarantined under
  `dgm200_run/invalid_attempts/astropy__astropy-7166.user-interrupt-20261009T111347`
  and is excluded from accuracy, latency, and patch metrics.
- The global token budget reserves the full 512,000-token per-task ceiling for
  this invalid attempt. The reservation will be attached to the valid task-17
  result before advancing to task 18, then the frozen task is rerun once.
