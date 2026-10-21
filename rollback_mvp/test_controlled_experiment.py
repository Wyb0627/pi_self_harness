from __future__ import annotations

import unittest

from controlled_experiment import (
    build_controlled_prompt,
    highest_score_decider,
    judge_controlled,
    load_controlled_cases,
    previous_version_decider,
)


class ControlledExperimentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = load_controlled_cases()

    def test_loads_cases_with_valid_oracles(self) -> None:
        self.assertEqual(len(self.cases), 12)
        for case in self.cases:
            ids = [version.id for version in case.versions]
            rollback_index = ids.index(case.oracle.rollback_to)
            self.assertEqual(
                case.oracle.culprit_edge,
                f"{ids[rollback_index]}->{ids[rollback_index + 1]}",
            )

    def test_prompt_keeps_oracle_hidden_and_debug_is_ablated(self) -> None:
        case = self.cases[0]
        full = build_controlled_prompt(case, include_debug=True)
        no_debug = build_controlled_prompt(case, include_debug=False)

        self.assertIn("Debug evidence:", full)
        self.assertIn(case.failure.debug[0], full)
        self.assertNotIn("Debug evidence:", no_debug)
        self.assertNotIn(case.failure.debug[0], no_debug)
        self.assertNotIn(case.oracle.explanation, full)
        self.assertNotIn(case.oracle.explanation, no_debug)

    def test_scoring_distinguishes_exact_over_and_under_rollback(self) -> None:
        case = self.cases[0]
        exact = judge_controlled(
            case,
            decider="test",
            repeat=0,
            choice=case.oracle.rollback_to,
            culprit_edge=case.oracle.culprit_edge,
            reason="",
        )
        over = judge_controlled(
            case,
            decider="test",
            repeat=0,
            choice=case.versions[0].id,
            culprit_edge="",
            reason="",
        )
        under = judge_controlled(
            case,
            decider="test",
            repeat=0,
            choice=case.versions[-2].id,
            culprit_edge="",
            reason="",
        )

        self.assertEqual((exact.exact, exact.distance, exact.attribution_hit), (1, 0, 1))
        self.assertGreater(over.over_rollback, 0)
        self.assertEqual(over.clears_toxicity, 1)
        self.assertGreater(under.under_rollback, 0)
        self.assertEqual(under.clears_toxicity, 0)

    def test_recent_edge_controls_are_solved_by_rollback_one(self) -> None:
        controls = {
            case.id: case
            for case in self.cases
            if case.id in {"reload-schema-mismatch", "timeout-unit-conversion"}
        }
        self.assertEqual(set(controls), {"reload-schema-mismatch", "timeout-unit-conversion"})
        for case in controls.values():
            self.assertEqual(previous_version_decider(case), case.oracle.rollback_to)

    def test_highest_score_is_not_an_oracle_alias(self) -> None:
        exact = sum(
            highest_score_decider(case) == case.oracle.rollback_to
            for case in self.cases
        )
        self.assertLess(exact, len(self.cases) // 2)


if __name__ == "__main__":
    unittest.main()
