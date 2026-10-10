# Cold-Start Dynamic Sampling 60/140 Experiment Protocol

> **Status: DESIGN ONLY.** No model call, Docker execution, embedding request,
> SWE-bench task execution, or paid evaluation is authorized by this document.
> It is a pre-registration and handoff runbook for a later, isolated run.
>
> **Scope:** strategy/workflow-level Pi evolution only. The mutable candidate is
> a single strategy.md artifact. This is not a full Pi source-level
> reproduction of DGM.

This protocol operationalizes the controller design in
[AGENTIC_ADAPTIVE_EVALUATION_DESIGN.md](AGENTIC_ADAPTIVE_EVALUATION_DESIGN.md).
It is deliberately stricter about cold-start isolation, a 60/140 split, and
all-in cost accounting. It does not replace that design document.

The labels A0 through A3 below are **evaluation-controller ablations**. They
must not be called B0 through B3: those labels already refer to different
rollback-policy baselines in
[EVOLUTION_ROLLBACK_DIRECTION.md](EVOLUTION_ROLLBACK_DIRECTION.md).

## 1. Purpose And Claim Boundary

The proposed method changes the *control plane* of DGM-style evolution:

1. It selects mutation-specific tasks instead of using a fixed evaluation panel.
2. It runs the parent and child on the same frozen task union before deciding
   whether to retain the child.
3. It adds a controller-private residual audit and a deterministic
   ACCEPT/REJECT/ESCALATE edge decision; Phase 2 adds true lineage rollback.

It does not directly make a fixed coding agent solve more tasks. Any endpoint
gain must arise through a better sequence of retained and rejected mutations.
Accordingly, the primary comparison is between the **final frozen agents**
produced by two full searches, not between scores from an adaptively selected
batch.

For an edge P_t -> C_t, the parent is a counterfactual reference, not a second
deployable candidate. Do not add score(P_t) and score(C_t), and do not compare
that sum with a fixed-panel score.

The protocol has two distinct evidence levels:

- **Evaluator evidence:** Does dynamic paired sampling make better
  ACCEPT/REJECT/ESCALATE decisions for a frozen set of candidate edges?
- **Search evidence:** At equal all-in resources, does the dynamic control
  plane produce a better final frozen strategy artifact, or reach a fixed
  endpoint target with lower all-in cost?

The dynamic selected-task score is an operational gate signal. It is not an
unbiased estimate of benchmark-wide agent capability.

## 2. Terminology

| Term | Meaning |
| --- | --- |
| H0 | Immutable initial Pi harness snapshot. It includes the approved initial source/package identity, runner, model configuration, execution policy, and the hash-attested immutable dynamic-sampling/rollback control-plane release. The control plane is part of the execution identity but outside the mutable artifact hash domain. |
| P0 | H0 plus the frozen initial strategy.md artifact. It is the first parent. |
| P_t | The current frozen parent artifact before mutation t. |
| C_t | The frozen child artifact proposed from P_t by exactly one mutation. |
| edge P_t -> C_t | One candidate mutation to be evaluated and either retained, rejected, or escalated. |
| D_evolve | The 60 tasks allowed to influence online mutation, sampling, audit, and archive decisions. |
| D_audit | A controller-private deterministic residual audit sampled from unselected D_evolve tasks after selector termination. It is conditionally random only within that residual pool, not an unconditional sample of all 60 tasks. |
| D_test | The 140 held-out tasks that must not influence any online decision. |
| C_search(A, s) | All costs for arm A and matched evolution seed s incurred before the final held-out endpoint. |
| C_total(A, s) | Arm A's C_search plus its one-time locked 140-task endpoint cost for matched evolution seed s. |
| C_reference(s) | The separately reported shared P0 reference-endpoint cost for matched block s. It is not silently assigned to only one arm. |
| C_descriptive_200_extra_60(A, s) | The separately reported optional cost of the new 60-task no-feedback supplement used to compose a descriptive 200-task result. |

P_t must be evaluated before the decision for its edge, not only after a
rollback is suspected. A parent result may be reused only when the complete
execution identity matches exactly. The original parent execution cost remains
part of C_total(A, s).

The primary cost estimand is reported model tokens:
input, output, cache-read, and cache-write tokens. Dollar cost, API calls,
agent wall time, task runtime, image-build time, and local embedding CPU/GPU
seconds are required secondary cost columns. They are not converted into one
unjustified scalar.

## 3. Research Questions And Falsifiable Claims

The following hypotheses must be locked before the confirmatory search. They
are intentionally separated so a quality/cost trade-off is not mislabeled as a
double improvement.

| ID | Hypothesis |
| --- | --- |
| H1 discrimination | On the same frozen candidate bank, A2 dynamic paired evaluation has lower decision regret against the locked full-D_evolve reference execution than A1 fixed paired evaluation. |
| H2 safety | On the same frozen candidate bank, A2 has a lower false-accept rate than A1 for children materially worse in the locked full-D_evolve reference execution. |
| H3 rollback | In a pre-registered multi-generation toxic-lineage experiment, the full method identifies the rollback target more accurately and restores independent downstream value at lower cost. |
| H4 endpoint quality | Conditional on the Phase 2 A3 release gate, under the same pre-reserved resource budgets A3 has a higher mean final D_test solve rate than A0. |
| H5 fixed-budget efficiency | Conditional on the Phase 2 A3 release gate, A3 has lower realized primary token cost than A0 by at least gamma while meeting the locked endpoint non-inferiority criterion. |

For one edge, define:

~~~text
Y_r(v, task) in {0, 1}               artifact v solves task in locked rollout r
Y_bar(v, task) = locked aggregation over task rollouts
Delta_e(task) = Y_bar(C_t, task) - Y_bar(P_t, task)
Delta_e_reference = mean over task in D_evolve of Delta_e(task)

ACCEPT_ref   if Delta_e_reference >= delta_plus
REJECT_ref   if Delta_e_reference <= delta_minus
ESCALATE_ref otherwise
~~~

The locked full-D_evolve reference execution is an operational comparison
target, not a noise-free ground-truth oracle. If task_rollout_count is one,
the reference labels above mean agreement with that one identity-bound
execution. A rollback oracle exists only in the separately isolated Phase 2
toxic-lineage fixture.

delta_plus, delta_minus, the audit guard, confidence level, bootstrap
settings, endpoint non-inferiority margin m_NI, optional quality target Q_star,
and minimum claimed cost saving gamma are required protocol-lock values. They
may be calibrated only from the Phase 1 pilot, then must be hash-locked before
the Phase 1b confirmation bank is generated or any of its outcome is visible.
They must not be changed after a Phase 1b confirmation result or any D_test
result is visible.

The phrase **"higher performance and lower token cost"** is permitted only if
both conditions hold:

1. The pre-registered one-sided inference for
   mean_s[Q(A3, s; D_test) - Q(A0, s; D_test)] supports superiority.
2. The pre-registered one-sided inference for
   mean_s[C_total(A3, s) - C_total(A0, s)] is less than -gamma.

If A3 is only non-inferior and costs less, use the narrower statement
"non-inferior endpoint quality at lower primary token cost." If only one
condition holds, report a quality/cost trade-off. Do not describe the
adaptively selected batch solve rate as the endpoint result.

An optional quality-cost frontier requires a separate, pre-registered grid of
independent search-budget cells. Each cell runs a complete search without
seeing D_test, then evaluates its final artifact once. D_test outcomes must
remain sealed until every budget cell is complete. A single search with one
locked endpoint cannot estimate the cost at which it first reached Q_star.

