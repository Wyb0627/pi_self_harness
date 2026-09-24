from __future__ import annotations

import unittest

from dgm_budgeted_quarantine import (
    Attempt,
    RULES,
    parse_json_stream,
    replay,
)
from evo_tree import EvoNode, EvoTree


def node(
    node_id: str,
    parent_id: str | None,
    resolved: set[str],
) -> EvoNode:
    return EvoNode(
        id=node_id,
        parent_id=parent_id,
        entry=None,
        accuracy=len(resolved) / 3,
        resolved=resolved,
        submitted={"a", "b", "c"},
    )


class DgmBudgetedQuarantineTest(unittest.TestCase):
    def test_json_stream_parser(self) -> None:
        self.assertEqual(
            parse_json_stream('{\n"a": 1\n}\n{"b": 2}\n'),
            [{"a": 1}, {"b": 2}],
        )

    def test_quarantine_skips_descendants_and_preserves_sibling(self) -> None:
        tree = EvoTree(
            {
                "initial": node("initial", None, {"a", "b"}),
                "toxic": node("toxic", "initial", {"a"}),
                "toxic-child": node("toxic-child", "toxic", {"a", "b", "c"}),
                "good": node("good", "initial", {"a", "b", "c"}),
            }
        )
        attempts = [
            Attempt(0, "toxic"),
            Attempt(1, "toxic-child"),
            Attempt(1, "good"),
        ]
        baseline = replay(
            tree,
            attempts,
            {"a", "b", "c"},
            proposal_cost=1.0,
            rule=None,
            comparison_budget=None,
        )
        policy = replay(
            tree,
            attempts,
            {"a", "b", "c"},
            proposal_cost=1.0,
            rule=RULES[0],
            comparison_budget=baseline["total_cost"],
        )
        self.assertEqual(policy["skipped_node_ids"], ["toxic-child"])
        self.assertEqual(policy["best_fixed_d60"], baseline["best_fixed_d60"])
        self.assertLess(policy["total_cost"], baseline["total_cost"])

    def test_primary_rule_requires_two_lost_tasks(self) -> None:
        tree = EvoTree(
            {
                "initial": node("initial", None, {"a", "b"}),
                "one-loss": node("one-loss", "initial", {"a"}),
            }
        )
        result = replay(
            tree,
            [Attempt(0, "one-loss")],
            {"a", "b", "c"},
            proposal_cost=1.0,
            rule=RULES[1],
            comparison_budget=None,
        )
        self.assertEqual(result["quarantined_count"], 0)


if __name__ == "__main__":
    unittest.main()
