# Agentic Adaptive Evaluation for DGM-Style Pi Evolution

## 1. Decision

This document defines the dynamic task-sampling controller used to evaluate one
candidate Pi evolution. It replaces a manually fixed per-branch subset for
online accept/rollback decisions.

The fixed universe remains DGM's 200 SWE-bench Verified tasks:

- Manifest: research_output/clm_budgeted_evolution_20260924_125503/dgm_swebench_verified_200.v1.json
- Ordered-ID SHA-256: 421c950302366954005dab020cdc89ca0d6ae1f0423e2b662637f7790a31d0d7
- Manifest SHA-256: 3fb913fbc73a05c1f7cae3b708c976374632820b58377aab5de08b742f96c967
- Distribution: 153 Django, 25 Sphinx, and 22 Astropy tasks.

The system calls frozen model APIs for diagnosis, query planning, reranking, and
iterative search. It does not train an RL policy. Deterministic code owns
budget enforcement, task validation, audit sampling, paired execution,
statistics, and the final decision.

> The model may propose what to inspect. Immutable execution evidence decides
> whether the candidate is accepted, rolled back, or escalated.

## 2. Scope and non-negotiable invariants

### 2.1 DGM-compatible evolution scope

DGM evolves the coding agent's own implementation, not only prompts. Its
self-improve prompt names coding_agent.py, tools, utils, prompts, workflow, and
requirements; released patches modify both the main agent and tools. Its archive,
benchmark evaluator, and outer evolution process remain outside the mutable
agent code.

The Pi equivalent is:

| Mutable candidate artifact | Immutable control plane |
| --- | --- |
| Pi coding-agent source, allowed tools, prompts/workflows, and declared dependencies | Dynamic sampler, task catalogue, embedding manifest, evaluator, decision policy, archive controller, rollback/CLM controller, and result store |

The candidate source must run as a whole process inside its task container. The
current rollback_mvp/pi_swe_runner.mjs launches Pi on the host and only routes
shell commands into Docker. It is suitable for prompt-only work, but not for
full DGM-equivalent self-modification: evolved extension/tool code could
otherwise execute in the host Pi process.

The container has no general network access. If the candidate needs an LLM, it
uses a narrowly validated host-side model proxy over a mounted local socket. The
proxy accepts only the frozen model/request schema and budget, holds credentials
outside the container, and rejects arbitrary HTTP destinations. The controller,
evaluator, gold patches, test patches, and official grader stay outside the
mutable candidate filesystem.

### 2.2 Evidence available to the sampler

The sampler receives only information available at an online evolution decision:

- Task catalogue fields: instance ID, repository, base commit, and public issue
  statement, plus deterministic features derived from them.
- Parent artifact trajectories, public-test/tool output, and previously observed
  parent failures.
- Parent-to-child artifact diff, changed paths/symbols, dependency change, and a
  frozen mutation summary.
- Earlier paired results from this same adaptive search, as sanitized public
  execution evidence.

The sampler must not receive gold patches, test patches, private evaluator logs,
future evolution outcomes, or outcomes from another candidate. Official grader
results feed the deterministic decision engine only; the selector never sees
hidden assertion text or grader-specific failure details.

The child diff is a necessary third signal alongside task content and historical
bad-case causes. Without it, the sampler cannot tell a context-compaction
change from a tool-editing change that happens to share past failures.

### 2.3 What an adaptive batch can and cannot measure

An adaptive batch is an operational diagnosis and safety gate. It intentionally
oversamples tasks likely to expose the current mutation's benefit or regression;
it is not an unbiased estimate of all 200 tasks. The independent audit detects
obvious selection blind spots, but a small audit cannot establish a global score.

For a publishable endpoint, pre-register one of the following before evolution:

1. Run the final frozen agent on all 200 tasks and label the result as an
   endpoint on a repeatedly exposed universe.
2. Reserve a task subset that never enters online sampling and use it once for
   the final endpoint. The combined catalogue remains exactly DGM's 200 tasks.
3. Use a separate held-out benchmark for the headline claim.

The controller records task roles but does not silently infer a split.

## 3. Data contracts

### 3.1 Task card

Each immutable TaskCard is indexed once for the 200 frozen rows:

