# pi-causal-rollback

A pi extension for evidence-gated rollback of evolving prompts, skills, tools,
and other harness artifacts.

The extension does not ask an LLM to make the final rollback decision. An
optional diagnoser ranks candidate patches; a configurable executable probe
then searches for a one-minimal patch-removal set that repairs the failure. The
result is an auditable rollback-and-replay plan.

## Install

From a checkout:

```bash
pi install ./pi-rollback -l
```

For a published repository:

```bash
pi install git:github.com/OWNER/pi-causal-rollback
```

## Commands

```text
/rollback checkpoint [label] [--depends id,id]
/rollback diagnose <failure-bundle.json>
/rollback status
/rollback apply [diagnosis-id]
/rollback apply [diagnosis-id] --execute
```

`apply` is a dry run unless both conditions hold:

1. `.pi/rollback.json` sets `"dryRun": false`.
2. The command includes `--execute` and the interactive confirmation is
   accepted.

The extension never runs `git reset`, `git checkout`, or `git stash`. It only
changes paths listed in `artifactPaths`.

## Configuration

Create `.pi/rollback.json`:

```json
{
  "artifactPaths": [".pi/extensions/evolving", ".pi/skills/evolving"],
  "probeCommand": ["node", "scripts/rollback-probe.mjs"],
  "priorCommand": ["node", "scripts/rollback-prior.mjs"],
  "probeRepeats": 3,
  "timeoutMs": 300000,
  "maxSliceFraction": 0.3,
  "minSliceRecall": 0.95,
  "singletonBudget": 1,
  "dryRun": true
}
```

`priorCommand` is optional. Each external command receives one final argument:
the absolute path to a JSON request. Commands run without a shell.

The slice fast path is enabled only when the failure bundle provides candidate
patches covering at most `maxSliceFraction` of the active lineage and an audited
`sliceAuditRecall` at or above `minSliceRecall`. Otherwise diagnosis uses full
repair-ddmin. If removing the slice does not repair the full lineage, diagnosis
falls back to the full lineage.

## Failure Bundle

```json
{
  "id": "tool-schema-regression",
  "summary": "Reload advertises a stale tool schema.",
  "candidatePatches": ["tool-cache", "reload-reuse"],
  "priorOrder": ["reload-reuse", "tool-cache"],
  "sliceAuditRecall": 0.97,
  "metadata": {
    "model": "deepseek-v4-flash",
    "promptHash": "sha256:...",
    "dataHash": "sha256:...",
    "gitHash": "..."
  }
}
```

Checkpoint references may be checkpoint IDs or unique labels.

## Probe Contract

The request contains:

```json
{
  "schemaVersion": 1,
  "failure": {},
  "workspace": "/absolute/project/path",
  "activePatchIds": ["cp-...", "cp-..."],
  "checkpoints": [
    {
      "id": "cp-...",
      "label": "cache-layer",
      "parentId": "cp-...",
      "snapshotDir": "/absolute/path/to/snapshot/files",
      "changedFiles": [".pi/extensions/evolving/cache.ts"],
      "dependsOn": []
    }
  ]
}
```

The evaluator must materialize or otherwise evaluate `activePatchIds` and print
one JSON object:

```json
{
  "failed": true,
  "cost": 0.03,
  "inputTokens": 1200,
  "outputTokens": 40,
  "model": "evaluator-name",
  "retries": 0
}
```

The optional prior command receives the failure and checkpoint manifests and
returns:

```json
{
  "order": ["checkpoint-label-or-id"],
  "model": "diagnoser-name",
  "inputTokens": 900,
  "outputTokens": 120,
  "cost": 0.01,
  "retries": 0,
  "rawResponse": "..."
}
```

## What Is Stored

- Content-addressed artifact snapshots:
  `.pi/rollback/artifacts/<sha256>/`
- Probe requests, raw stdout/stderr, decisions, costs, tokens, latency, retries,
  fallback state, and hashes:
  `.pi/rollback/runs/<diagnosis-id>/`
- Checkpoint and diagnosis records as pi `CustomEntry` values, so session
  branches retain their own lineage.

