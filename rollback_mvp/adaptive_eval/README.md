# Agentic Adaptive Evaluation Controller

Independent, fail-closed controller for evaluating one DGM-style Pi mutation.
It does not modify Pi core, run as an extension hook, train a policy, combine
lexical and semantic scores, or select audit tasks with a model.

## Implemented boundary

- Validates the literal DGM-200 manifest SHA-256 and ordered-ID SHA-256.
- Builds public-only task cards, pure-Python BM25, and a separate semantic index.
- Enforces the pinned 1024-D normalized Qwen sidecar response contract.
- Runs a strict selector tool loop with immutable rounds and explicit budgets.
- Samples the deterministic independent audit only after selector termination.
- Freezes one final manifest for parent, child, and every counterfactual.
- Runs identity-bound paired artifacts and deterministic ACCEPT/ROLLBACK/ESCALATE.
- Defines and tests a full-candidate container contract with no host fallback;
  the production Docker adapter remains deliberately blocked pending attestation.
- Runs the final pair, deterministic decision, and report through `pipeline.py`;
  invalid pair/identity evidence is persisted as `decision_invalid`.

The production experiment path requires `tqdm`. Its absence is terminal. The
test suite injects a plain progress iterator and never contacts a real model,
embedding service, Docker daemon, or paid service.

The checked-in production boundaries are interfaces, not configured services:
there is no real selector-model adapter, trusted adaptive-round evaluator,
CLM/ddmin adapter, or deployable restricted model proxy in this change. Tests
use scripted selector, fake embeddings/evaluators, and fake container runtime.

## Validation

```bash
python3 -m rollback_mvp.adaptive_eval.cli validate-catalogue
python3 -m unittest discover -s rollback_mvp/adaptive_eval -t . -p 'test_*.py' -v
```

## Run artifacts

Given an experiment output directory, selection/execution/pipeline components write:

- `selection-manifest.json`: raw selector responses, prompts/tool calls,
  candidates, proposals, embedding cache/vector hashes, coverage, audit, and
  final task IDs.
- `state/events/*.json`: hash-chained append-only round, pair, freeze, and error
  events.
- `frozen-task-plan.json`: the parent/child/counterfactual task-plan identity.
- `pairs/<task>/<role>/`: execution request, observation, exceptions, trajectory
  hashes, telemetry, and identity mismatch evidence.
- `counterfactuals/<artifact>/<task>/`: written only when an external CLM/ddmin
  integration calls the boundary with the identical final manifest; unequal
  plans are rejected.
- `final-report.json`: paired statistics, coverage/redundancy, telemetry, and
  deterministic decision.

## Container runtime status

The tested contract requires a digest-pinned image, verified candidate source
hash, `network=none`, read-only root, non-root user, dropped capabilities,
no-new-privileges, a hash-pinned seccomp profile, fresh-workspace claims, bounded
regular output files, and a restricted Unix-socket model proxy. Candidate output
is copied outside the mutable mount; an outside evaluator grades the patch.
Controller, evaluator, gold/test patches, credentials, and Docker socket are not
candidate mounts.

This checkout's Docker client is present, but its Colima daemon socket is not
accessible. In addition, `DockerCliRuntime` deliberately refuses execution until
quota-backed workspace/output volumes, proxy enforcement, fresh-workspace
claims, and timeout cleanup can be attested. The implementation never launches
candidate Pi on the host.
