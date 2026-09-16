"""Build strong-version rollback-decision scenarios from the EvoTree.

A strong-version decision point is a sibling fork (a parent node with >= 2
scored children) where DGM's greedy choice (pick the highest-accuracy child)
disagrees with the subtree-productive choice (the child whose subtree reaches
the best accuracy). These are the cases where DGM's score+novelty parent
selection is systematically wrong and diagnosis-guided rollback should win.

For each scenario we compute two things kept strictly apart:

  decider_view  -- ONLY decision-time information (parent id/intent, each
                   child's id/entry/intent/patch and its own score, plus each
                   child's per-task pass/fail on the parent's subset). No
                   downstream subtree results. This is what the LLM sees.

  oracle        -- the gold label from real downstream: the subtree-best child.
                   Used only for scoring, never shown to the decider.

See EVOLUTION_ROLLBACK_DIRECTION.md 4.2 (usage C, information-isolation rule).
"""

from dataclasses import dataclass, field

from evo_tree import EvoTree


@dataclass
class ChildView:
    id: str
    entry: str | None
    mutation_intent: str
    accuracy: float  # the child's OWN score (decision-time visible)
    patch: str
    n_resolved: int
    n_submitted: int


@dataclass
class Scenario:
    fork_parent: str
    parent_entry: str | None
    parent_intent: str
    children: list[ChildView] = field(default_factory=list)
    # Oracle / labels (scoring only, hidden from decider):
    greedy_child: str = ""  # highest own-accuracy child (what DGM would pick)
    oracle_child: str = ""  # subtree-best child (the productive premise)
    subtree_best: dict[str, float] = field(default_factory=dict)  # child -> best
    is_disagreement: bool = False  # greedy != oracle (the thesis case)


def build_scenarios(tree: EvoTree, min_scored_children: int = 2) -> list[Scenario]:
    scenarios: list[Scenario] = []
    for parent, scored_kids in tree.sibling_forks(min_scored_children):
        parent_node = tree.nodes[parent]
        children: list[ChildView] = []
        subtree_best: dict[str, float] = {}
        for kid in scored_kids:
            node = tree.nodes[kid]
            assert node.accuracy is not None  # scored by construction
            children.append(
                ChildView(
                    id=kid,
                    entry=node.entry,
                    mutation_intent=node.mutation_intent,
                    accuracy=node.accuracy,
                    patch=node.read_patch(),
                    n_resolved=len(node.resolved),
                    n_submitted=len(node.submitted),
                )
            )
            best = tree.subtree_best_accuracy(kid)
            subtree_best[kid] = best if best is not None else node.accuracy

        greedy_child = max(children, key=lambda c: c.accuracy).id
        oracle_child = max(scored_kids, key=lambda k: subtree_best[k])
        scenarios.append(
            Scenario(
                fork_parent=parent,
                parent_entry=parent_node.entry,
                parent_intent=parent_node.mutation_intent,
                children=children,
                greedy_child=greedy_child,
                oracle_child=oracle_child,
                subtree_best=subtree_best,
                is_disagreement=(greedy_child != oracle_child),
            )
        )
    return scenarios
