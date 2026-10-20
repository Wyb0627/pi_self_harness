## Diagnosing behavior that works only for primary inputs

When an extension-facing hook, event, or transformation callback fails to affect all inputs that reach the output, treat it as a routing/data-flow bug before looking for output-format bugs.

1. Reproduce with the smallest project where the hook observably fires for both a primary input and a secondary input (a file reached through a directive, import, template, or second builder). Log what the hook sees for each input and what text is present in the final output.

2. Find where the hook is emitted and every other place source text is read, transformed, or copied. Use `code_search` to search for the hook name, then search for functions that construct source objects or call the reader. Start with `file_pattern` `.*[.]py$` and `context_lines` 4.

3. Determine whether the transformed text is stored on the single object that continues downstream. If a separate reader or directive opens secondary inputs after the hook, the hook can fire yet its result can be discarded.

4. Read the callers of the candidate read/transform functions and annotate the route from file read to final serialization. Choose one shared bottleneck where the mutation can be applied; avoid adding duplicate transforms on each route.

5. Add tests that cover the secondary input route. Tests that only build the primary input give false confidence when the failing route is conditional.

Useful follow-up searches: the event/extension name, `read`, `parse`, `include`, or source cache names; then broaden to related builders/options after the data flow is understood.

## Tracing callable signatures through decorator and dispatch layers

When a callable rejects an argument it should accept, or reports the wrong duplicate-keyword error, the public callable is usually only the last layer of a pipeline that decides which names are legal. Trace all layers before changing validation logic.

1. Reproduce with two minimal calls: one supplying each accepted keyword, and one repeating the same keyword. Note the exact error wording; it often identifies the rejecting layer.

2. Find the public entry point and the decorator/registration path. Use `code_search` for the decorator name and for the error strings. Then use `callable_signatures` on the decorator and any inner wrappers to see whether the exposed signature is the original callable's signature or a synthesized list.

3. Locate where accepted keywords are computed. Search for signature-introspection calls and keyword lists: `getfullargspec`, `getargspec`, `signature`, `co_varnames`, `co_kwonlyargcount`, `kwonly`, `kwargs`, and the exact error messages from step 1. A custom parser may rebuild this list without consulting every part of the signature.

4. Test each argument category separately: positional-only, positional-or-keyword, keyword-only with defaults, keyword-only without defaults, `*args`, and `**kwargs`. A bug often appears only for keyword-only arguments or only for keyword-only arguments that have defaults.

5. Check duplicate-keyword handling at the same layer. If the duplicate check is applied only to one category of accepted names, repeated keywords in the other category fall through to the `unexpected` branch. The duplicate check should cover every accepted name.

6. Prefer fixing the shared helper used by all decorator variants over patching one registration path. If several public decorators forward to the same argument-parsing helper, a fix in that helper covers all of them.

Useful follow-up searches: the decorator/registration name, the exact error strings, all occurrences of `kwonly`, `kw_defaults`, `varkw`, and the shared parsing helper that builds accepted names.