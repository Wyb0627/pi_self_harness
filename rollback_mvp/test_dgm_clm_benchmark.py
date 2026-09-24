from __future__ import annotations

import json
import os
import tempfile
import unittest

from dgm_clm_benchmark import (
    MacroEdge,
    RecoveryEpisode,
    binary_search,
    clm_boundary_search,
    dgm_score_proxy,
    linear_scan,
    rollback_one,
)
from evo_tree import EvoTree


def make_episode() -> RecoveryEpisode:
    nodes = ("base", "p1", "p2", "p3", "p4")
    return RecoveryEpisode(
        id="episode",
        task_id="task",
        leaf_id="p4",
        nodes=nodes,
        outcomes=(True, False, False, False, False),
        scores=(0.2, 0.5, 0.4, 0.3, 0.25),
        edges=tuple(
            MacroEdge(
                id=child,
                parent_id=parent,
                patch_nodes=(child,),
                evidence=child,
            )
            for parent, child in zip(nodes, nodes[1:])
        ),
        first_bad_index=1,
        monotone=True,
    )


class DgmClmBenchmarkTest(unittest.TestCase):
    def test_delayed_regression_baselines(self) -> None:
        episode = make_episode()
        self.assertFalse(rollback_one(episode).repairs)
        self.assertFalse(dgm_score_proxy(episode).repairs)
        self.assertTrue(linear_scan(episode).exact)
        self.assertTrue(binary_search(episode).exact)

    def test_correct_prior_reduces_probe_calls(self) -> None:
        episode = make_episode()
        clm = clm_boundary_search(episode, ["p1", "p2", "p3", "p4"])
        self.assertTrue(clm.exact)
        self.assertEqual(clm.probe_calls, 1)
        self.assertLessEqual(clm.probe_calls, binary_search(episode).probe_calls)

    def test_loader_counts_error_tasks_as_submitted(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            node_dir = os.path.join(root, "initial")
            result_dir = os.path.join(node_dir, "predictions", "run")
            os.makedirs(result_dir)
            with open(os.path.join(node_dir, "metadata.json"), "w") as file:
                json.dump(
                    {
                        "parent_commit": None,
                        "entry": None,
                        "overall_performance": {
                            "accuracy_score": 0.5,
                            "total_submitted_instances": 2,
                            "total_resolved_ids": ["pass"],
                            "total_unresolved_ids": [],
                            "total_emptypatch_ids": [],
                            "files": [],
                        },
                    },
                    file,
                )
            with open(os.path.join(result_dir, "pass.json"), "w") as file:
                json.dump({}, file)
            with open(os.path.join(result_dir, "error.json"), "w") as file:
                json.dump({}, file)

            node = EvoTree.load(root).nodes["initial"]
            self.assertEqual(node.submitted, {"pass", "error"})
            self.assertEqual(node.resolved, {"pass"})


if __name__ == "__main__":
    unittest.main()
