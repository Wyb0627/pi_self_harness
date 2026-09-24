"""Evaluate CLM rollback decisions on DGM's released SWE-bench trajectories.

This is an offline recovery benchmark, not an off-policy reconstruction of what
new agents CLM would have generated. It uses only task outcomes already present
in the DGM release as the replay oracle.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import math
import os
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass

from config import DGM_SWE_ROOT, OUTPUT_DIR
from evo_tree import EvoTree
from llm_client import LLMClient, LLMResult


SYSTEM_PROMPT = """You rank historical code changes for rollback diagnosis.

The current coding-agent version fails one SWE-bench task that the baseline
version solved. Rank the macro-edges by how likely they are to contain the
EARLIEST change that introduced the failure condition. A later change may only
expose an earlier latent defect.

Use only the supplied patch intent, diff, and current failed trajectory. You do
not receive historical pass/fail outcomes or future descendants. The ranking is
a prior: executable replay will verify it.

Return strict JSON:
{
  "ranked_edges": ["<edge id>", "..."],
  "candidate_edges": ["<small high-recall subset>"],
  "reason": "<concise evidence>",
  "confidence": 0.0
}
"""


@dataclass(frozen=True)
class MacroEdge:
    id: str
    parent_id: str
    patch_nodes: tuple[str, ...]
    evidence: str


@dataclass(frozen=True)
class RecoveryEpisode:
    id: str
    task_id: str
    leaf_id: str
    nodes: tuple[str, ...]
    outcomes: tuple[bool, ...]
    scores: tuple[float, ...]
    edges: tuple[MacroEdge, ...]
    first_bad_index: int
    monotone: bool

    @property
    def delayed(self) -> bool:
        return self.first_bad_index < len(self.nodes) - 1


@dataclass(frozen=True)
class Decision:
    method: str
    selected_node: str
    selected_edge: str
    exact: bool
    repairs: bool
    probe_calls: int
    used_fallback: bool = False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm", action="store_true")
    parser.add_argument("--max-episodes", type=int, default=12)
    parser.add_argument("--llm-repeats", type=int, default=3)
    parser.add_argument("--llm-workers", type=int, default=4)
    parser.add_argument("--llm-max-tokens", type=int, default=1200)
    parser.add_argument("--reuse-llm", help="reuse LLM rows from a prior result")
    parser.add_argument("--seed", type=int, default=20260924)
    parser.add_argument(
        "--output",
        default=os.path.join(OUTPUT_DIR, "dgm_clm_benchmark.json"),
    )
    args = parser.parse_args()
    if args.llm and args.reuse_llm:
        parser.error("--llm and --reuse-llm are mutually exclusive")

    tree = EvoTree.load()
    episodes = build_recovery_episodes(tree)
    delayed_monotone = [
        episode for episode in episodes if episode.monotone and episode.delayed
    ]
    selected = deterministic_sample(
        delayed_monotone,
        args.max_episodes,
        args.seed,
    )
    baseline_decisions = [
        decision
        for episode in selected
        for decision in (
            no_rollback(episode),
            rollback_one(episode),
            dgm_score_proxy(episode),
            linear_scan(episode),
            binary_search(episode),
        )
    ]

    result = {
        "schema_version": 1,
        "preregistration": {
            "hypothesis": (
                "On monotone delayed regressions, CLM exact rollback >=0.90, "
                "repair success exceeds rollback-1 and the score-only DGM "
                "proxy, and mean probes do not exceed linear scan."
            ),
            "kill_criterion": (
                "Kill if exact <0.90, repair success does not exceed either "
                "baseline, or mean probes exceed linear scan."
            ),
        },
        "scope": (
            "Offline failure-recovery benchmark over logged DGM trajectories. "
            "It does not estimate counterfactual generated-agent performance."
        ),
        "endpoint_comparison": endpoint_comparison(),
        "census": summarize_census(episodes),
        "selection": {
            "seed": args.seed,
            "max_episodes": args.max_episodes,
            "episode_ids": [episode.id for episode in selected],
            "unique_tasks": len({episode.task_id for episode in selected}),
            "unique_leaves": len({episode.leaf_id for episode in selected}),
        },
        "episodes": [
            {
                "id": episode.id,
                "task_id": episode.task_id,
                "leaf_id": episode.leaf_id,
                "nodes": episode.nodes,
                "outcomes": episode.outcomes,
                "scores": episode.scores,
                "first_bad_index": episode.first_bad_index,
            }
            for episode in selected
        ],
        "baselines": summarize_decisions(baseline_decisions),
        "baseline_decisions": [
            asdict(decision) for decision in baseline_decisions
        ],
        "clm": None,
        "llm_runs": [],
    }

    if args.llm:
        client = LLMClient()
        completed: dict[int, tuple[Decision, list[dict]]] = {}
        with ThreadPoolExecutor(max_workers=args.llm_workers) as executor:
            futures = {
                executor.submit(
                    evaluate_llm_episode,
                    episode,
                    tree,
                    client,
                    args.llm_repeats,
                    args.llm_max_tokens,
                ): index
                for index, episode in enumerate(selected)
            }
            for future in as_completed(futures):
                index = futures[future]
                completed[index] = future.result()
                print(
                    f"[{len(completed)}/{len(selected)}] {selected[index].id}",
                    flush=True,
                )
        clm_decisions = [completed[index][0] for index in range(len(selected))]
        llm_rows = [
            row
            for index in range(len(selected))
            for row in completed[index][1]
        ]

        result["clm"] = {
            "decisions": [asdict(decision) for decision in clm_decisions],
            "summary": summarize_decisions(clm_decisions),
            "llm": {
                "model": client.model,
                "repeats_per_episode": args.llm_repeats,
                "calls": len(llm_rows),
                "top1_accuracy": mean(
                    [row["top1_exact"] for row in llm_rows]
                ),
                "input_tokens": sum(row["input_tokens"] for row in llm_rows),
                "output_tokens": sum(row["output_tokens"] for row in llm_rows),
                "latency_seconds": round(
                    sum(row["latency_seconds"] for row in llm_rows),
                    3,
                ),
                "attempts": sum(row["attempts"] for row in llm_rows),
            },
        }
        result["llm_runs"] = llm_rows
    elif args.reuse_llm:
        with open(args.reuse_llm) as file:
            prior_result = json.load(file)
        if prior_result["selection"]["episode_ids"] != result["selection"]["episode_ids"]:
            raise ValueError("Reused LLM result was generated for a different episode selection.")
        result["clm"] = prior_result["clm"]
        result["clm"]["llm"].pop("reused_from", None)
        if os.path.abspath(args.reuse_llm) != os.path.abspath(args.output):
            result["clm"]["llm"]["reused_from"] = os.path.abspath(args.reuse_llm)
        result["llm_runs"] = prior_result["llm_runs"]

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w") as file:
        json.dump(result, file, indent=2)
        file.write("\n")
    print_report(result)
    print(f"\nSaved result to {args.output}")


def build_recovery_episodes(tree: EvoTree) -> list[RecoveryEpisode]:
    scored_leaves = [
        node_id
        for node_id, node in tree.nodes.items()
        if node.scored and not tree.scored_descendants(node_id)
    ]
    episodes: list[RecoveryEpisode] = []
    seen: set[tuple[tuple[str, ...], str]] = set()
    for leaf_id in scored_leaves:
        full_path = tree.path_from_root(leaf_id)
        nodes = tuple(node_id for node_id in full_path if tree.nodes[node_id].scored)
        if len(nodes) < 2:
            continue
        common_tasks = set.intersection(
            *(tree.nodes[node_id].submitted for node_id in nodes)
        )
        if not common_tasks:
            continue
        scores = tuple(tree.accuracy_on_tasks(node_id, common_tasks) for node_id in nodes)
        edges = build_macro_edges(tree, full_path, nodes)
        for task_id in sorted(common_tasks):
            outcomes = tuple(task_id in tree.nodes[node_id].resolved for node_id in nodes)
            if not outcomes[0] or outcomes[-1]:
                continue
            first_bad_index = outcomes.index(False)
            transitions = sum(
                left != right for left, right in zip(outcomes, outcomes[1:])
            )
            key = (nodes, task_id)
            if key in seen:
                continue
            seen.add(key)
            episodes.append(
                RecoveryEpisode(
                    id=f"{leaf_id}:{task_id}",
                    task_id=task_id,
                    leaf_id=leaf_id,
                    nodes=nodes,
                    outcomes=outcomes,
                    scores=scores,
                    edges=edges,
                    first_bad_index=first_bad_index,
                    monotone=transitions == 1,
                )
            )
    return episodes


def build_macro_edges(
    tree: EvoTree,
    full_path: list[str],
    scored_nodes: tuple[str, ...],
) -> tuple[MacroEdge, ...]:
    positions = {node_id: index for index, node_id in enumerate(full_path)}
    edges: list[MacroEdge] = []
    for parent_id, child_id in zip(scored_nodes, scored_nodes[1:]):
        segment = full_path[positions[parent_id] + 1 : positions[child_id] + 1]
        evidence_parts = []
        for node_id in segment:
            node = tree.nodes[node_id]
            evidence_parts.append(
                "\n".join(
                    [
                        f"label: {node.entry or '(none)'}",
                        f"intent: {trim(node.mutation_intent, 800)}",
                        f"diff:\n{trim(node.read_patch(max_chars=2400), 2400)}",
                    ]
                )
            )
        edges.append(
            MacroEdge(
                id=child_id,
                parent_id=parent_id,
                patch_nodes=tuple(segment),
                evidence="\n\n".join(evidence_parts),
            )
        )
    return tuple(edges)


def rank_with_llm(
    episode: RecoveryEpisode,
    tree: EvoTree,
    client: LLMClient,
    max_tokens: int,
) -> LLMResult:
    lines = [
        "The current version fails the target task.",
        "",
        "Current failed trajectory excerpt:",
        read_failure_excerpt(tree.nodes[episode.leaf_id].dir_path, episode.task_id),
        "",
        "Candidate macro-edges, oldest to newest:",
    ]
    for index, edge in enumerate(episode.edges, start=1):
        lines.extend(
            [
                "",
                f"=== edge_id: e{index} ===",
                edge.evidence,
            ]
        )
    lines.append("\nRank every edge_id exactly once. Return JSON only.")
    return client.complete_json_with_telemetry(
        SYSTEM_PROMPT,
        "\n".join(lines),
        max_tokens=max_tokens,
    )


def evaluate_llm_episode(
    episode: RecoveryEpisode,
    tree: EvoTree,
    client: LLMClient,
    repeats: int,
    max_tokens: int,
) -> tuple[Decision, list[dict]]:
    rankings: list[list[str]] = []
    rows: list[dict] = []
    edge_ids = [edge.id for edge in episode.edges]
    aliases = {f"e{index}": edge.id for index, edge in enumerate(episode.edges, start=1)}
    target_edge = episode.edges[episode.first_bad_index - 1].id
    for repeat in range(repeats):
        response = rank_with_llm(episode, tree, client, max_tokens)
        alias_ranking = normalize_ranking(
            response.data.get("ranked_edges"),
            list(aliases),
        )
        ranking = [aliases[alias] for alias in alias_ranking]
        rankings.append(ranking)
        rows.append(
            {
                "episode_id": episode.id,
                "repeat": repeat + 1,
                "ranking": ranking,
                "anonymous_ranking": alias_ranking,
                "top1_exact": int(bool(ranking) and ranking[0] == target_edge),
                "input_tokens": response.input_tokens,
                "output_tokens": response.output_tokens,
                "latency_seconds": response.latency_seconds,
                "attempts": response.attempts,
                "raw_response": response.raw_response,
            }
        )
    prior = aggregate_rankings(rankings, edge_ids)
    return clm_boundary_search(episode, prior), rows


def clm_boundary_search(
    episode: RecoveryEpisode,
    prior_order: list[str],
) -> Decision:
    edge_ids = [edge.id for edge in episode.edges]
    edge_to_index = {edge_id: index + 1 for index, edge_id in enumerate(edge_ids)}
    queried: set[int] = set()

    def outcome(index: int) -> bool:
        if index not in (0, len(episode.nodes) - 1):
            queried.add(index)
        return episode.outcomes[index]

    slice_size = math.floor(len(edge_ids) * 0.30)
    candidates = prior_order[:slice_size] if slice_size >= 1 else []
    for edge_id in candidates:
        index = edge_to_index[edge_id]
        if outcome(index - 1) and not outcome(index):
            return decision_for_index(
                "clm-deepseek",
                episode,
                index,
                len(queried),
                used_fallback=False,
            )

    low = 0
    high = len(episode.nodes) - 1
    while high - low > 1:
        middle = (low + high) // 2
        if outcome(middle):
            low = middle
        else:
            high = middle
    return decision_for_index(
        "clm-deepseek",
        episode,
        high,
        len(queried),
        used_fallback=bool(candidates),
    )


def no_rollback(episode: RecoveryEpisode) -> Decision:
    return Decision(
        method="no-rollback",
        selected_node=episode.nodes[-1],
        selected_edge=episode.edges[-1].id,
        exact=False,
        repairs=False,
        probe_calls=0,
    )


def rollback_one(episode: RecoveryEpisode) -> Decision:
    selected_index = len(episode.nodes) - 2
    return decision_for_rollback_node(
        "rollback-1",
        episode,
        selected_index,
    )


def dgm_score_proxy(episode: RecoveryEpisode) -> Decision:
    selected_index = max(
        range(len(episode.nodes) - 1),
        key=lambda index: (episode.scores[index], index),
    )
    return decision_for_rollback_node(
        "dgm-score-proxy",
        episode,
        selected_index,
    )


def linear_scan(episode: RecoveryEpisode) -> Decision:
    calls = sum(
        index not in (0, len(episode.nodes) - 1)
        for index in range(1, episode.first_bad_index + 1)
    )
    return decision_for_index(
        "linear",
        episode,
        episode.first_bad_index,
        calls,
    )


def binary_search(episode: RecoveryEpisode) -> Decision:
    queried: set[int] = set()
    low = 0
    high = len(episode.nodes) - 1
    while high - low > 1:
        middle = (low + high) // 2
        queried.add(middle)
        if episode.outcomes[middle]:
            low = middle
        else:
            high = middle
    return decision_for_index(
        "binary",
        episode,
        high,
        len(queried),
    )


def decision_for_index(
    method: str,
    episode: RecoveryEpisode,
    bad_index: int,
    probe_calls: int,
    used_fallback: bool = False,
) -> Decision:
    return Decision(
        method=method,
        selected_node=episode.nodes[bad_index - 1],
        selected_edge=episode.edges[bad_index - 1].id,
        exact=bad_index == episode.first_bad_index,
        repairs=episode.outcomes[bad_index - 1],
        probe_calls=probe_calls,
        used_fallback=used_fallback,
    )


def decision_for_rollback_node(
    method: str,
    episode: RecoveryEpisode,
    selected_index: int,
) -> Decision:
    return Decision(
        method=method,
        selected_node=episode.nodes[selected_index],
        selected_edge=episode.edges[selected_index].id,
        exact=selected_index == episode.first_bad_index - 1,
        repairs=episode.outcomes[selected_index],
        probe_calls=0,
    )


def endpoint_comparison() -> dict:
    roots = {
        "dgm": DGM_SWE_ROOT,
        "no-open-ended": os.path.join(
            os.path.dirname(DGM_SWE_ROOT),
            "swe_dgm_nodarwin",
        ),
        "no-self-improve": os.path.join(
            os.path.dirname(DGM_SWE_ROOT),
            "swe_dgm_noselfimprove",
        ),
    }
    trees = {name: EvoTree.load(root) for name, root in roots.items()}
    best_ids = {
        name: max(
            (node for node in tree.nodes.values() if node.scored),
            key=lambda node: node.accuracy or 0.0,
        ).id
        for name, tree in trees.items()
    }
    initial = trees["dgm"].nodes["initial"]
    canonical_tasks = set(initial.submitted)
    rows = {
        "dgm-initial-agent": {
            "node_id": "initial",
            "raw_accuracy": initial.accuracy,
            "fixed_d60_accuracy": accuracy(initial.resolved, canonical_tasks),
        }
    }
    for name, node_id in best_ids.items():
        node = trees[name].nodes[node_id]
        rows[name] = {
            "node_id": node_id,
            "raw_accuracy": node.accuracy,
            "fixed_d60_accuracy": accuracy(node.resolved, canonical_tasks),
            "missing_d60_tasks": len(canonical_tasks - node.submitted),
        }
    return {
        "canonical_tasks": len(canonical_tasks),
        "systems": rows,
        "note": (
            "The DGM initial agent is not the pi repository's current agent. "
            "No released original-pi predictions exist on these tasks. Missing "
            "canonical tasks are counted as failures."
        ),
    }


def summarize_census(episodes: list[RecoveryEpisode]) -> dict:
    monotone = [episode for episode in episodes if episode.monotone]
    delayed = [episode for episode in monotone if episode.delayed]
    return {
        "all_failure_episodes": len(episodes),
        "unique_tasks": len({episode.task_id for episode in episodes}),
        "unique_leaves": len({episode.leaf_id for episode in episodes}),
        "monotone": len(monotone),
        "non_monotone": len(episodes) - len(monotone),
        "delayed_monotone": len(delayed),
        "delayed_unique_tasks": len({episode.task_id for episode in delayed}),
        "delayed_unique_leaves": len({episode.leaf_id for episode in delayed}),
        "mean_scored_states_delayed": round(
            mean([len(episode.nodes) for episode in delayed]),
            4,
        ),
    }


def summarize_decisions(decisions: list[Decision]) -> dict:
    methods = sorted({decision.method for decision in decisions})
    return {
        method: {
            "n": len(selected),
            "exact": round(mean([decision.exact for decision in selected]), 4),
            "repair_success": round(
                mean([decision.repairs for decision in selected]),
                4,
            ),
            "mean_probe_calls": round(
                mean([decision.probe_calls for decision in selected]),
                4,
            ),
            "fallback_rate": round(
                mean([decision.used_fallback for decision in selected]),
                4,
            ),
        }
        for method in methods
        if (selected := [decision for decision in decisions if decision.method == method])
    }


def deterministic_sample(
    episodes: list[RecoveryEpisode],
    limit: int,
    seed: int,
) -> list[RecoveryEpisode]:
    ordered = sorted(
        episodes,
        key=lambda episode: hashlib.sha256(
            f"{seed}|{episode.id}".encode()
        ).hexdigest(),
    )
    return ordered[:limit] if limit > 0 else ordered


def aggregate_rankings(
    rankings: list[list[str]],
    edge_ids: list[str],
) -> list[str]:
    scores = {edge_id: 0.0 for edge_id in edge_ids}
    for ranking in rankings:
        for index, edge_id in enumerate(ranking):
            scores[edge_id] += len(edge_ids) - index
    return sorted(
        edge_ids,
        key=lambda edge_id: (-scores[edge_id], edge_ids.index(edge_id)),
    )


def normalize_ranking(value: object, edge_ids: list[str]) -> list[str]:
    supplied = (
        [item for item in value if isinstance(item, str)]
        if isinstance(value, list)
        else []
    )
    valid = [edge_id for edge_id in supplied if edge_id in edge_ids]
    return unique([*valid, *edge_ids])


def read_failure_excerpt(node_dir: str, task_id: str) -> str:
    matches = sorted(
        glob.glob(os.path.join(node_dir, "predictions", "*", f"{task_id}.md"))
    )
    if not matches:
        return "(trajectory unavailable)"
    with open(matches[0], errors="replace") as file:
        text = file.read()
    if len(text) <= 5000:
        return text
    return f"{text[:1800]}\n...[middle truncated]...\n{text[-3000:]}"


def print_report(result: dict) -> None:
    print("=== DATA CENSUS ===")
    for key, value in result["census"].items():
        print(f"{key}: {value}")
    print("\n=== SAME-TASK ENDPOINTS ===")
    endpoint = result["endpoint_comparison"]
    print(f"canonical tasks: {endpoint['canonical_tasks']}")
    for name, row in endpoint["systems"].items():
        print(
            f"{name:<18} raw={row['raw_accuracy']:.4f} "
            f"fixed-d60={row['fixed_d60_accuracy']:.4f}"
        )
    print("\n=== RECOVERY BASELINES ===")
    for method, row in result["baselines"].items():
        print(
            f"{method:<18} n={row['n']:<3} exact={row['exact']:.4f} "
            f"repair={row['repair_success']:.4f} calls={row['mean_probe_calls']:.4f}"
        )
    if result["clm"]:
        print("\n=== CLM + DEEPSEEK ===")
        row = result["clm"]["summary"]["clm-deepseek"]
        print(
            f"clm-deepseek       n={row['n']:<3} exact={row['exact']:.4f} "
            f"repair={row['repair_success']:.4f} calls={row['mean_probe_calls']:.4f}"
        )
        print(json.dumps(result["clm"]["llm"], indent=2))


def accuracy(resolved: set[str], tasks: set[str]) -> float:
    if not tasks:
        raise ValueError("No shared tasks for endpoint comparison.")
    return len(resolved & tasks) / len(tasks)


def mean(values: list[float | int | bool]) -> float:
    return statistics.mean(values) if values else 0.0


def trim(value: str, limit: int) -> str:
    value = value.strip()
    return value[:limit] + ("\n...[truncated]" if len(value) > limit else "")


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


if __name__ == "__main__":
    main()
