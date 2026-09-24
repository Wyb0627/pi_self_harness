# Verified Failure Evidence

The exploratory Pi run consumed the 512K total-token budget without producing
a patch.

During cascade collection, Django fetches every column from related objects
even when deletion only needs relation fields. This can decode corrupt or
otherwise unusable values from unrelated columns and also increases query
cost. Inspect the deletion collector and restrict a related queryset to the
fields required for traversal only when signals, parent links, or other
dependencies do not require full model instances. Make the smallest
source-only repair.