~~~
TaskCard {
  instance_id, repo, base_commit, problem_statement,
  lexical_terms, structured_tags, task_text_hash,
  embedding_id, embedding_vector_hash, catalogue_revision
}
~~~

Lexical terms preserve exact signals such as exception classes, API names,
paths, tools, and component names. Structured tags are deterministic repository
and issue metadata, not LLM labels. The catalogue stores no evaluator-only
material.

### 3.2 Parent bad-case card

One BadCaseCard is produced per prior parent failure and is versioned by the
exact parent artifact:

~~~
BadCaseCard {
  parent_artifact_hash, instance_id, outcome, failure_taxonomy,
  trajectory_summary, tool_error_fingerprints, changed_paths,
  public_test_summary, source_trace_hash, created_at
}
~~~

The taxonomy is an assistive retrieval label, not a causal verdict. Raw
trajectory, structured extraction, model/prompt metadata, and parsing errors
are retained for case studies. A malformed or untraceable bad case is recorded
and excluded; it is never replaced with invented text.

### 3.3 Candidate-change card

~~~
CandidateChangeCard {
  parent_artifact_hash, child_artifact_hash, diff_hash,
  changed_paths, changed_symbols, dependency_change, mutation_summary,
  source_revision, created_at
}
~~~

The controller recomputes the diff hash from frozen parent and child snapshots.
A request is invalid if the hashes or fixed task manifest do not match its run
state.

## 4. Agentic multi-round retrieval

### 4.1 Why this is not a weighted four-way score

The following four roles answer different questions and have incomparable score
scales. A global formula such as a times repair plus b times regression plus c
times diversity plus d times exploration would introduce brittle, unjustified
coefficients. The selector instead plans and revises queries through tools. The
only fixed quantities are explicit resource limits, not route weights.

| Role | Question | Who selects |
| --- | --- | --- |
| Repair/cause recall | Which tasks resemble a parent bad case that the mutation claims to address? | Selector agent after inspecting lexical and semantic results |
| Regression recall | Which tasks exercise behavior touched by the child diff and might regress? | Selector agent after inspecting the change and task cards |
| Representative coverage | Which remaining tasks cover behavior regions not yet represented? | Deterministic facility-location tool, inspected by the selector |
| Independent audit | Which tasks could reveal unknown blind spots? | Deterministic seeded sampler, never the selector |

The first two are hypotheses. The third is deterministic diversity pressure.
The fourth is an independence guard. They must not be collapsed into one learned
reward.

### 4.2 Selector tools

The selector is a tool-calling model with a frozen system prompt and model/API
revision. It receives only these read-only tools:

~~~
search_lexical(query, filters, limit)
search_semantic(query, limit)
get_task(instance_id)
get_bad_case(bad_case_id)
get_change()
marginal_coverage(candidate_ids, selected_ids, universe)
inspect_round_results(round_id)
propose_tasks(instance_ids, rationale, expected_signal)
finish_round(stop_reason)
~~~

Lexical search uses exact/token/BM25-style retrieval over task cards. Semantic
search returns cosine-ranked task cards from the local embedding index. The
result lists stay separate and retain source/rank metadata. The implementation
must not silently make a weighted lexical-plus-embedding score; the model can
inspect both and issue another query.

Every proposal must name a retrieval role, evidence reference, testable expected
signal, and plain-language rationale. Unknown task IDs, duplicate IDs, attempts
to read restricted data, malformed output, and unrecognized tool calls terminate
the run as invalid rather than falling back to a heuristic subset.

### 4.3 Round protocol

For a mutation from parent P to child C:

1. Freeze an initial controller request with the catalogue, P/C hashes, change
   card, eligible parent bad cases, controller-held audit-seed derivation,
   API/embedding revision, and all explicit resource limits. The selector sees
   no audit seed or audit-candidate list.
2. In each round, the selector searches and proposes new non-audit tasks. The
   controller validates and appends an immutable round record before execution.
3. Evaluate P and C on exactly that round's tasks under matched execution
   identities. The next round may inspect sanitized pair aggregates and public
   trajectory evidence.
4. Stop only on a declared evidence-saturation rationale or an explicit task,
   selector-token, time, or round limit.
