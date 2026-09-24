# Verified Failure Evidence

The exploratory Pi run consumed the 512K total-token budget without producing
a patch.

The failing lookup is `restaurant__place__country`, where `Restaurant.place`
is a `OneToOneField(primary_key=True)` but is not a concrete inheritance parent.
The current allowlist traversal treats a foreign primary-key relation like a
parent link and shortens the lookup incorrectly. Inspect the model metadata
used by `ModelAdmin.lookup_allowed()` and distinguish an actual parent-link
field from an arbitrary relation that is also the primary key. Make the
smallest source-only repair.
