## Prefer source archaeology when field order changes behavior

If a failing behavior depends on the order of model field declarations:

1. Find the source module responsible for building model metadata instead of guessing or permuting the user model.
   Use the source_search tool with the exact exception message or the public method name that appears in the traceback.
2. Read the whole function that raises the error. Pay attention to the ordered lists it iterates (for example local_fields, local_concrete_fields, local_many_to_many) and the dictionaries populated from those lists (for example parents, fields_map).
3. Separate semantically different relations that have the same target model.
   A relation explicitly marked as a parent link is not the same as an ordinary relation to that parent model.
   Verify that every branch treats those two cases independently of declaration order.
4. When order matters, prefer changing the predicate or the iteration to be order-independent instead of reordering user declarations. A guard that selects the marked parent link is usually a smaller and safer fix.
5. Before editing, search the surrounding source for similar loops over the same metadata list so the fix matches the existing convention.
6. After identifying the intended operation, test both the originally failing order and the reversed order mentally or by running the relevant Django check/validation path; both should pass.