5. Union all non-audit selections, independently sample audit tasks from the
   remaining eligible catalogue, and freeze the final task union. Only then may
   CLM/ddmin counterfactual replay begin.

A later round appends tasks; it cannot edit an earlier round. There are no
implicit defaults for task budget, maximum rounds, audit size, per-task limits,
or selector-token budget. Every value is required in a versioned experiment
configuration.

Within each non-audit round, selection is lexicographic rather than a weighted
score sum. `coverage_selection_mode` is a required, hash-bound experiment
parameter with two modes:

- `greedy`: the selector returns an ordered set of direct repair/regression
  hypotheses. If hypotheses compete for remaining capacity, the controller
  chooses the candidate with greatest marginal coverage and uses instance ID
  only as a stable final tie-break. If capacity remains after direct
  hypotheses, it fills from the inspected candidate pool by marginal coverage;
  if that pool is empty, it uses the full eligible catalogue. A direct
  hypothesis with zero marginal coverage remains valid only when its evidence
  explicitly says why the apparent duplicate is a necessary distinct
  regression probe.
- `agent_only`: the controller preserves direct proposal order, truncates at
  round capacity, and never fills an under-capacity round. Marginal coverage is
  still recorded after selection for reporting, but it neither reorders nor
  rejects proposals.

The selector prompt exposes the active mode and exact round capacity. Changing
the mode changes the configuration hash, so evidence from the two arms cannot
be mixed. Neither mode adds a per-route quota or weighted score.

### 4.4 Controller pseudocode

~~~
selected = []
for round_id in range(config.max_rounds):
    proposal = selector_tool_loop(request, prior_round_summaries, selected)
    validated = validate_proposal(proposal, catalog, config)
    state.append_round(validated)
    result = paired_executor.run(parent, child, validated.task_ids)
    state.append_pair_result(result)
    selected.extend(validated.task_ids)
    if proposal.stop or state.budget_exhausted():
        break

audit = deterministic_audit(pool - set(selected), config.audit_seed)
manifest = state.freeze_union(selected, audit)
decision = decide(run_pairs(manifest.final_task_ids))
~~~

The final paired run may reuse a round result only if its full execution
identity is identical. Otherwise it reruns the task. This prevents a result
from another model, image, budget, or child snapshot entering a decision.

## 5. Coverage and redundancy

### 5.1 Similarity

For fixed task catalogue U, task embedding vectors are L2-normalized:

~~~
sim(i, j) = max(0, cosine(embedding(i), embedding(j)))
~~~

Similarity lies in [0, 1]. Lexical retrieval is for exact candidate generation,
not mixed into this semantic similarity with an arbitrary coefficient. The
coverage universe is explicit configuration, normally all online-eligible tasks
in the fixed 200-task catalogue. The initial definition is task-uniform
coverage. A repository-balanced definition is a different declared protocol,
not an invisible weight.

### 5.2 Facility-location coverage

For selected set S:

~~~
Coverage(S) = (1 / |U|) * sum over u in U of max over s in S sim(u, s)
~~~

This measures whether each catalogue task has a semantically similar
representative in S. The deterministic tool reports the marginal value of
candidate x:

~~~
DeltaCoverage(x | S) = (1 / |U|) * sum over u in U of
  max(0, sim(u, x) - max over s in S sim(u, s))
~~~

Facility location has diminishing returns: a near-duplicate contributes little
after a related task is selected. In `greedy` mode it fills remaining capacity
after direct repair/regression hypotheses without a diversity coefficient. A
zero-gain task is rejected unless it has a documented direct
causal/regression rationale. In `agent_only` mode these values are report-only
and do not affect task selection.

Example: after a Django migration case, another nearly identical migration case
usually has low marginal coverage. A Sphinx documentation case may have much
higher marginal coverage even when it shares no keywords with the mutation.
The batch therefore avoids becoming ten versions of one failure trace.

### 5.3 Redundancy diagnostic

Coverage drives completion. Redundancy is report-only:

~~~
Redundancy(S) = (1 / |S|) * sum over s in S of
  max over t in S, t != s of sim(s, t)
~~~

For fewer than two tasks, redundancy is zero. A value near one means most
selected tasks have a near-duplicate neighbor; a low value indicates spread.
The report records each task's nearest neighbor and similarity so the aggregate
is auditable.

