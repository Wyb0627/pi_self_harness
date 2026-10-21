# Verified Failure Evidence

The previous candidate added an `__in` lookup by combining `lookups.In` with
`KeyTransformNumericLookupMixin`. The official evaluator rejected it:

- `test_key_in` failed on dictionary/list JSON values with
  `sqlite3.InterfaceError: unsupported type`.
- `test_key_iregex` also remained failing.

Rollback that candidate. The new repair must preserve `In` lookup semantics
while reusing the existing backend-specific JSON RHS adaptation used by nearby
key-transform equality lookups. Treat this evidence as a causal prior, inspect
the current source, and verify the replacement independently.
