# Verified Failure Evidence

The previous candidate changed only the hour lookahead so it accepted signed
minute and second tokens independently. The official evaluator rejected it:

- `test_negative` failed for `-15:30`, `-1:15:30`, `-00:01:01`, `-01:01`,
  and accepted the invalid mixed-sign `-01:-01`.
- `test_parse_postgresql_format` also failed.

Rollback that candidate. Derive the grammar and conversion semantics for a
single leading sign applying to the complete clock-style duration. Preserve
the independently signed PostgreSQL day/time format and existing positive
formats. Make the smallest source-only repair.
