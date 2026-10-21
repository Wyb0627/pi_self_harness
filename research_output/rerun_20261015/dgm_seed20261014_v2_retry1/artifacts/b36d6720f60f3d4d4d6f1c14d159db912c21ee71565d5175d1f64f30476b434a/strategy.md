## Root-Cause Strategy for Rendering and Choice-Suppression Defects

When a framework bug report describes incorrect rendered output (an extra option, a missing attribute, or a widget being mutated), investigate from the public rendering contract inward instead of starting with a broad test run.

1. **State the contract**: write one sentence describing what should appear in the rendered HTML, and one sentence describing what should not appear. Keep this tied to user input and model metadata such as requiredness, initial state, and choices.
2. **Reproduce with the smallest possible source-level example**: create the relevant form/model/widget, render it, and inspect the exact HTML. A direct Python expression is faster than a full server response.
3. **Search the source tree** for the implementation of the responsible field or widget. Useful terms are the widget class name, `empty_label`, `use_required_attribute`, `get_context`, `choices`, `blank`, `checked`, and `required`.
4. **Read the nearest sibling implementations**. If the bug is in one widget but not another, reading their `get_context`, `use_required_attribute`, or option-generation methods shows the invariant that should be preserved.
5. **Trace metadata into the render path**. The fix should normally consult existing model/form metadata (requiredness, initial state, or an empty-label policy) rather than special-case a literal value or option string. This preserves the intended behavior of other widgets while correcting only the widget that renders an implicit unfilled state.
6. **Add a regression test at the rendering layer**. Assert both the presence and absence of the offending attribute or option in the rendered HTML so the contract is explicit and future changes cannot silently reintroduce it.
7. **Run the smallest relevant test module** for the component family (form fields, widgets, model forms, and admin forms when the same widget is used there).

This workflow is reusable for any incident whose symptom is visible in HTML output: it identifies the responsibility boundary, uses read-only source inspection to map the call chain, and validates the fix with a rendering-level assertion.