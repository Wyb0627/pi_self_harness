"""Scoring: judge each decider's choice against the subtree-best oracle.

Metrics per scenario (all use DGM's real downstream scores, oracle-side only):
  hit          -- 1 if the chosen child == oracle child (subtree-best), else 0.
  regret       -- oracle subtree-best minus chosen child's subtree-best. 0 means
                  the choice reaches an equally productive subtree; larger is a
                  worse premise. This is the offline analogue of "escape cost".

We report metrics over ALL forks and, separately, over DISAGREEMENT forks
(greedy != oracle), which are the cases where the method is supposed to beat
DGM's greedy parent selection.
"""

from dataclasses import dataclass

from scenarios import Scenario


@dataclass
class Judged:
    fork_parent: str
    decider: str
    choice: str
    reason: str
    hit: int
    regret: float


def judge(scenario: Scenario, decider_name: str, choice: str, reason: str) -> Judged:
    oracle_best = scenario.subtree_best[scenario.oracle_child]
    chosen_best = scenario.subtree_best.get(choice, 0.0)
    return Judged(
        fork_parent=scenario.fork_parent,
        decider=decider_name,
        choice=choice,
        reason=reason,
        hit=int(choice == scenario.oracle_child),
        regret=round(oracle_best - chosen_best, 4),
    )


def summarize(judged: list[Judged]) -> dict[str, float]:
    if not judged:
        return {"n": 0, "hit_rate": 0.0, "mean_regret": 0.0}
    n = len(judged)
    return {
        "n": n,
        "hit_rate": round(sum(j.hit for j in judged) / n, 4),
        "mean_regret": round(sum(j.regret for j in judged) / n, 4),
    }