Redundancy is not subtracted from an LLM score and cannot override a causally
necessary regression probe. Facility-location marginal gain already supplies
the anti-duplication pressure; redundancy exposes selection collapse and makes
ablations comparable.

## 6. Local embedding and lexical retrieval

### 6.1 Retrieval choice

Use lexical candidate generation plus local Qwen semantic retrieval. Do not use
pure grep as the production mechanism.

Lexical matching is valuable for error classes, tool names, symbols, paths, and
component labels. It cannot reliably recall behavior described with different
language, for example a trajectory saying that constraints disappeared after
compaction and an issue saying requirements vanish after context truncation.
With only 200 tasks, pre-embedding every task and comparing all 200 vectors per
query is cheap enough that semantic recall should not be sacrificed.

Lexical-only is a valid explicit ablation. Missing embedding infrastructure,
model/revision mismatch, malformed vectors, or index-hash mismatch must fail
closed. The controller must never silently substitute lexical search.

### 6.2 Reproducible MLX research sidecar

Use this pinned model:

~~~
model: mlx-community/Qwen3-Embedding-0.6B-4bit-DWQ
revision: 6c3ae70858513f1a78e9cdca3cae330d9075cd2a
dimension: 1024
pooling: last token
normalization: L2
~~~

The current Conda base has no mlx, mlx_lm, mlx_embeddings, transformers, or
cached MLX model. Provision a dedicated Python 3.13 research environment instead
of modifying the base environment. The setup shape below must be smoke-tested
and lock-recorded before use; it is not a Pi package dependency install:

~~~
conda create -n pi-qwen3-embed python=3.13 -y
conda run -n pi-qwen3-embed python -m pip install --upgrade pip
conda run -n pi-qwen3-embed python -m pip install \
  "mlx-embeddings==0.1.0" \
  "transformers[sentencepiece]>=5.10.0"
~~~

Do not use mlx-lm server as the embedding endpoint. Its supported public API is
text/chat completion, not embeddings. The mlx-embeddings package supports the
required Qwen3 padded causal attention, last-token pooling, and normalized
batches, but it is GPL-3.0. Keep it as an external local research sidecar unless
a dependency-license review explicitly approves including it in Pi distribution.

Download once with huggingface_hub.snapshot_download at the pinned revision,
verify every file hash, and load only the local snapshot. Do not let load resolve
an unpinned model repository at runtime. The sidecar records repository,
revision, file hashes, dependency lock, dimension, normalization, and query
template version.

Its small application-owned contract is:

~~~json
POST /v1/embeddings
{
  "input": ["text A", "text B"],
  "max_length": 2048
}
~~~

~~~json
{
  "data": [{"index": 0, "embedding": [0.0]}],
  "dimension": 1024,
  "normalized": true,
  "model_id": "mlx-community/Qwen3-Embedding-0.6B-4bit-DWQ",
  "model_revision": "6c3ae70858513f1a78e9cdca3cae330d9075cd2a",
  "manifest_sha256": "..."
}
~~~

Task documents are embedded as task text. Query documents use this frozen
template:

~~~
Instruct: Retrieve SWE-bench tasks whose affected behavior is relevant to a
coding-agent evolution and its observed failure mode.
Query: <candidate-change summary + parent bad-case diagnosis>
~~~

Every embedding-cache key includes full text, role, template revision, maximum
length, model revision, and sidecar manifest hash.

## 7. Immutable manifests, pairing, and decision

### 7.1 Selection manifest

Each run writes one append-only selection-manifest.json containing:

~~~
schema_version, run_id, parent_artifact_hash, child_artifact_hash,
dataset_manifest_hash, catalogue_hash, change_hash, config_hash,
selector_model_revision, embedding_manifest_hash,
rounds[{queries, tool_calls, candidates, proposals, rationales,
        coverage_gains, pair_result_hashes, stop_reason}],
pre_audit_task_ids, audit_seed_derivation, audit_candidate_ids,
audit_task_ids, final_task_ids, coverage, redundancy, manifest_hash
~~~

The audit seed derives deterministically from a pre-registered experiment seed,
parent hash, child hash, and catalogue hash. Sampling happens after the
non-audit set freezes and before any audit execution. The selector never sees
or chooses audit IDs.

