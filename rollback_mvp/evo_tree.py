"""EvoTree: parse DGM's released SWE evolution tree into a navigable structure.

Each node is one DGM coding-agent version. We read from DGM_SWE_ROOT:
  metadata.json      -> parent_commit, entry (mutation label), overall_performance
  self_evo.md        -> the self-modification reasoning (evolution history)
  model_patch.diff   -> the diff relative to the parent
  predictions/*.md   -> full per-task agent trajectory (debug info)

Scoring fields inside overall_performance give per-task pass/fail:
  total_resolved_ids / total_unresolved_ids / total_emptypatch_ids

Subset-intersection rule (see EVOLUTION_ROLLBACK_DIRECTION.md 4.2): DGM uses
staged evaluation (10/60/200 tasks), so nodes are scored on different task
subsets. Any cross-node comparison must be restricted to the intersection of
the two nodes' submitted-task sets, otherwise a task the descendant never ran
looks like a regression.
"""

import json
import os
from dataclasses import dataclass, field

from config import DGM_SWE_ROOT


def _extract_intent(problem_statement: str, max_chars: int = 1200) -> str:
    """Pull the '# To Implement' section (the mutation's stated intent).

    Falls back to the whole statement head if the marker is absent.
    """
    marker = "# To Implement"
    problem_statement = problem_statement or ""
    idx = problem_statement.find(marker)
    text = problem_statement[idx:] if idx >= 0 else problem_statement
    text = text.strip()
    return text[:max_chars] + ("..." if len(text) > max_chars else "")


@dataclass
class EvoNode:
    id: str
    parent_id: str | None
    entry: str | None  # mutation label, e.g. "solve_stochasticity"
    accuracy: float | None  # accuracy_score on this node's submitted subset
    resolved: set[str] = field(default_factory=set)
    submitted: set[str] = field(default_factory=set)  # resolved|unresolved|emptypatch
    dir_path: str = ""
    mutation_intent: str = ""  # the "# To Implement" section from problem_statement

    @property
    def scored(self) -> bool:
        return self.accuracy is not None

    def read_patch(self, max_chars: int = 6000) -> str:
        """The diff relative to the parent (decision-time visible)."""
        path = os.path.join(self.dir_path, "model_patch.diff")
        if not os.path.isfile(path):
            return ""
        with open(path, errors="replace") as f:
            text = f.read()
        return text[:max_chars] + ("\n...[truncated]" if len(text) > max_chars else "")


class EvoTree:
    def __init__(self, nodes: dict[str, EvoNode]):
        self.nodes = nodes
        self.children: dict[str, list[str]] = {nid: [] for nid in nodes}
        for nid, node in nodes.items():
            if node.parent_id in self.children:
                self.children[node.parent_id].append(nid)
        # Deterministic order for reproducibility.
        for nid in self.children:
            self.children[nid].sort()

    @classmethod
    def load(cls, root: str = DGM_SWE_ROOT) -> "EvoTree":
        nodes: dict[str, EvoNode] = {}
        for name in sorted(os.listdir(root)):
            node_dir = os.path.join(root, name)
            meta_path = os.path.join(node_dir, "metadata.json")
            if not os.path.isfile(meta_path):
                continue
            with open(meta_path) as f:
                meta = json.load(f)
            perf = meta.get("overall_performance")
            resolved: set[str] = set()
            submitted: set[str] = set()
            accuracy: float | None = None
            if perf:
                resolved = set(perf.get("total_resolved_ids", []))
                submitted = (
                    resolved
                    | set(perf.get("total_unresolved_ids", []))
                    | set(perf.get("total_emptypatch_ids", []))
                )
                accuracy = perf.get("accuracy_score")
            nodes[name] = EvoNode(
                id=name,
                parent_id=meta.get("parent_commit"),
                entry=meta.get("entry"),
                accuracy=accuracy,
                resolved=resolved,
                submitted=submitted,
                dir_path=node_dir,
                mutation_intent=_extract_intent(meta.get("problem_statement", "")),
            )
        return cls(nodes)

    # --- tree navigation ---

    def ancestors(self, nid: str) -> list[str]:
        """Ancestors from immediate parent up to the root."""
        out: list[str] = []
        cur = self.nodes[nid].parent_id
        while cur is not None and cur in self.nodes:
            out.append(cur)
            cur = self.nodes[cur].parent_id
        return out

    def descendants(self, nid: str) -> list[str]:
        out: list[str] = []
        for child in self.children.get(nid, []):
            out.append(child)
            out.extend(self.descendants(child))
        return out

    def path_from_root(self, nid: str) -> list[str]:
        return list(reversed(self.ancestors(nid))) + [nid]

    # --- scored views ---

    def scored_descendants(self, nid: str) -> list[str]:
        return [d for d in self.descendants(nid) if self.nodes[d].scored]

    def subtree_best_accuracy(self, nid: str) -> float | None:
        """Highest accuracy reachable in this node's subtree, including itself.

        This is the strong-version oracle signal (subtree-best). It is a
        gold-label quantity computed from DGM's real downstream results and is
        NOT visible to the rollback decider (see information-isolation rule).
        """
        vals: list[float] = []
        node = self.nodes[nid]
        if node.accuracy is not None:
            vals.append(node.accuracy)
        for d in self.scored_descendants(nid):
            acc = self.nodes[d].accuracy
            if acc is not None:
                vals.append(acc)
        return max(vals) if vals else None

    # --- fair per-task comparison (subset intersection) ---

    def comparable_tasks(self, a: str, b: str) -> set[str]:
        return self.nodes[a].submitted & self.nodes[b].submitted

    def regressed_tasks(self, ancestor: str, descendant: str) -> set[str]:
        """Tasks resolved by the ancestor but not by the descendant, on the
        intersection of their submitted subsets."""
        inter = self.comparable_tasks(ancestor, descendant)
        anc = self.nodes[ancestor]
        desc = self.nodes[descendant]
        return {t for t in inter if t in anc.resolved and t not in desc.resolved}

    def sibling_forks(self, min_scored_children: int = 2) -> list[tuple[str, list[str]]]:
        """Parents with >= min_scored_children scored children."""
        forks = []
        for parent, kids in self.children.items():
            scored_kids = [k for k in kids if self.nodes[k].scored]
            if len(scored_kids) >= min_scored_children:
                forks.append((parent, scored_kids))
        return forks
