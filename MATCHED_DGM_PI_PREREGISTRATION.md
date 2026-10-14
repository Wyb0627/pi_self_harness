# Pre-Registration: Matched DGM/P2-on-Pi Pilot

Date frozen: 2026-10-14

## Question

Does project-specific Pi harness evolution improve one-pass performance on the
isolated DGM big-140 endpoint? The pilot compares P0, DGM-style archive search,
and DGM-style search with an RF-CLM adaptive rollback gate.

## Claim Boundary

The mutable artifact contains:

- Pi is the task agent and mutation-proposer substrate.
- `strategy.md`.
- A strict `tools.json` manifest and at most four human-readable Python tool
  handlers.
- Generated handlers run only through a trusted host proxy in the task image
  with `network=none`, a read-only candidate mount, and a read-write task
  workspace. They cannot become Pi lifecycle hooks or execute on the host.

The two evolution arms share mutation, task-agent, model, container, per-call,
slot, and wall limits:

- DGM has no adaptive rollback.
- P2 uses an agent-only adaptive gate. Every selected gate task must be from the
  failed entry task's repository. On a verified regression, repair-first CLM
  finds a minimal sufficient removal set, restores the earliest affected
  lineage prefix, and dependency-safely replays later mutations.
- Parent selection, keep-all archive behavior, and 10-to-60 promotion follow
  DGM's released algorithm.
- The endpoint is adapted to a strict big-140 holdout.

Pi core and the host harness remain frozen. This is not a source-level DGM
reproduction. The big-140 tasks are hidden from this new search, but they have
appeared in historical repository runs and human analysis. The result tests
isolation from the new search, not project-wide unseen-benchmark generalization.

## Hypothesis

**H1:** The final DGM archive artifact has higher one-pass big-140 accuracy than
P0.

**H2:** The final P2 archive artifact has higher one-pass big-140 accuracy than
matched DGM.

**Kill criteria:** H1 is rejected for this seed when DGM-minus-P0 is
non-positive. H2 is rejected for this seed when P2-minus-DGM is non-positive. A
broad policy-level claim is rejected unless at least three independent matched
seeds are later run and the seed-level paired interval excludes zero. Any
D_test visibility before search sealing, identity mismatch, endpoint rerun, or
hidden evaluator feedback entering mutation invalidates the run.

## Frozen Data

- Full DGM-200 manifest SHA-256:
  `3fb913fbc73a05c1f7cae3b708c976374632820b58377aab5de08b742f96c967`
- D_evolve: literal DGM small 10 plus medium 50.
- D_test: literal DGM big 140.
- D_test is materialized only after `search-seal.json` exists.
- Historical DGM200 outputs are forbidden mutation input and cache evidence.

## DGM Search Policy

- Pilot maximum: 10 proposal slots, organized as five waves of two proposals.
- Concurrency: one locally; wave parent draws are still frozen before either
  proposal executes.
- Parent sampling with replacement:

  `weight = sigmoid(10 * (score_60 - 0.5)) / (1 + functioning_child_count)`

- A child first runs small-10 and promotes when it resolves at least 4/10.
- A promoted child runs the additional medium-50.
- Every valid cumulative-60 child enters the unbounded archive, including
  children worse than their parent.
- Final artifact: highest cumulative-60 score, then earliest insertion ordinal,
  then artifact hash.
- Mutation is anchored to one failed D_evolve entry task and sees only the
  parent artifact plus sanitized public same-repository D_evolve task text.
- Mutation output may append one strategy section and add or replace one
  candidate tool. Task IDs may appear only in selector output, never in
  strategy or tool content.
- P2 runs the same fixed cumulative-60 archive score after its adaptive
  same-repository gate and any verified RF-CLM repair.

## Budgets

| Reserve | Global reported-token stop | Active wall cap |
| --- | ---: | ---: |
| DGM/P2 search | none | 108,000 s |
| Final harness big-140 endpoint | 80,000,000 | 108,000 s |
| Shared P0 big-140 reference | 80,000,000 | 108,000 s |

Per task: 512,000 total reported tokens, 65,536 output tokens, and 3,600
seconds. Mutation: 64,000 total reported tokens, 16,384 output tokens, and 900
seconds. Search stops on the 10-slot limit or active wall limit, not a global
token threshold. Actual token use remains fully logged. Endpoint reserves are
non-transferable.

## Metrics

- Primary: DGM and P2 resolved/140; paired DGM-minus-P0 and P2-minus-DGM.
- Secondary: Wilson intervals, paired bootstrap interval, exact McNemar value,
  P0-only/final-only/ties.
- Cost: input/output/cache token totals, API calls, task executions, agent
  duration, evaluator duration, image-build time, pacing time, and active wall
  time.
- Search: proposal slots, archive size, D_evolve score curve, invalid
  candidates, small-screen rejects, adaptive gate pairs, RF-CLM probes,
  removals, replay plans, and wall/slot termination.

Task-level statistics describe one artifact pair. They are not independent
evolution replicates and cannot establish policy-level superiority.
