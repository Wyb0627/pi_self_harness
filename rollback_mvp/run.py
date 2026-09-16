"""Run the offline rollback-decision experiment.

Compares three deciders on DGM's real SWE evolution-tree forks:
  greedy  -- DGM-style score-based parent selection (baseline)
  random  -- no attribution (Ours-minus-A ablation)
  llm     -- Gemini diagnosis-guided rollback (method under test)

Usage:
  python run.py --offline            # baselines only, no API calls
  python run.py                      # includes the Gemini decider
  python run.py --only-disagreement  # restrict to greedy != oracle forks

Each fork is scored against the subtree-best oracle (hit rate + mean regret),
reported over all forks and over the disagreement subset (the thesis cases).
"""

import argparse
import json
import os
import random

from config import OUTPUT_DIR
from deciders import greedy_decider, llm_decider, random_decider
from evo_tree import EvoTree
from scenarios import build_scenarios
from scorer import Judged, judge, summarize


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="skip the Gemini decider")
    parser.add_argument("--only-disagreement", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--llm-repeats", type=int, default=5, help="LLM calls per fork")
    args = parser.parse_args()

    tree = EvoTree.load()
    scenarios = build_scenarios(tree)
    if args.only_disagreement:
        scenarios = [s for s in scenarios if s.is_disagreement]

    n_dis = sum(1 for s in scenarios if s.is_disagreement)
    print(f"Loaded tree: {len(tree.nodes)} nodes, {sum(n.scored for n in tree.nodes.values())} scored")
    print(f"Forks: {len(scenarios)} total, {n_dis} disagreement (greedy != oracle)\n")

    rng = random.Random(args.seed)
    results: list[Judged] = []

    client = None
    if not args.offline:
        from gemini_client import GeminiClient

        client = GeminiClient()

    for s in scenarios:
        results.append(judge(s, "greedy", greedy_decider(s), "highest own accuracy"))
        results.append(judge(s, "random", random_decider(s, rng), "uniform random"))
        if client is not None:
            # Majority vote across repeats to smooth LLM stochasticity.
            votes: dict[str, str] = {}
            counts: dict[str, int] = {}
            for _ in range(args.llm_repeats):
                choice, reason = llm_decider(s, client)
                counts[choice] = counts.get(choice, 0) + 1
                votes[choice] = reason
            best_choice = max(counts, key=lambda c: counts[c])
            results.append(judge(s, "llm", best_choice, votes[best_choice]))

    _report(results, scenarios)
    _save(results)


def _report(results: list[Judged], scenarios) -> None:
    dis_parents = {s.fork_parent for s in scenarios if s.is_disagreement}
    deciders = sorted({j.decider for j in results}, key=lambda d: {"greedy": 0, "random": 1, "llm": 2}.get(d, 9))

    print("=== ALL FORKS ===")
    print(f"{'decider':<10}{'n':>4}{'hit_rate':>10}{'mean_regret':>13}")
    for d in deciders:
        s = summarize([j for j in results if j.decider == d])
        print(f"{d:<10}{s['n']:>4}{s['hit_rate']:>10}{s['mean_regret']:>13}")

    print("\n=== DISAGREEMENT FORKS (greedy != oracle) ===")
    print(f"{'decider':<10}{'n':>4}{'hit_rate':>10}{'mean_regret':>13}")
    for d in deciders:
        s = summarize([j for j in results if j.decider == d and j.fork_parent in dis_parents])
        print(f"{d:<10}{s['n']:>4}{s['hit_rate']:>10}{s['mean_regret']:>13}")

    print("\n=== PER-DISAGREEMENT-FORK DETAIL ===")
    for j in results:
        if j.fork_parent in dis_parents:
            print(f"  [{j.decider:<6}] fork {j.fork_parent[:19]} choice {j.choice[:19]} hit={j.hit} regret={j.regret}")


def _save(results: list[Judged]) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "results.jsonl")
    with open(path, "w") as f:
        for j in results:
            f.write(json.dumps(j.__dict__) + "\n")
    print(f"\nSaved {len(results)} decisions to {path}")


if __name__ == "__main__":
    main()
