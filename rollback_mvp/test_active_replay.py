from __future__ import annotations

import unittest

from active_replay import (
    active_sliced_ddmin,
    ReplayOracle,
    SyntheticLineage,
    binary_prefix,
    ddmin,
    failure_first_repair,
    full_ddmin,
    full_repair_ddmin,
    repair_first_ddmin,
    sliced_ddmin,
)


def make_case(
    causes: frozenset[int],
    *,
    candidate_slice: tuple[int, ...] = (0, 1, 2, 3, 4, 5),
    noise_rate: float = 0.0,
    cause_families: tuple[frozenset[int], ...] = (),
) -> SyntheticLineage:
    return SyntheticLineage(
        case_id=7,
        n_edges=6,
        cause_set=causes,
        candidate_slice=candidate_slice,
        prior_order=(2, 4, 1, 5, 0, 3),
        noise_rate=noise_rate,
        cause_families=cause_families,
    )


class ActiveReplayTest(unittest.TestCase):
    def test_ddmin_recovers_interacting_cause_set(self) -> None:
        case = make_case(frozenset({1, 4}))
        oracle = ReplayOracle(case, repeats=1)
        self.assertEqual(ddmin(case.all_edges, oracle), (1, 4))

    def test_full_ddmin_recovers_three_edge_cause(self) -> None:
        case = make_case(frozenset({0, 2, 5}))
        diagnosis = full_ddmin(case, repeats=1)
        self.assertEqual(diagnosis.predicted_set, (0, 2, 5))

    def test_sliced_ddmin_uses_slice_when_complete(self) -> None:
        case = make_case(
            frozenset({1, 4}),
            candidate_slice=(4, 1, 2),
        )
        diagnosis = sliced_ddmin(case, repeats=1)
        self.assertEqual(diagnosis.predicted_set, (1, 4))
        self.assertFalse(diagnosis.used_fallback)

    def test_sliced_ddmin_falls_back_when_slice_misses_cause(self) -> None:
        case = make_case(
            frozenset({1, 4}),
            candidate_slice=(1, 2, 3),
        )
        diagnosis = sliced_ddmin(case, repeats=1)
        self.assertEqual(diagnosis.predicted_set, (1, 4))
        self.assertTrue(diagnosis.used_fallback)

    def test_binary_prefix_finds_trigger_not_earliest_interaction(self) -> None:
        case = make_case(frozenset({1, 4}))
        diagnosis = binary_prefix(case, repeats=1)
        self.assertEqual(diagnosis.predicted_set, (4,))
        self.assertNotEqual(diagnosis.predicted_set, tuple(sorted(case.cause_set)))

    def test_active_sliced_ddmin_stops_on_high_prior_singleton(self) -> None:
        case = make_case(
            frozenset({2}),
            candidate_slice=(2, 4, 1),
        )
        diagnosis = active_sliced_ddmin(case, repeats=1)
        self.assertEqual(diagnosis.predicted_set, (2,))
        self.assertLessEqual(diagnosis.probe_calls, 2)

    def test_repair_first_removes_one_member_of_joint_cause(self) -> None:
        case = make_case(
            frozenset({2, 4}),
            candidate_slice=(2, 4, 1),
        )
        diagnosis = repair_first_ddmin(case, repeats=1)
        self.assertEqual(diagnosis.predicted_set, (2,))
        self.assertFalse(
            case.fails(set(case.all_edges) - set(diagnosis.predicted_set))
        )

    def test_full_repair_ddmin_returns_minimal_removal(self) -> None:
        case = make_case(frozenset({1, 4}))
        diagnosis = full_repair_ddmin(case, repeats=1)
        self.assertEqual(len(diagnosis.predicted_set), 1)
        self.assertTrue(set(diagnosis.predicted_set) <= case.cause_set)

    def test_repair_first_handles_alternative_singleton_causes(self) -> None:
        case = make_case(
            frozenset({1, 4}),
            candidate_slice=(4, 1, 2),
            cause_families=(frozenset({1}), frozenset({4})),
        )
        diagnosis = repair_first_ddmin(case, repeats=1)
        self.assertEqual(diagnosis.predicted_set, (1, 4))
        previous = failure_first_repair(case, repeats=1)
        self.assertFalse(
            case.fails(set(case.all_edges) - set(previous.predicted_set))
        )

    def test_noise_is_reproducible_for_same_case_and_subset(self) -> None:
        case = make_case(frozenset({1}), noise_rate=0.25)
        first = ReplayOracle(case, repeats=3)
        second = ReplayOracle(case, repeats=3)
        self.assertEqual(first((0, 1, 2)), second((0, 1, 2)))


if __name__ == "__main__":
    unittest.main()