## 4. Frozen Dataset Contract

The fixed source is:

~~~text
DGM repository commit:
682eb38a3eb232f4396924cacd0a083bf1444cf8

SWE-bench Verified:
princeton-nlp/SWE-bench_Verified, test split,
revision c104f840cc67f8b6eec6f759ebc8b2693d585d4a

Frozen manifest:
research_output/clm_budgeted_evolution_20260924_125503/
  dgm_swebench_verified_200.v1.json

Full manifest SHA-256:
3fb913fbc73a05c1f7cae3b708c976374632820b58377aab5de08b742f96c967

Ordered task-ID SHA-256:
421c950302366954005dab020cdc89ca0d6ae1f0423e2b662637f7790a31d0d7
~~~

The DGM partitions are disjoint and must retain their literal membership:

| Partition | Size | SHA-256 | Role |
| --- | ---: | --- | --- |
| small | 10 | b8909d87321bf7e9277e82baff8b2a739a3e1e76585ec512ae8ad4b6eef86591 | Initial fixed screen |
| medium | 50 | bf1cde9b2590f7813cc0cbb43a3ce0a9fccbdd163083891ff96b9abc82e4c06f | Additional evolution tasks |
| big | 140 | 76a8b81f0c044a64c928ab46312b5eb69c3728ab7d39c4fe6239a790797906cd | Held-out endpoint |

~~~text
D_evolve = small union medium = 60 tasks
D_test   = big = 140 tasks
~~~

The fixed control is called **DGM-compatible**, not an exact replay of DGM's
public implementation. The paper describes cumulative 10 -> 60 -> 200
staging, while locally available historical runners/artifacts do not establish
an executable, byte-for-byte equivalent 140-stage implementation.

### 4.1 Access Rules

| Component | D_evolve | D_test | Gold/test patches and grader-private output |
| --- | --- | --- | --- |
| Candidate strategy artifact | Selected task input only | Never | Never |
| Mutation proposer | Public D_evolve evidence only | Never | Never |
| Selector and audit controller | D_evolve operational catalogue only | Never | Never |
| Embedding sidecar/index for evolution | D_evolve only | Never | Never |
| Archive and parent-selection logic | Sanitized D_evolve evidence only | Never | Never |
| Rollback diagnoser and replay policy (A3 only) | Sanitized public D_evolve lineage evidence only | Never | Never |
| Locked endpoint executor | After final freeze only | Yes, once | Outside evaluator only |
| Human analysis during search | Protocol/health metadata only | No outcomes | Never |

The strategy artifact, selector, mutation proposer, archive process, and
search workers never receive D_test. A separate locked endpoint worker may
receive one current D_test task's public input only after the final artifact is
frozen. It must not return task cards, trajectories, patches, or outcomes to
any search or mutation component.

The implementation must create and hash-bind three explicit manifests:

~~~text
evolve-60-manifest.json
test-140-manifest.json
split-binding.json
~~~

split-binding.json must contain the full-manifest hash, all three partition
hashes, the two role manifests, their ordered ID hashes, and a declaration that
no D_test row, ID, issue text, embedding, or task result is mounted into an
online worker.

The current adaptive_eval implementation exposes a complete 200-task catalogue
to the selector, audit pool, and coverage universe. It therefore does **not**
satisfy this split yet. A role-filtered operational catalogue and zero-visibility
D_test boundary are mandatory implementation gates, not optional refinements.

### 4.2 Freshness Limitation

The new framework can be isolated from all prior DGM-200 output. However, this
checkout already contains partial DGM-200 execution and human analysis. The
140-task endpoint is isolated from the *new search*, but it is not a
project-wide newly discovered benchmark. Report it as an isolated endpoint for
this protocol, not as proof of unseen-benchmark generalization.

If a publishable generalization claim is needed, add a separately frozen
external benchmark that has never appeared in a run, prompt, repair artifact,
failure card, or human analysis.

## 5. Cold-Start And Information-Isolation Rules

This experiment must begin only after every currently running experiment has
reached its normal terminal state, its process has exited, and its output root
has been frozen read-only. Do not pause, resume, modify, or reuse an active
experiment for this protocol. Early termination is allowed only after explicit
user authorization and must be recorded as a protocol deviation.

### 5.1 Mandatory Readiness Attestation

Before creating any candidate, write a cold-start-attestation.json with:

- initial_harness_git_sha, explicitly approved by the experiment owner.
- A separate immutable control-plane release manifest for the latest dynamic
  sampler and rollback code. The control plane is versioned and hash-attested,
  is part of H0's execution identity, but is not part of the mutable candidate
  artifact.
- Pi package/shrinkwrap hash, runner hash, model configuration hash, evaluator
  hash, and image digest or image-build identity.
- Exact baseline strategy.md content hash and a declaration of whether the
  baseline is empty.
- The full/split manifest hashes from Section 4.
- The clean-checkout absolute path, approved base SHA, clean-status hash, and
  a statement that the new candidate root was created from that checkout rather
  than the current dirty working tree or a historical task workspace. If an
  immutable patch is necessary, it must have a separately approved content hash
  and be applied only to that clean checkout.
- A runtime-generated denylist containing every historical experiment root,
  its sealed content hash, terminal state, and exited process identity, plus a
  successful mount/read-access audit. Inability to attest any of these is a
  readiness failure, not an optional missing field.

There is no pre-existing strategy.md in this repository. Create P0 as a new
immutable directory only after the baseline is approved:

~~~text
artifacts/P0/
  strategy.md
artifact-records/<p0-artifact-hash>.json
~~~

Do not infer P0 from a task result, an empty strategyHash in prior output, or a
current workspace state.

### 5.2 Historical Output Denylist

The following data is forbidden as candidate input, cache evidence, selector
evidence, mutation context, embedding input, or control-arm evidence. This is
the initial static denylist; Phase 0 extends it with every prior experiment
root discovered at runtime.

