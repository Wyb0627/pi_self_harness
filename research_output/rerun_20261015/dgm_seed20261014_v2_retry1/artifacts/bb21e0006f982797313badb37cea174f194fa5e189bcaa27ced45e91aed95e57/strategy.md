## Static code-path tracing for missing effects

When a report describes a hook, callback, event, option, or transform that should change output but does not, use the `code_search` tool to locate the relevant code path statically instead of guessing.

1. Search for the exact name from the report (hook, option, event, directive). If it is not present, search for nearby aliases and abbreviations.
2. Separate definition sites from call sites using the surrounding lines returned by the search. Record the file:line pairs.
3. Trace the data-flow from the call site to the output stage. Look for intermediate readers, cached copies, or secondary parse paths that may bypass the changed value; search for terms such as 'read', 'include', 'copy', 'cache', 'append'.
4. Before editing, write a one-sentence hypothesis naming the stage where the effect is lost and the file where the fix belongs.
5. After making a change, re-run the same searches to verify that the edited path is reachable from the original call site.

Use this workflow for every issue where an extension or builder hook appears to fire but its effect does not reach the final document.

## Trace argument contracts before changing dispatch code

When a runtime error quotes a callable and one of its parameter names (for example telling the user a keyword was unexpected), the root cause is usually an argument-dispatch layer that reconstructs calls from external syntax. Treat every such layer as a separate contract to inspect, rather than changing the target callable.

1. Locate the error message text verbatim; it identifies the dispatch/validation code that decides whether arguments are accepted.
2. Use `callable_contract` to read the target callable's signature and find its call sites. Record each parameter kind (positional-only, positional-or-keyword, keyword-only, var-positional, var-keyword), defaults, and decorators.
3. Reconstruct what argument model the dispatch layer builds: names, positional vs keyword groups, duplicates, defaults, and parameter kinds. Compare that model with the actual signature.
4. Identify where external syntax is mapped into the call. If the dispatch code filters parameters before calling, verify that accepted parameter kinds and defaults are handled consistently.
5. Find every entry point that reaches the dispatch layer so the same contract is checked once and shared.
6. Before editing, write a one-sentence hypothesis naming the contract mismatch and the file that implements the dispatch layer.
7. After editing, trace the same path again and verify that each accepted external argument reaches the target with the same name and type, and each rejected duplicate reaches the intended error branch.

Use this workflow whenever a public API rejects or forwards arguments unexpectedly, especially when the error message quotes a parameter name.