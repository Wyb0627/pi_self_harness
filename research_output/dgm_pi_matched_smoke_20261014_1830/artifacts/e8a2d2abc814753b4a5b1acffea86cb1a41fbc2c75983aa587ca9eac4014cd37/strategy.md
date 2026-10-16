# Strategy: Smallest Viable Change with Phase Budgets

## 1. Goal
Complete each repository task by making the smallest correct change. The default failure mode is spending too many resources on exploration and producing no result. Prevent that by treating every task as: find one likely edit site, patch it minimally, and prove it with narrow tests.

## 2. Inspection (target: 20% of budget)
- List top-level files and read README, contributing guide, and build configuration files to identify language, test command, and layout.
- Read the request and extract the exact observable behavior. Convert it into a list of candidate keywords and likely module names.
- Use grep or equivalent to locate definitions that determine that behavior. Prefer exact identifiers over broad searches.
- For each candidate, inspect only its immediate body, callers, and existing tests. Do not read unrelated architecture unless necessary.
- Stop when one candidate edit site is clear. Record file path, line number, current behavior, changed behavior, and verification command.
- If no candidate appears after 20% of the budget, choose the closest API or function mentioned in the request and make the smallest plausible improvement there.

## 3. Editing (target: 10% of budget)
- Make the smallest syntactic change that alters behavior in the desired direction.
- Preserve style, types, and conventions. Add comments only if they explain non-obvious intent.
- If the change requires more than one edit, keep them in the same function or module unless impossible.
- Avoid refactoring, reformatting, renaming, or dependency updates.
- If a library function or language feature provides a cleaner equivalent, prefer using it only when it is already available in the project's supported environment.

## 4. Verification (target: 50% of budget)
- Run the most specific test or command that exercises the changed line first.
- If no specific test exists, run the module or package test suite.
- Use the project's configured commands. For large suites, use filters with file, class, or test names.
- Inspect failures immediately; do not run broad suites until the narrow check passes.
- Also run a quick static check if configured, on the changed file only.
- If the change is verified, stop; do not add extra enhancements.

## 5. Token and time budget
- Allocate work by phases: inspection 20%, edit 10%, verification 50%, recovery 20%.
- Re-evaluate after each phase.
- Prefer commands that return small output: head, tail, grep, sed, git diff.
- Never print whole files unless they are under about 100 lines.
- Track all commands and candidates in short notes so recovery does not repeat work.

## 6. Recovery (target: 20% of budget)
- If verification fails, first inspect the failure message and the diff. The failure is usually local to the edit.
- If the edit is wrong, revert it and revisit the candidates list from inspection; choose the next most plausible candidate.
- Do not begin a new repository-wide search from scratch; reuse search context.
- If repeated failures consume most of the recovery budget, fall back to a minimal patch at the nearest public API point and verify only that it compiles or passes syntax.
- If the project has no tests, at least ensure the patch is syntactically valid and consistent with surrounding code.

## 7. Finalization
- Before finishing, show a short diff stat and full diff to confirm only intended changes are present.
- Remove debug statements, temporary files, and accidental unrelated edits.
- If possible, re-run the narrow verification once more on the final diff.

This strategy is intentionally conservative: in an unfamiliar repository, a small, verified patch is more likely to produce a working result than a broad exploration followed by a large untested change.