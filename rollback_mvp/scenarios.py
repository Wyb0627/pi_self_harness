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

from __future__ import annotations

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
    comparison_tasks: tuple[str, ...] = ()
    # Oracle / labels (scoring only, hidden from decider):
    greedy_children: tuple[str, ...] = ()  # all highest own-score children
    oracle_children: tuple[str, ...] = ()  # all subtree-best children
    subtree_best: dict[str, float] = field(default_factory=dict)  # child -> best
    is_disagreement: bool = False  # greedy and oracle sets are disjoint


def build_scenarios(tree: EvoTree, min_scored_children: int = 2) -> list[Scenario]:
    scenarios: list[Scenario] = []
    for parent, scored_kids in tree.sibling_forks(min_scored_children):
        parent_node = tree.nodes[parent]
        branch_nodes = {
            kid: [kid, *tree.scored_descendants(kid)] for kid in scored_kids
        }
        compared_nodes = [
            node_id for nodes in branch_nodes.values() for node_id in nodes
        ]
        common_tasks = set.intersection(
            *(tree.nodes[node_id].submitted for node_id in compared_nodes)
        )
        if not common_tasks:
            continue

        children: list[ChildView] = []
        subtree_best: dict[str, float] = {}
        for kid in scored_kids:
            node = tree.nodes[kid]
            accuracy = tree.accuracy_on_tasks(kid, common_tasks)
            children.append(
                ChildView(
                    id=kid,
                    entry=node.entry,
                    mutation_intent=node.mutation_intent,
                    accuracy=accuracy,
                    patch=node.read_patch(),
                    n_resolved=sum(task in node.resolved for task in common_tasks),
                    n_submitted=len(common_tasks),
                )
            )
            subtree_best[kid] = tree.subtree_best_accuracy_on_tasks(
                kid,
                common_tasks,
            )

        max_own = max(child.accuracy for child in children)
        greedy_children = tuple(
            child.id for child in children if child.accuracy == max_own
        )
        max_subtree = max(subtree_best.values())
        oracle_children = tuple(
            child for child in scored_kids if subtree_best[child] == max_subtree
        )
        scenarios.append(
            Scenario(
                fork_parent=parent,
                parent_entry=parent_node.entry,
                parent_intent=parent_node.mutation_intent,
                children=children,
                comparison_tasks=tuple(sorted(common_tasks)),
                greedy_children=greedy_children,
                oracle_children=oracle_children,
                subtree_best=subtree_best,
                is_disagreement=set(greedy_children).isdisjoint(oracle_children),
            )
        )
    return scenarios
