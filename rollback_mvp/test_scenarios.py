from __future__ import annotations

import unittest

from evo_tree import EvoTree
from scenarios import build_scenarios


class ScenarioConstructionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scenarios = build_scenarios(EvoTree.load())

    def test_all_scores_use_one_common_task_set_per_fork(self) -> None:
        self.assertEqual(len(self.scenarios), 11)
        for scenario in self.scenarios:
            self.assertTrue(scenario.comparison_tasks)
            self.assertTrue(
                all(
                    child.n_submitted == len(scenario.comparison_tasks)
                    for child in scenario.children
                )
            )

    def test_oracle_and_greedy_keep_ties_set_valued(self) -> None:
        initial = next(
            scenario
            for scenario in self.scenarios
            if scenario.fork_parent == "initial"
        )
        self.assertEqual(len(initial.greedy_children), 4)
        self.assertEqual(len(initial.oracle_children), 2)
        self.assertFalse(initial.is_disagreement)

    def test_only_one_strict_disagreement_remains(self) -> None:
        strict = [
            scenario for scenario in self.scenarios if scenario.is_disagreement
        ]
        self.assertEqual(len(strict), 1)
        self.assertEqual(strict[0].fork_parent, "20250327_141021_286218")


if __name__ == "__main__":
    unittest.main()
