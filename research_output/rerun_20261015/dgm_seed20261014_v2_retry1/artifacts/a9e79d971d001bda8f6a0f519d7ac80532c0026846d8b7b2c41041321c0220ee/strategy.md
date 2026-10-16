## Strategy: Debugging generated SQL and query-string defects

Most defects in this area are small assembly mistakes. Investigate with a narrow loop.

1. Reproduce with the smallest construction that triggers the bad output. Prefer calling the builder/helper directly instead of running a full integration flow.
2. Trace the generated string backwards. Identify every place that appends a token or joins a list. Write down the actual values of ordering, suffix, condition, and option arguments.
3. Distinguish None, empty string, empty list, and a list containing empty strings. These often behave differently in join/punctuation logic.
4. Isolate the single helper or expression responsible. Print the exact generated fragment before changing anything.
5. Search for all call sites of shared helpers and parallel implementations in other backends before committing to a one-line fix.
6. Fix in the shared helper only if the behavior is common; otherwise fix in the backend-specific compiler/schema module.
7. Add a focused unit test that asserts the exact output string for both the reported edge case and a normal case.
8. Re-check adjacent formatting cases (ordering absent/present, composite expressions, constraints) so punctuation changes do not ripple.

Useful repository anchors: django/db/backends/*/schema.py, django/db/backends/ddl_references.py, and django/db/models/sql/compiler.py.