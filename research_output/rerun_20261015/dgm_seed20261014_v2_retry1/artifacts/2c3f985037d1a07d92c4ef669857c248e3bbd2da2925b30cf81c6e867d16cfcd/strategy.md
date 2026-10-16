## Reproduce-first root-cause workflow

1. Turn the reported behavior into a minimal executable reproduction before making changes. Prefer a small test or script that exercises only the public API involved; assertions should capture both the current wrong result and the expected result.
2. Identify the responsible code path from the observed output, then read the complete enclosing methods and their callers. Check how neighboring cases are handled (empty input, None, duplicates, ordering, and type coercion) before editing.
3. Apply the smallest, most local change that fixes the root cause. Preserve existing public behavior and error messages unless the report explicitly requires otherwise.
4. Add or extend focused tests at the unit level that would fail before the change and pass after it. Run the closest test module first, then adjacent tests that share the same code path.
5. Review the final diff for necessity: every hunk should map to a concrete behavior change, and no hunk should alter unrelated error handling, formatting, or configuration.
6. For query or SQL-related issues, inspect generated SQL and query counts with the smallest models that reproduce the issue. Use that evidence to decide whether the problem is correctness, performance, or both.
7. When the responsible symbol is unknown, search for distinctive method names, raised exceptions, or SQL fragments across the source tree before editing.