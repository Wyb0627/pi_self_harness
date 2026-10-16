## Static code-path tracing for missing effects

When a report describes a hook, callback, event, option, or transform that should change output but does not, use the `code_search` tool to locate the relevant code path statically instead of guessing.

1. Search for the exact name from the report (hook, option, event, directive). If it is not present, search for nearby aliases and abbreviations.
2. Separate definition sites from call sites using the surrounding lines returned by the search. Record the file:line pairs.
3. Trace the data-flow from the call site to the output stage. Look for intermediate readers, cached copies, or secondary parse paths that may bypass the changed value; search for terms such as 'read', 'include', 'copy', 'cache', 'append'.
4. Before editing, write a one-sentence hypothesis naming the stage where the effect is lost and the file where the fix belongs.
5. After making a change, re-run the same searches to verify that the edited path is reachable from the original call site.

Use this workflow for every issue where an extension or builder hook appears to fire but its effect does not reach the final document.

## Static code-path tracing for missing effects

When a report describes a hook, callback, event, option, or transform that should change output but does not, use the `code_search` tool to locate the relevant code path statically instead of guessing.

1. Search for the exact name from the report (hook, option, event, directive). If it is not present, search for nearby aliases and abbreviations.
2. Separate definition sites from call sites using the surrounding lines returned by the search. Record the file:line pairs.
3. Trace the data-flow from the call site to the output stage. Look for intermediate readers, cached copies, or secondary parse paths that may bypass the changed value; search for terms such as 'read', 'include', 'copy', 'cache', 'append'.
4. Before editing, write a one-sentence hypothesis naming the stage where the effect is lost and the file where the fix belongs.
5. After making a change, re-run the same searches to verify that the edited path is reachable from the original call site.

Use this workflow for every issue where an extension or builder hook appears to fire but its effect does not reach the final document.

## Trace identity mismatches in database schema operations

When a migration or schema operation fails because an index, constraint, or column is reported as ambiguous, missing, or duplicated, treat the problem as an identity-matching failure rather than a SQL or data problem.

1. Identify the exact operation that failed (for example, deleting a composite index, altering a field, or removing a constraint) and the backend method named in the traceback.
2. Use `symbol_map` with the method name to find its definition and all callers. Then use `code_search` for related nouns from the error message (`constraint`, `index`, `unique`, `fields`) in the same file to locate every place the method collects or filters candidates.
3. List every property used to consider two schema elements equal. Common identities are: database name, field list, constraint kind, and condition. A match on fields alone is not an identity; two different constraints can legitimately share the same fields.
4. Determine whether the failing operation distinguishes the element it wants from other elements that share fields. If candidate collection returns multiple elements, check whether each candidate carries a type marker or kind attribute that the operation ignored.
5. Before editing, write one sentence describing the intended identity of the schema element and which existing predicate in the code gets it wrong (for example, matching only fields, or not filtering by constraint kind).
6. After editing, search for tests that exercise the same backend method for both unique and non-unique composed indexes, then re-run the searches to confirm the changed filter is applied on every code path that collects candidates.