Persist raw selector responses, parsed tool calls, candidates, embedding/cache
hashes, token/cost/latency, exceptions, and validation failures. Use atomic
write and content hashes following the existing rollback_mvp state pattern.

### 7.2 Paired execution

For each frozen task ID, execute parent and child with the same task input and
base commit, model revision/inference settings, time/token/retry/tool budgets,
runner/evaluator image, and container policy. Use a fresh workspace and no
shared mutable agent state. Counterbalance parent/child order by deterministic
hash to reduce provider or queue drift.

A cache hit is valid only when its execution identity contains all of the above
plus the exact artifact hash. Incomplete, duplicate, or cross-identity pairs are
errors, not failed tasks and not imputed zeros.

The final union freezes before CLM/ddmin probing. Parent, child, and every
counterfactual artifact must use precisely that plan. Otherwise a rollback
comparison would run different versions on different tests.

### 7.3 Three-state decision engine

The decision engine is deterministic and versioned. It consumes only complete
paired results and a pre-registered DecisionPolicy. It never calls an LLM.
Required policy values include confidence level, bootstrap seed/count,
acceptance margin, rollback margin, audit guard, and escalation cap. There are
no magic in-code thresholds.

Let delta be child minus parent task success on the final union. Record
child-only wins, parent-only wins, ties, paired bootstrap interval, and exact
McNemar/binomial result over discordant pairs. Then:

~~~
ACCEPT    lower bound for delta clears the acceptance margin
          and the independent audit guard passes.
ROLLBACK  upper bound for delta is at or below the rollback margin.
ESCALATE  otherwise; hold the child and create a separately bounded expansion
          request instead of accepting or destroying it automatically.
INVALID   manifest, identity, or paired-evidence validation failed.
~~~

INVALID fails closed and is a controller error, not a scientific outcome.
ESCALATE is also appropriate when targeted evidence and audit evidence disagree.
A new escalation has a new immutable manifest and cannot edit the old one.

Selected tasks are adaptive, so these statistics support an operational
accept/rollback gate rather than an unqualified confidence interval for all
200 tasks. Audit and the endpoint protocol in Section 2.3 are separate
scientific controls.

## 8. Current-code feasibility and boundary

This MVP requires no Pi-core change. Implement it as an independent fail-closed
controller, not as a normal extension hook or a static Vitest task table.

| Existing area | Reuse |
| --- | --- |
| rollback_mvp/orchestrate_endpoint_200.py | Atomic state/hash helpers, task materialization, Docker task execution, official grading, resume state, and paired statistics |
| rollback_mvp/pi_swe_runner.mjs | Existing Pi trajectory, token, and tool telemetry format; replace host-Pi execution only in full-scope stage |
| rollback_mvp/dgm_budgeted_quarantine.py | Parent/child gained-lost task accounting pattern |
| packages/coding-agent/src/core/extensions/types.ts | SDK custom-tool/state interfaces for selector-facing evidence |
| packages/evals | Stable input identities, paired evaluation/reporting, and artifacts |
| pi-rollback/src/replay.ts and pi-rollback/src/diagnosis.ts | Checkpoint, replay, repair-ddmin, and diagnostic-evidence patterns |

Add these controller modules under rollback_mvp/adaptive_eval:

~~~
schemas.py            catalogue.py          trajectory.py
diagnosis.py          retrieval.py          embedding_client.py
coverage.py           selector_agent.py     audit_sampler.py
paired_executor.py    decision.py           state.py
reporter.py           cli.py
~~~

MVP deliberately starts without real candidate self-modification. It first
proves catalogue, retrieval, manifest, independent audit, pair identity, and
decision semantics offline. The containerized full-Pi runner follows only after
those deterministic components pass. This avoids allowing a mutable candidate
to be the first implementation path for its own evaluator.

## 9. Milestones and acceptance criteria

### Milestone 1: deterministic offline foundation

- Implement schemas, catalogue validation, lexical index, embedding-client
  contract, cache keys, coverage, redundancy, and deterministic audit sampling.
- Test with fake embedding client and fake evaluator only; make no external API
  call.
- Persist selected IDs, retrieval rank/source, similarity, coverage gain, hash,
  and exception.
