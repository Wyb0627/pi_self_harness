# Repair-First Execution Policy

Treat each source edit as a falsifiable causal hypothesis.

1. In the first four tool calls, locate the failing control flow and the
   closest existing tests or analogous implementation.
2. State the invariant violated by the current code. Prefer dataflow,
   dependency-ordering, and expression-compilation explanations over broad
   repository exploration.
3. Make the smallest plausible source edit by the eighth tool call. Do not
   delay implementation while searching for a released fix.
4. Reuse the framework's existing abstraction or lookup mixin before adding a
   parallel implementation.
5. Run the narrowest available local test. If dependencies are unavailable,
   inspect call sites and types, then finish without creating compatibility
   environments.
6. If a candidate edit contradicts local evidence, remove only that edit and
   retain independent useful changes. Stop after one verified minimal repair.
