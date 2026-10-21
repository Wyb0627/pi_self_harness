## Diagnose by tracing behavior to its source

- Start with the observable symptom: rendered output, error message, or generated query. Search the repository for the most distinctive symbol in that symptom, then follow callers from the public API down to the low-level helper that owns the decision.
- Before changing code, locate existing tests around the owning module. Identify the smallest model/form/request fixture needed to turn the symptom into a failing regression test. A focused test is both evidence and a safety net.
- When the fix belongs in a shared rendering or helper path, prefer changing the shared function so all call sites remain consistent. Pay special attention to default, blank, empty, and missing states; these are common sources of subtle behavioral bugs.
- After patching, run the focused regression test and related tests in the same module to confirm no nearby behavior changed.