- Require wrong dataset hashes, duplicate IDs, malformed manifests,
  non-normalized/wrong-dimension vectors, and missing sidecar metadata to fail
  closed.
- Require same input and seed to reproduce audit IDs and manifest hashes.

### Milestone 2: selector API loop

- Define a top-level selector-client abstraction and scripted fake for tests.
- Implement frozen tool schema and append-only multi-round state.
- Add direct model-API adapter only after tests cover malformed JSON, unknown
  tool calls, budget exhaustion, and declared stop behavior.
- Require every selected non-audit task to have role, evidence reference, and
  rationale. Do not expose a scalar route-weight configuration.

### Milestone 3: paired executor and decision

- Adapt current runner behind parent/child artifact interface.
- Implement identities, counterbalancing, complete-pair validation, statistics,
  reports, and ACCEPT/ROLLBACK/ESCALATE state machine.
- Reject a counterfactual with a different frozen task plan.
- Verify audit sampling is independent of selector output.

### Milestone 4: full DGM-scope candidate isolation

- Run the full candidate Pi process inside a container with narrow model proxy,
  immutable controller/evaluator mounts, path allowlists, resource bounds, and
  no unrestricted host/network access.
- Verify an evolved tool/extension cannot execute in the host Pi process, modify
  controller/evaluator/task-gold data, obtain model credentials, or call an
  arbitrary network destination.

Every experimental loop uses tqdm in terminal output and persists full
trajectory, configuration, budget, intermediate result, exception, and decision
artifacts. Real API or embedding failures remain visible and terminal; no silent
fallback is permitted.

## 10. Ablations and reporting

Use one frozen task universe, mutation proposer, model configuration, budget,
and final endpoint protocol. Compare:

- Fixed DGM-style subset.
- Lexical-only retrieval as an explicitly configured ablation.
- One-shot selector without iterative feedback.
- Agentic selector without facility-location completion.
- Agentic selector without independent audit.
- Full method.

Report task IDs per round, role counts, task-source ranks, coverage, redundancy,
per-repository distribution, audit outcomes, parent/child contingency counts,
retrieval/execution tokens, cost, latency, escalation rate, and final all-task
or held-out endpoint separately. Do not present the adaptive selected subset as
an unbiased 200-task score.

### 10.1 Facility-location ablation pre-registration and current evidence

The facility-location arm changes only `coverage_selection_mode`; selector
model, prompts other than the declared mode, task universe, budgets, and
candidate evidence remain frozen.

Predictions:

- If direct proposals exactly fill round capacity, `greedy` and `agent_only`
  select identical task IDs.
- If proposals exceed capacity, the modes may differ because only `greedy`
  reorders by marginal coverage.
- If proposals underfill capacity, `agent_only` executes fewer paired tasks;
  selector tokens are unchanged for a fixed action trace.

Kill criteria:

- Any task-ID difference in the exact-capacity replay means the ablation is not
  isolated.
- Do not remove facility-location completion if underfilled real rounds save
  less than 20% execution cost, or if the held-out/reference endpoint shows
  materially worse regret or false-accept behavior.

The deterministic mechanism replay at
`research_output/adaptive_eval_coverage_ablation_20261014/` passes the isolation
check. Its under-capacity toy case selects one planned task instead of two,
while selector traces and token counts remain unchanged. This is not endpoint
evidence: no real selector API, paired SWE-bench execution, wall-time
measurement, or quality measurement was run.

## 11. Non-goals

- No RL, reward model, or learned route-weight policy.
- No silent lexical fallback when the embedding sidecar is unavailable.
- No model-selected random audit.
- No child-specific test plan in a parent/child comparison.
- No private evaluator feedback in selector prompts.
- No host execution of arbitrary evolved Pi code.
- No claim that the controller alone reproduces DGM's endpoint or establishes
  generalization beyond its declared final protocol.

## 12. Primary sources

- DGM paper: paper_ref/DGM.pdf and https://arxiv.org/abs/2505.22954
- Qwen model card: https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
- Pinned MLX conversion: https://huggingface.co/mlx-community/Qwen3-Embedding-0.6B-4bit-DWQ
- MLX embeddings implementation: https://github.com/Blaizzy/mlx-embeddings
- MLX LM server scope: https://github.com/ml-explore/mlx-lm
