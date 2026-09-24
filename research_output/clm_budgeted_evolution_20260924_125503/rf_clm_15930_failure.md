# Verified Failure Evidence

The exploratory Pi run consumed the 512K total-token budget without producing
a patch. It repeatedly inspected `WhereNode`, `Case`, `When`, and
`EmptyResultSet`.

The reproduced SQL contains an empty conditional:

```text
CASE WHEN THEN true ELSE false END
```

The input condition is `~Q(pk__in=[])`, which is logically true. The repair
must preserve this truth value when `When.as_sql()` catches the sentinel raised
while compiling an empty lookup. Do not redesign general query negation; make
the smallest source-only correction at the conditional-expression boundary.