~~~text
research_output/clm_budgeted_evolution_20260924_125503/dgm200_run/**
research_output/clm_budgeted_evolution_20260924_125503/endpoint_runs/**
research_output/clm_budgeted_evolution_20260924_125503/rf_clm_*
rollback_mvp/outputs/** when it contains task outcomes or evaluator feedback
~~~

In particular, do not reuse prior trace.jsonl, result.json, failure_evidence.md,
recovery results, feedback probes, official evaluator logs, token results, or
checkpoints. The existing run lacks the frozen parent/child artifact identities
and paired execution identities required here; some recovery artifacts also
contain forbidden official evaluator feedback.

The new workers must use allowlist mounts. The candidate must receive only its
artifact, the selected public task input, and the permitted immutable runtime.
It must not mount the controller source, evaluator source, Docker socket, API
credentials, full benchmark records, or any historical output root.

After Phase 1 seals, its candidate-bank artifacts, reference-execution
observations, decision labels, trajectories, case-study evidence, and human
selection notes are added to this denylist for every later mutation worker,
search worker, selector, archive process, rollback diagnoser/replay worker,
and human final-candidate review. They may be read only by the isolated
analysis process that produces the Phase 1 report. They must not become a
source of new bad-case cards or prompt edits.

### 5.3 Model And API Isolation

Use only an environment-injected credential. Never read, copy, or parse the
literal credentials present in llm_api_samples/.

If using the approved deployment, record:

~~~text
provider identity
model ID: byteplus/deepseek-v4-flash-ga
endpoint/proxy identity
any provider-supplied revision identifier
temperature, top-p, max output tokens, retry policy
request hash, response hash, token telemetry, and latency
~~~

If the provider does not expose a reproducible sampling seed or revision,
record that limitation. An experiment seed can reproduce controller
randomization and task ordering, not necessarily model outputs bit-for-bit.

The protocol lock must specify a separate model setting block for each role:

~~~text
Pi task agent
mutation proposer
dynamic selector
rollback diagnoser, if Phase 2 is enabled
locked endpoint task agent
~~~

Each block records provider, model, endpoint/proxy identity, available revision,
temperature, top-p, output cap, retry policy, and request schema. All arms use
the same block for a given role. If every role uses
byteplus/deepseek-v4-flash-ga, that fact must be explicit rather than implied.

For the planned DeepSeek run, byteplus/deepseek-v4-flash-ga is the approved
model ID for every LLM role unless the experiment owner revises the protocol
lock before paid work. A role-specific deviation is a new protocol version, not
a runtime fallback, and must be applied identically to every compared arm that
uses that role.

The lock also defines task_rollout_count, pair aggregation, and retry
classification. If it specifies one rollout, the full D_evolve result is a
"locked reference execution" rather than a noise-free oracle. Only
infrastructure retries allowed by the frozen retry policy may repeat a task;
model failures are not silently retried as fresh samples. Every repeat counts
in the all-in ledger.

## 6. Strategy-Artifact Mutation Boundary

The MVP is deliberately narrower than full DGM source self-modification.
Every candidate artifact has exactly this mutable surface:

~~~text
artifact/
  strategy.md
~~~

Only strategy.md may differ between a parent and its child. The child may not
modify:

- Pi source, tools, extensions, package dependencies, runner, model
  configuration, container policy, controller, selector, evaluator, task
  manifests, embedding index, archive policy, or rollback policy.
- Task-specific patches, explicit task IDs, gold patch content, test patch
  content, grader-private text, credentials, network instructions, or
  benchmark-specific hardcoding.

For each edge, persist a CandidateChangeCard containing at least:

~~~text
parent_artifact_hash
child_artifact_hash
source_tree_hash for P_t and C_t
source_diff_hash
changed_paths = ["strategy.md"]
mutation_summary
source_revision
created_at
mutation prompt/request/response hashes
~~~

Candidate-specific provenance is stored in an immutable sidecar outside the
artifact tree, for example artifact-records/<artifact-hash>.json. The artifact
hash domain is exactly the strategy.md file and its normalized path. This
avoids changing source_tree_hash or source_diff_hash through timestamps,
parent pointers, or other metadata while preserving the invariant that
changed_paths equals ["strategy.md"].

Any symlink, extra file, missing metadata, malformed strategy, scope breach,
or hash mismatch is INVALID. It does not become a heuristic fallback, failed
task, or zero-score candidate.

The mutation proposer may see only public selected D_evolve task cards, the
current parent strategy, sanitized public trajectory/tool output, and
sanitized paired evidence allowed by the protocol lock. It may not see D_test,
official grading details, gold/test patches, other arms' private evidence, or
future descendant results.

The A3 rollback diagnoser may see only the frozen, sanitized public D_evolve
lineage evidence named by its diagnosis schema: artifact/edge identities,
allowed change-card fields, allowed public trajectory summaries, and allowed
paired observations. It may not see D_test, official grading details, gold/test
patches, historical feedback-assisted output, the hidden toxic-lineage oracle,
or evidence from another arm. Its prompt, tool allowlist, and evidence-schema
hash are part of the A3 protocol lock.

## 7. Controller Ablations

All arms start from an identical P0. They must use the same immutable harness,
model configuration, mutation proposer prompt, candidate scope, per-task
limits, retry policy, task image/evaluator identity, task-order
counterbalancing rule, shared archive-interface/parent-selection rule, mutation limit, and
separately pre-reserved search and endpoint resource ceilings.

| Arm | Task allocation | Parent/child execution | Lineage policy | Purpose |
| --- | --- | --- | --- | --- |
| A0 fixed unpaired | DGM-compatible fixed 10 -> 60 evolution panel | Child-focused evaluation; no per-edge parent rerun | Fixed promotion/archive policy; no dynamic sampling or diagnostic rollback | Headline fixed-policy control |
| A1 fixed paired | Same fixed panels as A0 | Matched P/C execution on the fixed panel | Deterministic binary ACCEPT/REJECT only; no dynamic selection, escalation, or lineage rollback | Isolates parent-evaluation cost and value |
| A2 dynamic paired | Selector chooses from D_evolve, then residual audit | Matched P/C execution on a frozen union | Edge-local ACCEPT/REJECT/ESCALATE only; it never revisits a prior accepted ancestor | Isolates dynamic sampling value |
| A3 full rollback | Dynamic selection plus residual audit | Matched P/C execution on a frozen union | Adds lineage diagnosis, ancestor rollback, and pre-registered replay after a later toxic-edge signal | Separates multigeneration rollback value |

A0 is a DGM-compatible fixed-policy control, not a claim to reproduce DGM's
original code, models, archive implementation, or private-feedback diagnosis
prompt.

For A1 and A2, REJECT means edge-local rejection: C_t is preserved as an audit
artifact but P_t remains the current parent. It is not called rollback.

A3 is not executable during the single-edge MVP. It becomes a distinct arm
only after Phase 2 implements a lineage diagnosis state machine. If it
diagnoses bad edge e_j: P_(j-1) -> P_j, its restore state is exactly
P_(j-1), not P_j; P_j and its descendant status are then governed by a frozen
invalidation/replay policy. Until that gate passes, Phase 1 reports A0, A1,
and A2 only.

### 7.1 Fixed-Policy Algorithm For A0 And A1

The fixed controls must use a deterministic policy file, not a prose
placeholder. Their stage state machines are:

~~~text
A0 for each proposed child C_t:
    run the fixed D_small=10 screen for C_t
    if basic_edit_gate(C_t, D_small) is false:
        emit REJECT; do not promote C_t
    else:
        run the fixed additional D_medium=50 panel for C_t
        compute score_60(C_t) from the cumulative 60 observations
        apply a0_score_60_eligibility_rule(C_t, score_60)
        if eligible, emit ACCEPT and insert the common ArchiveEntry(C_t)
        else emit REJECT

A1 for each proposed edge P_t -> C_t:
    run matched P_t/C_t executions on the fixed D_small=10 screen
    apply a1_small_screen_rule(P_t, C_t, D_small)
    if the result is REJECT:
        emit REJECT; do not promote the edge
    if the result is PROMOTE:
        run matched P_t/C_t executions on all fixed D_medium=50 tasks
        apply a1_final_60_decision(P_t, C_t, D_small union D_medium)
        emit exactly ACCEPT or REJECT
        if ACCEPT, emit the common ArchiveEntry(C_t)

select later parents only through the common archive interface over eligible
ArchiveEntry records; do not require score_60 from non-fixed arms.
~~~

The A0/A1 fixed policy and the all-arm common archive interface must be a
separately validated, hash-bound file at frozen-inputs/fixed-policy.json. The
following is its minimum schema. The illustrative placeholders are invalid final
values: every field must contain a concrete owner-approved value before a paid
run.

~~~json
{
  "schema_version": "owner-approved",
  "small_panel": {
    "ordered_task_ids_sha256": "b8909d...",
    "task_order_rule": "owner-approved deterministic rule"
  },
  "medium_panel": {
    "ordered_task_ids_sha256": "bf1cde...",
    "task_order_rule": "owner-approved deterministic rule"
  },
  "basic_edit_gate": {
    "applies_to": "A0 only",
    "observations": "owner-approved panel and rollout aggregation",
    "comparator": "owner-approved comparator",
    "threshold": "owner-approved numeric value",
    "minimum_complete_tasks": "owner-approved numeric value"
  },
  "a0_score_60_eligibility_rule": {
    "applies_to": "A0 score_60 insertion only",
    "score_60_definition": "owner-approved exact formula",
    "eligibility": "owner-approved predicate"
  },
  "common_archive_lifecycle": {
    "applies_to": "every accepted ArchiveEntry in A0/A1/A2/A3",
    "capacity": "owner-approved numeric value or explicit unbounded state",
    "eviction_rule": "owner-approved deterministic rule over common ArchiveEntry fields",
    "accepted_entry_insertion_rule": "must retain the new accepted entry or deterministically evict another entry"
  },
  "parent_selection": {
    "eligible_set": "owner-approved predicate over common ArchiveEntry fields",
    "weight_transform": "owner-approved exact formula over common ArchiveEntry fields",
    "sampling_with_replacement": "owner-approved boolean",
    "seed_derivation": "owner-approved deterministic derivation",
    "draws_per_wave": "owner-approved numeric value"
  },
  "wave_schedule": {
    "max_waves": "owner-approved numeric value",
    "proposals_per_parent": "owner-approved numeric value",
    "proposal_slot_order": "owner-approved deterministic rule",
    "tie_breaker": "owner-approved total ordering"
  },
  "invalid_handling": {
    "invalid_child_scope_or_schema": "frozen terminal action",
    "invalid_task_or_pair": "frozen terminal action",
    "replacement_slot_rule": "owner-approved fixed rule"
  },
  "descendant_eligibility": {
    "accepted_child_may_be_parent": "owner-approved boolean/predicate",
    "required_archive_state": "owner-approved state"
  },
  "a1_fixed_stage_policy": {
    "small_screen_rule": "owner-approved paired formula producing PROMOTE or REJECT",
    "medium_execution_rule": "run matched P/C on all 50 fixed medium tasks after PROMOTE",
    "final_60_decision": "owner-approved paired formula producing ACCEPT or REJECT",
    "stage_transition_and_terminal_actions": ["PROMOTE", "REJECT", "ACCEPT"]
  },
  "final_artifact_selection": {
    "rule": "owner-approved deterministic rule over common ArchiveEntry fields"
  }
}
~~~

This schema fixes the basic edit gate, archive eligibility/lifecycle, exact parent
selection rule, parent draws/proposals per wave, task ordering and tie-breaking,
invalid-child handling, and descendant eligibility. No run may substitute a
threshold, archive rule, replacement rule, or parent-selection rule after
outcomes are visible. Missing, malformed, or hash-mismatched fixed-policy.json
blocks the paid run.

For A1, P_t and C_t run the same fixed panel at each promoted stage. A1 never
calls the dynamic selector and has no ESCALATE path: its 10-task rule can only
REJECT or PROMOTE, and its 60-task rule must terminate in ACCEPT or REJECT
using only fixed-panel observations. A1's common ArchiveEntry is emitted only
after final ACCEPT.

### 7.2 Shared Archive Interface

Every arm writes the same normalized ArchiveEntry after an accepted child and
then applies the same capacity/eviction lifecycle:

~~~text
artifact hash
parent artifact hash
lineage depth
accepted terminal action
insertion ordinal
creation/event hashes
immutable execution-identity hashes
~~~

The shared parent-selection and final-artifact rules may use only these common
fields. They may not use score_60, selected-set solve rate, selector rationale,
paired margin, arm label, or any other arm-specific quality signal. A0/A1 may
use score_60 or their fixed paired formula only to decide whether to insert a
child; A2/A3 use their frozen decision action for that same eligibility step.
This preserves a common archive interface while leaving task allocation and
evaluator evidence as the ablated control-plane difference.

The common lifecycle's capacity and eviction rule may use only common
ArchiveEntry fields and must not reject the newly accepted child merely because
the archive is full: it retains that entry or deterministically evicts another
entry. The exact eligible predicate, weight transform, parent draw count,
tie-breaker, lifecycle, and final-artifact rule are fields of the hash-bound
policy. If no eligible entry exists, the rule must deterministically specify
whether P0 is selected or the arm is invalid; it may not use human inspection.

### 7.3 Candidate-Bank Requirement

In the evaluator pilot, generate and freeze all P0 -> C_i strategy artifacts
before any evaluation outcome is visible. Every arm then evaluates the same
candidate bank. This separates evaluator effects from proposer effects.

In a live search, arms will necessarily diverge after different
accept/reject/rollback decisions. The statistical unit is then the independent
evolution seed, not an individual task or edge.

## 8. Dynamic Pairing Procedure

For each P_t -> C_t edge in A2 or A3:

1. Freeze the controller request with the D_evolve catalogue identity,
   parent/child hashes, change card, eligible public parent bad cases, model
   identities, and every explicit budget.
2. The selector uses only frozen read-only tools for lexical retrieval,
   semantic retrieval, task cards, parent evidence, the change card, coverage,
   and sanitized prior-round summaries.
3. Before executing a round, append a hash-chained, immutable round manifest
   with the exact selected IDs and rationales.
4. Run P_t and C_t on exactly those IDs with matched execution identities.
   Counterbalance P/C execution order by a frozen hash rule.
5. Append results; the selector may add tasks but may not modify earlier
   rounds.
6. Once the selector stops, derive the controller-private audit seed, sample
   the residual D_audit from the still-unselected D_evolve pool, reserve the
   pre-budgeted expansion capacity from the remaining non-audit IDs, and freeze
   the base task plan.
7. Run the required final identity-bound pair on the frozen union. A prior
   round result is reusable only if its full execution identity is equal to the
   final request; otherwise rerun it and account for both attempts.
8. Validate complete pairs and apply the frozen deterministic decision policy.
   Identity mismatch, incomplete telemetry, duplicate observations, invalid
   model metadata, or an invalid manifest terminates the edge as INVALID.

The selector must fail closed for malformed JSON/tool output, unknown or
duplicate IDs, absent evidence references, unauthorized tools, missing
embedding metadata, task-budget overflow, or selector-token/time overflow. It
must not substitute a heuristic batch or a lexical-only fallback.

The split-aware configuration must enforce:

~~~text
initial_selected_task_budget
+ max_cumulative_escalation_tasks
+ audit_size
<= 60

max_tasks_per_round <= initial_selected_task_budget
~~~

The selector may consume only initial_selected_task_budget before the residual
audit is frozen. A2 may later consume no more than
max_cumulative_escalation_tasks, only from the pre-reserved non-audit IDs. An
expansion writes a new immutable task plan; it can never displace an audit ID,
increase the total 60-task capacity, or reveal audit outcomes to the selector.

The residual audit is conditionally randomized within the remaining pool, but
it is not an unconditional random sample of all 60 tasks.
Report it as a residual-audit gap, not as a whole-population estimate.

### 8.1 Frozen Decision State Transitions

For A1 and A2, the common terminal actions are:

~~~text
ACCEPT:
    C_t becomes an eligible archive entry under the frozen archive rule.

REJECT:
    C_t is retained only as an immutable audit artifact.
    P_t remains the current parent; C_t produces no descendants.

~~~

For A2 only, ESCALATE creates a new immutable expansion manifest. It may append
only pre-budgeted, pre-reserved non-audit D_evolve tasks. The selector never
receives audit IDs or audit outcomes. Re-run the decision on the new manifest.
The expansion policy must define its exact task budget, allowed selector input,
maximum expansion attempts, and final terminal state before execution. A later
expansion may not alter the original manifest, exceed the cumulative expansion
cap, or reveal its residual-audit outcomes to the selector.

For A2 only:

~~~text
ESCALATE_EXHAUSTED:
    If the frozen expansion task/round cap is exhausted without ACCEPT or
    REJECT, C_t is not archived, P_t remains current, and the edge is
    reported as ABSTAIN/unresolved rather than coerced into a favorable action.
~~~

### 8.1.1 Cross-Arm Terminal-Action Mapping

Every scientifically valid edge must emit one metric action before candidate
bank analysis:

~~~text
A0 basic_edit_gate failure or score_60 eligibility rejection -> REJECT
A0 score_60 eligibility pass                                -> ACCEPT
A1 locked binary paired formula                         -> ACCEPT or REJECT
A2 terminal ACCEPT or REJECT                            -> same action
A2 ESCALATE_EXHAUSTED                                   -> ABSTAIN
~~~

Invalid/incomplete states in Section 13.1 are not scientific actions and are
reported separately under the locked invalid-block rule. For valid edges,
action-agreement and regret denominators include every ACCEPT, REJECT, and
ABSTAIN outcome; an ABSTAIN is never silently excluded. Its agreement mapping,
regret/utility penalty, and H1/H2 denominators must be locked in advance.
Specifically, ESCALATE_ref denotes the full-reference unresolved category;
ABSTAIN can agree only with ESCALATE_ref. False-accept rate is calculated over
valid REJECT_ref edges, false-reject rate over valid ACCEPT_ref edges, and the
valid-edge abstention rate is always reported alongside both.

### 8.2 A3 Lineage-Rollback State Machine

For A3, a separate Phase 2 state machine is required:

~~~text
late toxic-edge signal -> freeze lineage evidence -> diagnose one bad edge
e_j: P_(j-1) -> P_j -> restore state P_(j-1) -> invalidate P_j and classify
its descendants -> replay only descendants admitted by the frozen replay rule
-> write a new lineage manifest
~~~

The A3 policy must define the trigger schema, diagnosis evidence schema,
diagnoser prompt hash, unique-target rule, restore-state rule, descendant
invalidation rule, replay-admission predicate, and terminal action when no
unique bad edge can be identified. The latter is
ROLLBACK_TARGET_UNRESOLVED: freeze the lineage, do not choose an ancestor by
heuristic, and continue only as explicitly permitted by the locked policy.

No A3 result is valid until this state machine, its oracle fixture, and its
identity-bound replay executor are implemented, tested, and certified by the
Phase 2 release gate.

Every execution identity includes, at minimum:

~~~text
artifact hashes
task ID and base commit
provider/model/revision/inference settings
strategy and prompt revisions
runner and evaluator revisions
image/build identity
token/time/retry/tool budgets
container/host strategy-runner policy
task-plan and split-manifest hashes
~~~

## 9. Execution Phases

### Phase 0: Readiness And Sealing

1. Wait until every unrelated experiment reaches its normal terminal state,
   every related process has exited, and its output root is frozen read-only.
   Early termination requires explicit user authorization and a recorded
   protocol deviation with the job/process identity, reason, and authorization
   time.
2. Record the terminal-state attestation, archive the prior roots outside the
   new experiment root, and add them to the runtime denylist.
3. Create a clean checkout from the user-approved initial_harness_git_sha.
4. Create and hash P0; lock all runtime, model, prompt, split, seed, and
   budget configuration before paid work.
5. Complete non-paid validation of manifest/split binding, mount isolation,
   artifact snapshotting, identity binding, strict API schemas, ledger
   reconciliation, and no-private-feedback flow.
6. Do not start paid SWE-bench work until every readiness gate in Section 13
   passes.

### Phase 1: Frozen Candidate-Bank Evaluator Pilot

1. Generate a pre-registered candidate bank from P0 without exposing any
   evaluation outcome to the proposer.
2. Run A0, A1, and A2 over the same frozen edges. A3 is excluded until the
   Phase 2 release gate passes.
3. After all online decisions are sealed, run each frozen P/C pair on the full
   D_evolve=60 under the locked reference identity and rollout aggregation,
   only in an isolated analysis environment.
4. Compute reference-action agreement, false accepts, false rejects, escalation
   behavior, regret, audit gap, coverage, and all-in cost.
5. Use the pilot only to lock implementation, thresholds, and budget. A
   candidate bank used for tuning cannot be confirmation evidence.

### Phase 1b: Frozen Evaluator Confirmation Bank

1. Seal the Phase 1 policy, prompt, model, selector, embedding, budget, and
   decision configuration in a new hash-bound protocol lock. Do not use Phase 1
   evidence to choose a preferred candidate or mutate the later search.
2. With fresh mutation seeds, generate a second candidate bank whose P0 -> C_i
   artifacts have never appeared in Phase 1. Freeze the complete bank before
   any evaluation outcome is visible.
3. Evaluate that bank only with the already locked A0/A1/A2 evaluator policies.
   No threshold, budget, prompt, model, model setting, or selector change is
   permitted after a confirmation observation exists.
4. After its online decisions seal, run each confirmation P/C pair on the full
   D_evolve=60 locked reference execution in the isolated analysis environment.
5. A confirmation failure weakens or falsifies the evaluator claim; it cannot
   trigger retuning followed by a replacement confirmation run. If later Phase
   2 work changes any shared A0/A1/A2 evaluator implementation or identity,
   repeat Phase 1b with a new unused bank.

### Phase 2: Controlled Multi-Generation Rollback Pilot

Create a pre-registered lineage such as:

~~~text
P0 -> P1 -> toxic edge -> P3 -> P4
~~~

The toxic edge and true rollback point must be written into an oracle file that
the controller, selector, proposer, and candidate cannot read. Evaluate
rollback target accuracy, recovery cost, retention of independent downstream
gains, and toxic-edge recurrence. A single P0 -> C1 edge can test rejection,
but cannot test causal rollback to an ancestor.

The A3 release gate passes only when all of the following are implemented and
verified against the isolated fixture: multigeneration lineage diagnosis,
edge-to-predecessor restore, identity-bound descendant invalidation/replay, a
toxic-lineage oracle fixture, and an append-only lineage/ledger bridge. Write a
release certificate containing the tested fixture identity, implementation and
control-plane hashes, trigger/diagnoser/replay policy hashes, test evidence
hashes, and the terminal pass status. Its hash must be present in
protocol-lock.json before any A3 online search. A failed or missing certificate
blocks A3 rather than degrading it into edge-local rejection.

### Phase 3: Confirmatory Online Search

1. Freeze new, unused experiment seeds and mutation histories.
2. Only if the Phase 2 A3 release certificate is present and valid, run the
   headline matched-seed A0 versus A3 comparison. Otherwise, A0/A1/A2 work may
   continue only as exploratory evaluation; H3, H4, and H5 cannot be reported
   as confirmatory results.
3. Apply the same separately pre-reserved search and 140-task endpoint budgets
   to all participating arms.
4. Persist every parent, child, selection manifest, pair result, decision,
   archive transition, ledger entry, and terminal failure.
5. Never use D_test for parent selection, stopping, prompt changes, threshold
   changes, or human candidate selection.
6. Freeze the final artifact with the pre-registered archive rule, not manual
   inspection of the most attractive result.

### Phase 4: Locked Endpoint

After every online search artifact is frozen, construct one endpoint block per
matched evolution seed/provider-time block. In each block, run P0 once and run
each participating arm's final frozen artifact once on D_test=140 under the
same locked endpoint identity. The task-level artifact order is assigned by a
pre-registered counterbalanced hash schedule across P0 and all participating
arms; P0 must not always run first or last. The endpoint executor may not
return outcomes to the search process.

The P0 result is a shared reference for that matched block. Persist its cost as
C_reference, report it alongside every arm, and never charge it to only A0 or
A3. The primary arm cost contrast uses C_total(A, s); the program-level ledger
also reports the common reference cost and, if desired, an explicitly equal
shared allocation. Endpoint task outcomes remain sealed from search workers and
human candidate selection until every endpoint block is complete.

If the pre-registered descriptive-200 switch is enabled, do not rerun the
locked 140 observations. Instead, run only a new no-feedback D_evolve=60
endpoint for the same frozen artifact under the same endpoint identity, and
combine those 60 observations by task ID with the locked 140 observations. Do
not reuse online-search observations with a different execution identity. Store
the extra run as C_descriptive_200_extra_60, outside H4/H5 C_total, and never
feed it back to search. Label the combined value **DGM-compatible
repeated-exposure descriptive endpoint** and report the isolated 140-task
endpoint first.

## 10. Metrics And Cost Ledger

### 10.1 Local Evaluator Metrics

For frozen candidate-bank edges, report:

- Reference-action agreement against ACCEPT_ref, REJECT_ref, and ESCALATE_ref.
- False-accept and false-reject rates for edge-level decisions; separately,
  A3 rollback-target error only after the Phase 2 release gate.
- Valid-edge abstention rate and the locked ABSTAIN penalty used in
  reference-execution regret; no conditional resolved-edge score may replace
  the all-valid-edge result.
- Attempted-edge invalid rate, replacement-slot use, and the corresponding
  all-attempted edge count; valid-edge H1/H2 results may not be presented
  without these companion failure metrics.
- Escalation rate and escalation correctness.
- Reference-execution regret from the online action.
- Residual-audit gap: targeted-set Delta versus residual-audit Delta.
- Correct decisions per all-in token and per task execution.
- Coverage, redundancy, retrieval roles/ranks, repository distribution,
  P-only wins, C-only wins, ties, and invalid/incomplete-pair counts.

The selected-set raw solve rate is descriptive only. A low selected-set rate
can indicate a useful regression probe rather than poor sampling.

### 10.2 Endpoint Metrics

For each evolution seed, report:

- Q(final; D_test), the held-out 140-task solve rate.
- Held-out gain relative to the matched-block P0 reference.
- Probability that the final candidate is materially worse than the matched-block
  P0 reference under the locked materiality margin.
- Accepted, rejected, rolled-back, escalated, and invalid mutation counts.
- Cost to escape a known bad branch in the controlled lineage experiment.
- An optional quality-cost frontier only from the independently pre-registered
  budget-grid cells described in Section 3.

Task-level Wilson intervals or McNemar tests may describe one pair of final
artifacts. They do not replace seed-level inference about a search policy.

### 10.3 Required All-In Ledger

~~~text
C_total(A, s) =
  C_mutation_proposer
+ C_selector
+ C_embedding_and_retrieval
+ C_parent_runs
+ C_child_runs
+ C_audit_runs
+ C_escalation_runs
+ C_diagnosis_rollback_replay
+ C_retries_and_invalid_attempts
+ C_final_endpoint
~~~

For each term, persist input/output/cache-read/cache-write reported tokens,
API calls, agent time, task runtime, image-build time, retry count, failure
classification, and local embedding CPU/GPU seconds. Local embedding compute
is not free merely because it has no API token charge.

Valid cache reuse requires equal artifact hash, task/base commit, model
revision/settings, prompt revision, runner/evaluator revision, image identity,
budget, container policy, and randomization identity. The initial cost that
created a reusable parent result must remain in the ledger. Do not convert
parent execution cost to zero through cache accounting.

Report both C_search(A, s) and C_total(A, s); the latter includes exactly one
locked 140-task endpoint per final artifact. Report C_reference(s) and any
C_descriptive_200_extra_60(A, s) in separate, non-overlapping ledger columns.
The full program ledger is the sum of all arm C_total values, every shared P0
reference cost, and every optional descriptive-200 supplement. It must never
make the P0 reference or a failed retry disappear.

Phase 1, Phase 1b, and Phase 2 engineering/calibration costs are also retained
in a separate C_development ledger. They are not selectively charged to a
confirmatory arm and are not silently omitted from the report. The H4/H5
primary comparison uses only the pre-registered confirmatory-search and locked
endpoint ledger defined above.

## 11. Statistical Analysis

| Setting | Statistical unit | Permitted analysis |
| --- | --- | --- |
| Frozen candidate-bank pilot or confirmation bank | P -> C edge, clustered by parent lineage | Pre-registered clustered paired bootstrap; reference-execution regret and action metrics |
| Controlled rollback pilot | Pre-registered toxic lineage | Target accuracy, recovery cost, and case-study evidence |
| Online search | Matched independent evolution seed | Pre-registered paired seed-level comparison |
| One final artifact pair | Endpoint task | Descriptive paired task analysis only |

### 11.1 Primary Confirmatory Contrasts

Conditional on the A3 Phase 2 release gate, pair A0 and A3 by evolution seed
s and endpoint provider-time block. The primary endpoint and cost contrasts
are:

~~~text
d_Q(s) = Q(A3, s; D_test) - Q(A0, s; D_test)
d_C(s) = C_total(A3, s) - C_total(A0, s)
~~~

P0 is a secondary matched-block reference only. Its separately reported
C_reference does not become an unrecorded one-arm charge in d_C. The 140 task
outcomes inside one endpoint are not 140 independent evolution replicates;
task-level Wilson intervals or McNemar tests describe an artifact pair but
cannot replace seed-level policy inference.

The primary H4 test is a locked seed-paired bootstrap confidence-bound test of
the mean d_Q. It supports endpoint superiority only when its one-sided lower
bound exceeds zero and reports the pre-registered minimum important endpoint
effect. The H5 cost test is a locked seed-paired bootstrap confidence-bound
test of mean d_C. It supports lower cost only when its one-sided upper bound is
less than -gamma and the locked endpoint non-inferiority bound is above -m_NI.

H4 and H5 are co-primary for the statement "higher performance and lower token
cost": use an intersection-union rule, so both one-sided tests must pass at
the locked headline alpha. If endpoint superiority fails but non-inferiority
and H5 pass, the only permitted conclusion is "non-inferior endpoint quality
at lower primary token cost."

### 11.2 Assignment, Multiplicity, And Power

Before Phase 3, the lock must specify all of the following:

1. Matched seed assignment, arm-to-worker assignment, and the provider-time
   interleaving/counterbalancing schedule. No arm may receive another arm's
   outcomes while its search is active.
2. One-sided alpha values, bootstrap resample count and seed, endpoint minimum
   important effect, m_NI, gamma, and the complete H1-H5 multiplicity plan.
   The required default structure is: H4/H5 use the co-primary
   intersection-union rule above; H1/H2/H3 form a separately declared support
   family with a locked Holm procedure or a stricter pre-registered rule.
3. The exact estimands and directions for H1, H2, and H3, including whether
   H3 has enough independently pre-registered toxic lineages for a confirmatory
   claim. A single fixture is a mechanistic case study, not a population-level
   superiority test.
4. A power calculation or simulation, saved with an input/output hash, that
   derives the confirmatory seed count from the target endpoint effect, gamma,
   expected paired quality and cost variance/correlation, desired joint power,
   and the chosen alpha plan. Use the larger per-endpoint requirement or a
   joint-power simulation for the H4/H5 co-primary claim.
5. A separate clustered-edge candidate-bank power calculation or minimum
   detectable-effect analysis for H1/H2. It must account for parent-lineage
   clustering, expected invalid/replacement rate, the chosen support-family
   alpha rule, and the confirmation-bank size. Without it, H1/H2 are
   exploratory rather than confirmatory.
6. The failure-table rule for invalid or incomplete matched seed blocks. An
   invalid block may never be silently dropped, replaced after outcomes, or
   converted to a zero score; the lock must choose a pre-specified conservative
   analysis or state that a confirmatory inference is unavailable.

Three independent generation seeds are only an exploratory minimum. If the
completed valid seed count is below the pre-registered power-derived count, all
online-search endpoint results are exploratory. Do not use D_test to choose
seed count, candidates, prompts, thresholds, stopping conditions, or the
analysis plan.

## 12. Required Protocol Lock

No implicit defaults are allowed. The following fields must be present in a
versioned protocol-lock.json before paid execution:

~~~text
schema_version
protocol_document_sha256
initial_harness_git_sha
initial_harness_patch_bundle_hash_or_null
clean_checkout_path_hash and clean_status_hash
control_plane_release_manifest_hash
P0 artifact hash and strategy content hash
full/evolve/test split-manifest hashes
fixed_policy_file_path and fixed_policy_file_sha256
final_artifact_selection_rule
failure_state_table_version and invalid_matched_block_rule
experiment seeds, matched-seed assignment, and seed count
candidate-bank size, parent-lineage structure, and H1/H2 power-analysis input/output hashes
online mutation limit
archive parent-selection rule and archive tie-breaker
A0/A1 fixed-policy schema version and promotion/archive rule identity
A1 small-stage promotion/rejection and final-60 decision identities
per-arm search token/time reserves
per-arm 140-task endpoint token/time reserves
P0 reference endpoint token/time reserve and shared-cost allocation rule
optional descriptive-200 extra-60 reserve and enabled/disabled switch
optional frontier budget-grid cells, seed allocation, and endpoint sealing rule
per-task token/time/retry/tool limits
task_rollout_count, pair aggregation, and endpoint aggregation
initial_selected_task_budget, max_cumulative_escalation_tasks, audit size, and audit seed derivation
selector task/round/tool/token/time limits and expansion policy
delta_plus, delta_minus, audit guard, m_NI, Q_star, and gamma
cross-arm terminal-action mapping, ABSTAIN penalty, and H1/H2 denominators
bootstrap method, seed, samples, confidence level, and one-sided alpha values
H1-H5 estimands, directions, multiplicity plan, and minimum important effect
H1/H2 primary A2-versus-A1 comparator and any secondary A2-versus-A0 contrast
power-analysis input/output hashes and confirmatory seed count
Pi task-agent model configuration block
mutation-proposer model configuration block
selector model configuration block
rollback-diagnoser model configuration block or disabled state
locked endpoint task-agent model configuration block
mutation proposer and selector prompt hashes
embedding model revision and sidecar manifest hash
runner/evaluator/image/container-policy identities
endpoint ordering/counterbalance schedule hash and retry rule
P0 endpoint reference mode and provider-time block rule
A3 trigger-policy, diagnosis-schema, and replay-policy file hashes or disabled state
A3 diagnoser prompt hash, unique-target rule, and ROLLBACK_TARGET_UNRESOLVED action
A3 Phase 2 release certificate hash or disabled state
intention-to-evaluate handling for invalid/provider/budget/endpoint failures
~~~

The configuration schema must validate
initial_selected_task_budget + max_cumulative_escalation_tasks + audit_size <= 60
and max_tasks_per_round <= initial_selected_task_budget before worker startup. It must also
verify that each resource reserve is non-overlapping: search work cannot consume
the 140-task endpoint reserve, P0 reference reserve, or optional descriptive
extra-60 reserve.

The current unit-test decision values are not experiment defaults. Missing,
zero, malformed, or unrecorded required values must stop the experiment.

## 13. Readiness Gates And Failure Rules

The following gates must pass before a paid run. A failure is terminal for the
affected run; do not silently switch models, data, worker mode, or evaluation
policy.

| Gate | Current status | Required before execution |
| --- | --- | --- |
| Previous-experiment terminal attestation | Pending | Every prior run reached normal terminal state, all related processes exited, output roots are read-only, and historical outputs are denylisted; an early stop requires explicit user authorization plus a recorded deviation |
| Clean H0/P0 attestation | Not created | Approved initial harness snapshot and immutable strategy artifact |
| 60/140 split isolation | Missing | Role-filtered operational catalogue, split binding, and D_test zero-visibility test |
| Strict DeepSeek selector | Missing | Fail-closed action schema, persisted raw evidence, version/config identity, timeout/429 behavior |
| Pinned embedding sidecar | Missing | Pinned local model snapshot, 1024-D normalized response, file-hash manifest, cache binding |
| Strategy artifact bridge | Partial | Snapshotter, change-card builder, strategy-only scope validation |
| Paired round executor | Missing | Matched P/C execution, round/final plan identities, sanitized public evidence |
| Strategy endpoint adapter | Missing | Immutable strategy injection, outside official grading, no-feedback original_only endpoint |
| A2 edge controller/branch driver | Missing | Accept/reject/escalate transitions and append-only lineage without ancestor rollback |
| A3 Phase 2 release gate | Missing | Diagnosis, ancestor restore, identity-bound replay, toxic-lineage fixture, and a valid release certificate |
| P0 reference endpoint scheduler | Missing | One P0-on-140 endpoint per matched seed/time block with locked task-level counterbalancing and shared-cost ledgering |
| Unified ledger | Missing | Reconciliation across selection rounds, final pairs, proposer, embedding, retry, rollback, and endpoint |
| Runtime isolation | MVP only | Strategy-runner policy attestation; full-source candidate isolation remains blocked |
| Controlled rollback oracle | Missing | Pre-registered multigeneration toxic-lineage fixture |

### 13.1 Frozen Failure-State Table

The versioned failure-state table named in protocol-lock.json must implement at
least the following terminal handling. It applies to A0's child-focused path
and every paired path; no arm may receive a more favorable rescue rule.

| Trigger | Terminal state | Score and continuation | Ledger and inference handling |
| --- | --- | --- | --- |
| Configuration, hash, manifest, or data-isolation violation | ARM_INVALID | Stop the affected arm. If the violation touches a shared H0/control-plane or D_test boundary, invalidate the whole experiment root. Do not repair and continue under the same run identity. | Retain every incurred cost; apply the locked invalid-matched-block rule. |
| Edge-local selector/schema failure, task-plan mismatch, duplicate observation, missing required telemetry, or edge-specific execution-identity mismatch | EDGE_EVALUATION_INVALID | Stop the edge; do not score it as Y=0, archive C_t, or let it produce descendants. P_t remains current. Continue only through an identically pre-allocated replacement slot if the frozen arm policy permits one. | Retain all selector/evaluation attempts; exclude it only from valid-edge H1/H2 denominators and report it in the attempted-edge invalid rate. |
| Invalid child scope, strategy schema, symlink, or artifact hash | CANDIDATE_INVALID_REJECTED | Do not score it as Y=0; it cannot enter the archive or produce descendants. It consumes only the pre-allocated proposal/replacement slot defined by the frozen arm policy. | Retain proposal and validation costs. |
| Provider/API failure after the locked infrastructure retries | PAIR_INCOMPLETE_INVALID | Do not score it as zero or silently sample a new model output. Continue only through an identically pre-allocated replacement slot if the lock permits one. | Retain every attempt and report the incomplete pair. |
| Task-agent timeout with complete identity, task readiness, and telemetry | TASK_TIMEOUT_OBSERVED_ZERO | Record the task observation as Y=0. Runner, provider, image, and grader failures must not be relabeled as a valid agent timeout. | Retain full task cost and classify separately from infrastructure failure. |
| Search-budget reserve exhausted | SEARCH_BUDGET_EXHAUSTED | Preserve the endpoint reserve. Freeze the artifact under the pre-declared final-artifact rule, or mark the arm invalid if that explicit lock rule requires it. | No manual replacement or best-looking candidate choice; retain all search costs. |
| Locked endpoint failure after allowed infrastructure retries | ENDPOINT_INVALID | Do not substitute another candidate or silently rerun. The endpoint block follows the pre-registered invalid-block rule. | Retain endpoint costs and display the failed block in the primary result table. |
| Dynamic escalation capacity exhausted | ESCALATE_EXHAUSTED | Do not archive C_t; P_t remains current and the edge remains unresolved. | Retain all expansion costs and report the terminal state. |
| A3 lineage evidence has no unique diagnosed bad edge | ROLLBACK_TARGET_UNRESOLVED | Freeze the lineage and do not choose an ancestor heuristically. Only the pre-registered unresolved-lineage action may continue it. | Retain diagnosis costs and report the unresolved lineage separately. |

Only TASK_TIMEOUT_OBSERVED_ZERO is an observed task failure. Every other
invalid/incomplete state remains distinct from an unsolved task and is never
silently collapsed into a numerical score.

The full-candidate Docker path is intentionally fail-closed and must not be
bypassed through host execution. The strategy/workflow MVP may use the existing
Pi host runner only after its narrower policy, artifact boundary, and identity
binding are implemented and documented.

Every production loop must show a terminal tqdm progress bar and persist
configuration, round/task progress, trajectories, token telemetry, tool
telemetry, exceptions, invalid states, and hash-chained events. A missing
progress bar or required artifact is a run failure, not a reason to reduce
logging.

## 14. Reproducibility Layout

Create a new output root only after Phase 0 passes. It must never be
dgm200_run/ or any other historical experiment root.

~~~text
research_output/adaptive_strategy_mvp_<experiment-id>/
  protocol-lock.json
  cold-start-attestation.json
  frozen-inputs/
    dgm200-manifest.json
    evolve-60-manifest.json
    test-140-manifest.json
    split-binding.json
    experiment-config.json
    decision-policy.json
    fixed-policy.json
    failure-state-table.json
    control-plane-release-manifest.json
    a3-trigger-policy.json
    a3-diagnosis-schema.json
    a3-replay-policy.json
    software-manifest.json
  artifacts/
    P0/
    <artifact-hash>/
  artifact-records/
  candidate-bank/
  arms/
    A0-fixed-unpaired/
    A1-fixed-paired/
    A2-dynamic-paired/
    A3-full-rollback-phase2-gated/
  round-manifests/
  selection-manifests/
  frozen-task-plans/
  pairs/
  rollback-lineages/
  phase2-release/
  state/events/
  global-cost-ledger.jsonl
  reports/
  endpoints/
    P0_reference_140/
    D_test_140/
    D_evolve_60_descriptive/
    DGM200_descriptive_merged_reports/
  invalid-attempts/
~~~

Each edge directory must retain its controller request, candidate-change card,
artifact manifest, mutation request/response hashes, round manifests, raw
selector evidence, sanitized evidence presented to later components,
selection manifest, frozen task plan, pair observations, decision, local
ledger, and terminal outcome.

Use distinct classifications for:

~~~text
infrastructure invalid
scientific negative result
candidate failure
budget termination
provider failure
data-isolation violation
~~~

Do not silently collapse these into unresolved tasks.

## 15. Existing Tooling Boundaries

The following current tools are reusable only after adapters enforce this
protocol:

- rollback_mvp/pi_swe_runner.mjs supports one strategy file for one task and
  records useful trajectory/token telemetry. It does not provide the required
  adaptive identity, artifact hashing, endpoint orchestration, or
  outside-evaluator binding by itself.
- rollback_mvp/orchestrate_endpoint_200.py supports fixed Pi endpoint
  operations, but it has no strategy-artifact parameter, archive driver, or
  dynamic selector. Do not use --max-tasks 60: manifest row order is not the
  literal DGM small union medium partition.
- rollback_mvp/adaptive_eval/ supplies contracts, fake tests, state, coverage,
  audit, pairing, and decision logic. It currently has no production selector,
  sidecar, round evaluator, or deployable full-candidate runtime.
- freeze_dgm200_manifest.py is not a runtime helper for this experiment; it
  can download data and must not be invoked to recreate the already frozen
  input manifest.

The only currently suitable non-paid provenance check is validation of the
already frozen full manifest. It is not proof that the 60/140 isolation,
strategy artifact execution, or dynamic experiment is ready. No agent may
interpret an existing CLI validation command as authorization to begin a paid
run.

## 16. Permitted And Prohibited Language

Permitted after the appropriate evidence is complete:

- "Dynamic paired sampling improved mutation-decision quality under the
  pre-registered strategy-level Pi protocol."
- "Under the pre-registered resource ceiling, the method improved the isolated
  140-task endpoint and/or cost frontier."
- "Higher endpoint performance and lower primary token cost" only after the
  Phase 2 release gate and both co-primary H4/H5 tests pass.
- "The 200-task result is a DGM-compatible repeated-exposure descriptive
  endpoint."

Prohibited:

- "The selected dynamic batch score is the agent's benchmark performance."
- "The MVP is full Pi source-level self-evolution or an exact DGM replication."
- "DGM's published 50% is a same-model, same-agent, causal baseline."
- "DGM-200 is a newly unseen holdout for this repository."
- "The method is token-efficient" before the unified all-in ledger passes.
- "A3 rollback improved the search" before its Phase 2 release gate and
  controlled toxic-lineage evidence pass.
- Any use of official evaluator feedback in selector, mutation, bad-case,
  archive, or standard endpoint decisions.

## 17. Handoff Checklist

Before delegating implementation or execution, the receiving agent must
acknowledge all of the following:

- The experiment starts from an approved initial harness and a newly created
  P0, never from an intermediate 200-task output.
- The new run waits until currently active experiments reach normal terminal
  state, their processes exit, and their output roots are read-only; it does
  not read their evidence. Early termination requires explicit user approval
  and a recorded deviation.
- Phase 1 runs only A0/A1/A2. A3 is a distinct multigeneration rollback arm
  only after its Phase 2 release certificate is valid.
- D_evolve=60 and D_test=140 are enforced by access controls, not a convention
  in prompts.
- A parent is a counterfactual reference, not an additional endpoint score.
- All P/C, selector, audit, proposer, rollback, retry, and endpoint costs are
  ledgered, with P0 reference and optional descriptive-200 supplement costs
  reported separately rather than silently assigned to one arm.
- P0-on-140 runs once per matched seed/time block after search sealing, and a
  descriptive 200 result combines locked 140 observations with a new 60-task
  endpoint supplement rather than rerunning D_test.
- The strategy-artifact MVP does not authorize host execution of evolved Pi
  source code.
- A readiness-gate failure stops the run rather than silently degrading it.
