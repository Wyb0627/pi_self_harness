# Repository Change Strategy

## Core principle
Treat every task as a small, targeted change until evidence proves otherwise. Spend tokens on hypothesis verification, not repository exploration. If the patch is not nearly complete after a small number of edits, the approach is wrong.

## 1. Scope bounding
- Read the problem statement and identify the affected component (API, CLI, backend, library, config).
- Extract only concrete identifiers: module names, function names, class names, configuration keys, error messages.
- Search the repository for those identifiers with one targeted query (rg/grep/IDE). Read at most 3-5 files in the first pass.
- Write down the minimal file set you expect to touch. Do not add related improvements while reading.

## 2. Hypothesis-first inspection
- Before opening files, state one falsifiable hypothesis: "The likely defect/change is in X; making Y produce Z."
- Inspect call sites, import paths, and adjacent modules needed to prove or disprove it.
- Use `git log -S`/`git blame` for relevant functions to infer project conventions and intent.
- Stop searching once the hypothesis is supported. Avoid reading unrelated tests, docs, or history.

## 3. Minimal implementation
- Create the smallest diff that realizes the hypothesis.
- Preserve existing style, public API, and configuration mechanisms.
- Reuse already imported utilities and idiomatic standard-library APIs instead of introducing new dependency patterns.
- If multiple files seem needed, implement the core file first and only then touch dependent call sites.
- Do not refactor, reformat, or rename unrelated code.

## 4. Early, focused verification
- Run the narrowest feasible check immediately after editing: syntax/compile for the edited files, then one targeted test or test file.
- Prefer test commands discovered in CI config, Makefile, package manifest, or documentation.
- Before broad tests, run `git diff --check` and inspect `git diff --stat`; the diff should touch only intended lines.
- If the targeted check fails, debug that failure, update the hypothesis, and retry once. Do not widen to full-suite exploration.
- Only if the failure demonstrates that the change affects more code should you expand scope.

## 5. Token budget enforcement
- Set explicit checkpoints: before each edit, ask whether the current hypothesis is still the cheapest plausible explanation.
- Allow at most 2-3 implementation attempts. After that, stop editing and re-read the problem statement and the current diff.
- Never launch full test suites, install new dependencies, or regenerate tooling unless a focused command already failed for a reason that requires it.
- Do not read whole files when a symbol search can answer the question.

## 6. Recovery
- If halfway through the effective budget you still have no verified patch:
  1. Re-read the original problem statement for overlooked scope clues.
  2. Search for parallel examples in sibling modules rather than repeatedly inspecting the same files.
  3. Use stack traces or test expectations as the specification.
  4. Produce the most minimal patch that matches the strongest hypothesis; verify with syntax/compile only if deeper verification is impossible.
- If the strongest hypothesis cannot be verified, report the precise file, attempted change, and unresolved check rather than an open-ended summary.

## 7. Finish after verification
- Once a focused verification passes and the diff is minimal, stop. Do not polish comments, reorganize code, or add tests beyond the task unless doing so is necessary for correctness.
- Final state should be a small, self-contained change that a reviewer can understand from `git diff` alone.