# DGM to P2 Partial Experiment Handoff

## Snapshot

- Stop time: `2026-10-20T06:00:16Z` / `2026-10-20T14:00:16+08:00`.
- Stop reason: user-requested machine handoff, not algorithm failure.
- Stop method: `SIGINT` to formal PGID 15186; no force kill. The idle login
  shell created by the launcher was closed with `SIGHUP` after cleanup.
- Schedule: `每小时监测 DGM-P2 实验` is paused; last run
  `2026-10-20T05:08:05.590076Z`.
- Branch/current handoff source: `main` at `855e89073f00d217e7687f9c29510dd88a32024e`.
- Frozen experiment source: `64de49831ac64144b0981428cd6c104bb8f97196`.
- Protocol: `matched-dgm-pi-v2`; seed `20261014`; concurrency `1`.
- Model: `rollback-deepseek / byteplus/deepseek-v4-flash-ga`.
- D_test consumed: **no**. There is no search seal, endpoint state, endpoint
  materialization, or P2 observation.

## Progress and Accuracy

- P0: **21/60 = 35.00%**.
- Slot 0: **23/60 = 38.33%**, archived.
- Slot 1: mutation output invalid, rejected before task evaluation.
- Slot 2: **3/10 = 30.00%**, rejected by the 4/10 small-panel gate.
- Slot 3: **20/60 = 33.33%**, archived.
- Slot 4: mutation persisted; first small task was interrupted during official
  evaluation and has no observation. Slot 4 must resume from its first task.
- Slots 5-9: not started.
- Partial-search best: `30be840203090319746a26f6a5ca5ab68280a2d630e900066c3908fa4d03d4b9` at
  **23/60 = 38.33%**. This is not a
  final sealed DGM result and must not be used for a DGM/P2 conclusion.
- P2: prepared, paid preflight passed before launch, search not started.

## Cost Snapshot

- Complete observations: `190`.
- Valid/resolved: `190` /
  `67`.
- Ledger reported tokens: `70,678,467`.
- Conservative charge: `0`.
- API calls/task executions: `195` / `190`.
- Ledger active time: `41,389.387` s
  (`11:29:49`).
- Agent/evaluator/image time: `21,317.445` /
  `2,295.212` / `217.512` s.
- Interrupted task consumed `233,205` reported tokens according to its
  persisted result, but it is excluded from formal token and accuracy aggregates.
- Status distribution: 86 completed, 104 valid task-budget-exhausted observed
  zeros, 0 provider/runner infrastructure-invalid, and 0 timeouts.
- Observation aggregation and task-ledger aggregation agree exactly on reported
  tokens, task count, resolved count, and status distribution.

## Budget Clarification

The search-wide token cap is already `null` for both DGM and P2. The observed
search token count therefore cannot stop search. The two 80,000,000 token values
are independent post-seal reserves for `endpoint:p0` and `endpoint:final`, each
covering a configured maximum reservation of 71,680,000 tokens. They remain
frozen because changing them would invalidate the experiment config and protocol
hashes.

## Checkpoint

- Manifested payload: `1276` files,
  `4,090,169` bytes.
- Integrity: `file-manifest.sha256`; validate with
  `python3 validate_checkpoint.py`.
- Complete observation evidence only; workspace, trace, runner/evaluator logs,
  PEM, proxy logs, auth, environment, and credentials are excluded.
- Resume instructions: `remote-restore-and-resume.md`.
- Metrics: `metrics-summary.json`, `metrics-by-phase.csv`,
  `task-outcomes.csv`, and `interrupted-tasks.json`.

The checkpoint is a user-requested partial checkpoint. It is not a
`search-seal.json`, success record, or `infrastructure_invalid` record.
