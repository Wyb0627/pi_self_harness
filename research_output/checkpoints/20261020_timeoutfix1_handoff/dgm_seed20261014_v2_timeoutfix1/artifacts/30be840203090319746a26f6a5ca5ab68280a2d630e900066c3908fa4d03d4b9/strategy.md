## Diagnosing behavior that works only for primary inputs

When an extension-facing hook, event, or transformation callback fails to affect all inputs that reach the output, treat it as a routing/data-flow bug before looking for output-format bugs.

1. Reproduce with the smallest project where the hook observably fires for both a primary input and a secondary input (a file reached through a directive, import, template, or second builder). Log what the hook sees for each input and what text is present in the final output.

2. Find where the hook is emitted and every other place source text is read, transformed, or copied. Use `code_search` to search for the hook name, then search for functions that construct source objects or call the reader. Start with `file_pattern` `.*[.]py$` and `context_lines` 4.

3. Determine whether the transformed text is stored on the single object that continues downstream. If a separate reader or directive opens secondary inputs after the hook, the hook can fire yet its result can be discarded.

4. Read the callers of the candidate read/transform functions and annotate the route from file read to final serialization. Choose one shared bottleneck where the mutation can be applied; avoid adding duplicate transforms on each route.

5. Add tests that cover the secondary input route. Tests that only build the primary input give false confidence when the failing route is conditional.

Useful follow-up searches: the event/extension name, `read`, `parse`, `include`, or source cache names; then broaden to related builders/options after the data flow is understood.