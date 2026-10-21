## Static code-path tracing for missing effects

When a report describes a hook, callback, event, option, or transform that should change output but does not, use the `code_search` tool to locate the relevant code path statically instead of guessing.

1. Search for the exact name from the report (hook, option, event, directive). If it is not present, search for nearby aliases and abbreviations.
2. Separate definition sites from call sites using the surrounding lines returned by the search. Record the file:line pairs.
3. Trace the data-flow from the call site to the output stage. Look for intermediate readers, cached copies, or secondary parse paths that may bypass the changed value; search for terms such as 'read', 'include', 'copy', 'cache', 'append'.
4. Before editing, write a one-sentence hypothesis naming the stage where the effect is lost and the file where the fix belongs.
5. After making a change, re-run the same searches to verify that the edited path is reachable from the original call site.

Use this workflow for every issue where an extension or builder hook appears to fire but its effect does not reach the final document.