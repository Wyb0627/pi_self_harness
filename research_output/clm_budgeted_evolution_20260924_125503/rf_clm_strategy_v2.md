# Repair-First Causal Debugging Policy

Use the failure boundary to derive one concrete invariant before broad
exploration. Make a minimal source edit by the eighth tool call, then verify it.

- ORM expression failures: trace how empty/full-result sentinels are compiled
  under negation and conditional expressions. Preserve semantic truth values;
  never emit an empty SQL condition.
- ORM lookup failures: compare the target lookup with adjacent working lookup
  classes. Reuse backend-specific RHS preparation and JSON adaptation, not only
  numeric casting behavior.
- Relation traversal failures: distinguish explicit model inheritance from a
  relation that happens to be the primary key. Follow metadata that represents
  parent links rather than inferring inheritance from `primary_key`.
- Cascade deletion failures: derive the exact fields needed for relation
  traversal. Restrict related-object queries to those fields when no signal or
  parent dependency requires full model loading.
- Parsers: preserve the sign semantics of the complete grammar. Do not fix one
  token in isolation when a leading sign applies to the whole value.

Do not search release history or download another implementation. Do not
modify tests. If local dependencies are missing, inspect existing tests and
source, implement the hypothesis, and stop instead of building an environment.
If a candidate contradicts local evidence, remove only that edit and retain
independent useful changes.
