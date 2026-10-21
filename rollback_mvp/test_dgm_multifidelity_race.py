from __future__ import annotations

import unittest

from dgm_multifidelity_race import hash_order, run_trial
from evo_tree import EvoNode


def arm(node_id: str, solved: int) -> EvoNode:
    tasks = {f"t{index:03}" for index in range(200)}
    return EvoNode(
        id=node_id,
        parent_id="initial",
        entry=None,
        accuracy=solved / 200,
        resolved={f"t{index:03}" for index in range(solved)},
        submitted=tasks,
    )


class DgmMultifidelityRaceTest(unittest.TestCase):
    def test_uniform_full_cost_and_selection(self) -> None:
        arms = [arm(f"a{index}", 20 + index * 10) for index in range(8)]
        tasks = tuple(f"t{index:03}" for index in range(200))
        result = run_trial(
            arms,
            tasks,
            "a7",
            "uniform-full",
            tie_seed=1,
        )
        self.assertEqual(result.task_evaluations, 1600)
        self.assertTrue(result.contains_global_best)
        self.assertEqual(result.best_selected_score, 0.45)

    def test_stability_gate_uses_one_finalist_for_stable_leader(self) -> None:
        arms = [arm(f"a{index}", 0) for index in range(7)]
        arms.append(arm("a7", 200))
        tasks = tuple(f"t{index:03}" for index in range(200))
        result = run_trial(
            arms,
            tasks,
            "a7",
            "stability-gated-6",
            tie_seed=1,
        )
        self.assertEqual(result.promoted_after_10, 6)
        self.assertEqual(result.promoted_after_60, 1)
        self.assertEqual(result.task_evaluations, 520)
        self.assertTrue(result.contains_global_best)

    def test_hash_order_is_reproducible(self) -> None:
        tasks = ("a", "b", "c")
        self.assertEqual(
            hash_order(tasks, 7, "test"),
            hash_order(tasks, 7, "test"),
        )
        self.assertNotEqual(
            hash_order(tasks, 7, "test"),
            hash_order(tasks, 8, "test"),
        )


if __name__ == "__main__":
    unittest.main()
