# Coverage Selection Mechanism Ablation

Evidence level: mechanism-only replay over the frozen DGM-200 catalogue.
The selector action trace is fixed across both arbitration modes.

## Pre-registration

Hypothesis: facility-location arbitration is behaviorally redundant when direct proposals exactly fill capacity. It changes selection only when proposals exceed capacity or when it fills an under-capacity round.

Primary checks:

- Exact-capacity task IDs must be identical.
- Over-capacity modes may differ because only greedy reorders.
- Under-capacity agent-only must select fewer planned tasks.
- Fixed selector traces and selector token usage must remain unchanged.

Kill criterion: any exact-capacity ID difference invalidates the isolation. A future endpoint run must retain greedy completion if real underfilled rounds save less than 20% execution cost or show materially worse regret or false-accept behavior.

## Scenarios

| Scenario | Greedy tasks | Agent-only tasks | Same IDs |
| --- | ---: | ---: | --- |
| exact_direct_budget | 2 | 2 | True |
| over_capacity | 2 | 2 | False |
| under_capacity | 2 | 1 | False |

## Result

- Exact-budget isolation passed: True.
- Over-capacity arbitration differs: True.
- Under-capacity planned task-count reduction in this replay: 50.0%.
- Selector traces remained identical: True.
- Kill criterion triggered: False.

## Interpretation

The mechanism hypothesis survives replay: coverage arbitration is behaviorally redundant only when direct proposals exactly fill the round. Agent-only can save paired executions only when a round is underfilled.

## Limitation

This replay does not estimate SWE-bench quality, regression recall, wall time, or endpoint cost. A valid endpoint ablation still requires a real selector adapter, pinned embedding sidecar, trusted paired round evaluator, and isolated candidate runtime.
