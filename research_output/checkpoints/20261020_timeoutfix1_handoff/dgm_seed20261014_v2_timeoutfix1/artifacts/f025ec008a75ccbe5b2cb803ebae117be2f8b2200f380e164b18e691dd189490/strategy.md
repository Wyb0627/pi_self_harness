# Reusable Strategy

## 1. Reproduce before editing
- Create the smallest possible reproduction that shows the reported failure, either as a standalone script or as a focused test.
- Note the exact error message and stack trace; the exception type and message usually name the subsystem to investigate.
- Check whether the failure depends on declaration order, input order, or configuration order and record that fact explicitly.

## 2. Trace the code path from observed behavior
- Use the `search_source_code` tool to locate every occurrence of the relevant exception, option name, or function.
- Follow the stack trace backward: identify where the exception is raised and what data was being computed at that point.
- When the report involves model fields or ORM metadata, inspect metaclass/Options code and any loops that iterate fields in declaration order.

## 3. Fix root causes, not symptoms
- Look for state that is set while iterating and then silently overwritten by a later iteration.
- If an explicit marker or attribute should control behavior, find where that marker is read and ensure the decision does not depend on prior unrelated declarations unless the API contract requires it.
- Make the smallest change that preserves the intended behavior for all orderings.

## 4. Validate with focused and adjacent tests
- Run the reproduction case first, then run nearby existing tests for the same component.
- For ORM/model changes, include adjacent checks involving inheritance, field-name clashes, primary-key handling, and related-field lookups.
- Re-read the diff to confirm it changes only the intended code path and introduces no new ordering assumptions.

## 5. Use read-only source search efficiently
- Always prefer `search_source_code` over guessing file locations.
- Search for the literal error message or option name first; then narrow by file path substrings such as `models/` or `forms/` when the search is too broad.