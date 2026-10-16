## Static code-path tracing for missing effects

When a report describes a hook, callback, event, option, or transform that should change output but does not, use the `code_search` tool to locate the relevant code path statically instead of guessing.

1. Search for the exact name from the report (hook, option, event, directive). If it is not present, search for nearby aliases and abbreviations.
2. Separate definition sites from call sites using the surrounding lines returned by the search. Record the file:line pairs.
3. Trace the data-flow from the call site to the output stage. Look for intermediate readers, cached copies, or secondary parse paths that may bypass the changed value; search for terms such as 'read', 'include', 'copy', 'cache', 'append'.
4. Before editing, write a one-sentence hypothesis naming the stage where the effect is lost and the file where the fix belongs.
5. After making a change, re-run the same searches to verify that the edited path is reachable from the original call site.

Use this workflow for every issue where an extension or builder hook appears to fire but its effect does not reach the final document.

## Regex and format-contract auditing for parsing fixes

When a reported bug is about a parser, a quoted regular expression, or a value that is rejected even though it looks valid, audit the format contract before editing.

1. Locate the parsing code with `code_search`, using the function name from the report and related names such as `_re`, `parse`, `format`, `field`, and `duration`.
2. Run `regex_contract_audit` on the module. Read the structural report for every compiled pattern: named groups, lookarounds, signed digit captures, and unsigned lookahead digit constraints.
3. Check sign and optionality consistency. If a component is allowed to be signed in one named group or branch, every lookahead, separator, and related branch that consumes the same component must accept the same optional sign. Mismatched lookaheads are a common cause of valid inputs being rejected.
4. Check whether the pattern is built dynamically with formatting, concatenation, or f-strings. If external values can appear in the pattern, wrap literal parts with `re.escape()` unless metacharacter behavior is intentional.
5. After editing, re-run `regex_contract_audit` to confirm the reported lookahead and optional-sign constraints changed as intended, and use `code_search` to find all callers or documented examples of the format so the fix covers every shape.