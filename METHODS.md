# Methods

## Pre-registered 60/140 Dynamic-Sampling Evaluation
- **Purpose**: Compare a DGM-compatible fixed evaluation policy with dynamic
  paired sampling from a clean initial Pi strategy artifact; true
  multigeneration rollback is a separately Phase-2-gated extension.
- **Core logic**: The online controller may see only
  D_evolve = small(10) + medium(50). For each mutation, it compares the
  parent and child on one frozen task union plus a controller-private residual
  audit; only
  after the search freezes may the final artifact run once on
  D_test = big(140). The headline comparison is final-agent held-out quality
  and the complete search-plus-endpoint ledger, not the selected-batch score.
- **Key code**:
  ~~~python
  # Required future execution boundary; no production adapter exists yet.
  selection = controller.run_selection(parent=parent, child=child)
  decision = run_final_pipeline(
      selection=selection, executor=paired_executor,
      parent=parent, child=child, policy=decision_policy,
      catalogue=evolve_catalogue, vectors=evolve_vectors,
  )
  ~~~
- **Notes**: Phase 1 runs A0/A1/A2 only; A3 requires a tested lineage
  diagnosis/restore/replay oracle before it may be the headline arm. P0 has a
  separate shared-cost 140-task reference endpoint for each matched seed/time
  block. A descriptive 200 result combines that locked 140 endpoint with a new
  identity-matched 60-task endpoint supplement, never a rerun of D_test. The
  protocol calls the controller ablations A0 through A3 to avoid collision with
  existing rollback-policy labels. It requires a role-filtered catalogue and
  D_test zero visibility before any paid run. See
  DYNAMIC_SAMPLING_60_140_EXPERIMENT_PROTOCOL.md.

## Agentic Adaptive Evaluation Sampling
- **Purpose**: Select a small mutation-specific SWE-bench batch for a DGM-style
  evolution while preserving an auditable paired accept/rollback gate.
- **Core logic**: A frozen tool-calling model iteratively retrieves tasks from
  parent bad-case evidence, parent-to-child diff, lexical search, and semantic
  search. It may adapt to earlier paired public evidence, but every round is
  append-only and a controller-private deterministic residual audit is added
  after it stops.
- **Key code**:
  ~~~python
  selection = controller.run_selection()
  final = run_final_pipeline(
      selection=selection, executor=paired_executor,
      parent=parent, child=child, policy=decision_policy,
      catalogue=catalogue, vectors=vectors, output_root=output_root,
  )
  ~~~
- **Notes**: The model proposes evidence to inspect but cannot make a final
  decision. Invalid output, incomplete pairs, and identity/hash mismatches fail
  closed. An adaptive batch is an operational gate, not an unbiased full-set
  estimate. The implementation is in `rollback_mvp/adaptive_eval/controller.py`
  and `selector_agent.py`; every selector prompt/response/tool result is retained.

## Facility-Location Coverage and Audit
- **Purpose**: Prevent a causal/regression-focused batch from collapsing onto
  near-duplicate issues while retaining a controller-private residual-pool
  check.
- **Core logic**: For L2-normalized task embeddings, the selected set covers a
  catalogue task through its most similar representative. Greedy marginal
  coverage fills remaining capacity; average nearest-neighbor similarity is
  logged as redundancy rather than folded into an opaque score.
- **Key code**:
  ~~~python
  def marginal_coverage(candidate, selected, universe):
      before = [max((similarity(u, s) for s in selected), default=0.0)
                for u in universe]
      after = [max(old, similarity(u, candidate))
               for u, old in zip(universe, before)]
      return sum(new - old for old, new in zip(before, after)) / len(universe)

  def redundancy(selected):
      if len(selected) < 2:
          return 0.0
      return sum(max(similarity(item, other) for j, other in enumerate(selected)
                     if index != j) for index, item in enumerate(selected)) / len(selected)
  ~~~
- **Notes**: Lexical retrieval handles exact errors, paths, tools, and symbols;
  local Qwen embedding handles semantic paraphrases. The audit seed derives
  from frozen run identities and cannot be selected by the model. See
  AGENTIC_ADAPTIVE_EVALUATION_DESIGN.md for the full contract.

## Frozen DGM-200 Catalogue and Embedding Index
- **Purpose**: Bind retrieval to the exact public DGM task universe without
  exposing gold patches or silently falling back when semantic infrastructure
  is invalid.
- **Core logic**: `catalogue.py` validates raw manifest SHA-256
  `3fb913f...f96c967`, newline-delimited ordered-ID SHA-256 `421c950...1d0d7`,
  all row hashes, ordinals, unique IDs, and the 153/25/22 distribution.
  `embedding_client.py` accepts only the pinned Qwen revision, normalized 1024-D
  vectors, matching sidecar manifest metadata, and cache keys over text, role,
  template, max length, model revision, and sidecar hash.
- **Key code**:
  ```python
  catalogue = load_frozen_catalogue(manifest_path)
  embedded = embed_catalogue(catalogue, embedding_client, evidence_dir)
  lexical = LexicalIndex(embedded.catalogue)
  semantic = SemanticIndex(
      embedded.catalogue, embedded.vectors, embedding_client
  )
  ```
- **Notes**: BM25 and cosine rankings remain separate result streams. No
  `mlx-embeddings` package or model was installed or downloaded.

## Identity-Bound Paired Decision
- **Purpose**: Prevent missing, duplicate, cross-model, cross-image, or
  cross-manifest observations from becoming failed tasks or zero scores.
- **Core logic**: `paired_executor.py` freezes a task plan and binds each task
  to both artifact hashes, exact model/inference settings, budgets, runner and
  evaluator image digests/revisions, and container policy. `decision.py` first
  requires exactly one complete identity-consistent parent/child pair per final
  task, then computes child-only wins, parent-only wins, paired bootstrap
  interval, exact McNemar value, and the audit guard.
- **Key code**:
  ```python
  pairs = executor.run_pairs(parent_artifact, child_artifact)
  validated = validate_complete_pairs(frozen_plan, pairs, catalogue)
  decision = decide(frozen_plan, validated, decision_policy, catalogue)
  counterfactual = executor.run_counterfactual(artifact, frozen_plan)
  ```
- **Notes**: A counterfactual plan unequal to the parent/child final manifest is
  terminal. Incomplete evidence is controller-invalid, not `ROLLBACK` and not a
  score of zero. CLM/ddmin integration is not implemented here; this is the
  enforced boundary it must call.

## Full-Candidate Container Boundary
- **Purpose**: Specify a fail-closed boundary for evolved Pi source without
  permitting host execution or access to evaluator and gold data.
- **Core logic**: `container_runner.py` validates the candidate source content
  hash, digest-pinned image, public-only task input, restricted Unix-socket
  model proxy, resource/security policy, and candidate output hashes. The
  candidate receives no general network and produces a patch/trajectory; an
  injected outside evaluator grades copied immutable evidence.
- **Key code**:
  ```python
  invocation = build_invocation(
      request=request, image_digest=image_digest, policy=policy,
      proxy_policy=proxy_policy, immutable_control_roots=control_roots,
  )
  runtime_result = docker_runtime.run(invocation)
  observation = outside_evaluator.evaluate(request, result, patch, trace, evidence)
  ```
- **Notes**: Only the contract and fake runtime were tested. The current Colima
  socket is inaccessible, and `DockerCliRuntime` deliberately refuses execution
  until quota-backed mounts, enforced proxy ledger, fresh workspaces, and timeout
  cleanup can be attested. There is no host-Pi fallback.