Snapshots reject absolute paths, parent traversal, Git internals, symlinks, and
paths overlapping the rollback store. Snapshot contents can still contain
secrets; keep `.pi/rollback/` out of version control.

## Rollback Semantics

1. Verify that the current checkpoint fails and the baseline passes.
2. Test whether removing the highest-prior patch repairs the full lineage.
3. If not, run ddmin directly over removal sets on a gate-eligible dependency
   slice, or on the full lineage.
4. Return a one-minimal sufficient removal set verified against the full
   failure probe. This intentionally does not spend probes recovering every
   member of the complete causal family when one removal is already sufficient.
5. Restore the checkpoint before the earliest removal.
6. Replay later patches only when they neither depend on a removed/skipped patch
   nor overlap its changed files.
7. Probe the exact dependency-safe replay plan; abstain if the extra skipped
   patches reintroduce or expose a failure.
8. Navigate pi's session tree to the checkpoint anchor, persist the resulting
   replayed state as a new checkpoint, and reload resources.

File overlap is treated conservatively because full-file snapshots cannot prove
that two edits to the same file commute. Semantic dependencies can be declared
with `--depends`.

## Deterministic Demo

The demo models a failure that requires both `cache-layer` and
`parallel-workers`.

```bash
mkdir -p .pi
cp pi-rollback/fixtures/rollback.json .pi/rollback.json
pi -e ./pi-rollback
```

Inside pi:

```text
/rollback checkpoint baseline
!node pi-rollback/fixtures/demo-step.mjs cache-layer
/rollback checkpoint cache-layer
!node pi-rollback/fixtures/demo-step.mjs logging
/rollback checkpoint logging
!node pi-rollback/fixtures/demo-step.mjs telemetry
/rollback checkpoint telemetry
!node pi-rollback/fixtures/demo-step.mjs formatting
/rollback checkpoint formatting
!node pi-rollback/fixtures/demo-step.mjs retries
/rollback checkpoint retries
!node pi-rollback/fixtures/demo-step.mjs parallel-workers
/rollback checkpoint parallel-workers
!node pi-rollback/fixtures/demo-step.mjs docs
/rollback checkpoint docs
/rollback diagnose pi-rollback/fixtures/failure.json
/rollback apply
```

The expected diagnosis verifies that removing `cache-layer` is sufficient,
rolls back before it, and retains the independent later patches. It does not
spend additional probes proving that `parallel-workers` is also a member of the
full conjunctive cause set.

## Evidence and Limits

Offline experiments found:

- The corrected DGM census has 69 start-pass/end-fail episodes: 56 monotone and
  13 non-monotone. Binary search was less accurate and more expensive than
  linear scan over all corrected episodes.
- Full ddmin recovered all clean synthetic 1-3 patch interactions.
- Sliced ddmin preserved exact recovery through fallback, but a reliable cost
  win appeared only when the slice covered at most 30% of edges with at least
  95% cause recall.
- At 40% slices, savings were only 11%-14%; the universal low-cost claim was
  rejected.
- Repair-first minimization achieved 97.0%-100% repair success and
  96.67%-100% one-minimal removals across seven conjunctive, alternative,
  mixed, noisy, low-recall, prior-sensitivity, and shallow-lineage settings.
  It reduced probe calls by 42.86%-49.89% versus the previous failure-first
  path; every paired 95% bootstrap interval for call reduction excluded zero.
- On DGM's 10-task SWE-bench Verified development subset, isolated Pi 0.85.1
  with DeepSeek solved 5/10. Three one-call causal-slice repairs all passed the
  official grader, raising the combined result to 8/10. The best released DGM
  node solves 4/10 on those task IDs, but uses a different model and agent
  substrate.
- All 15 package tests pass, including exact dependency-safe replay-plan
  verification and abstention when that plan does not repair the failure.

The 8/10 result is development-set evidence, not a full matched evolution
claim. A publication-level comparison still requires same-model DGM-style
evolution, multiple seeds, and the untouched 140-task holdout. Endpoint cost
dominance is also unverified because the model gateway exceeded the requested
repair output-token cap.
