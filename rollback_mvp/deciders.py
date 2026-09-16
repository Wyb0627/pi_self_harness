"""Rollback deciders: the method under test (LLM) and the baselines.

All deciders take a Scenario and return the child id they would keep growing
from (the "premise" they judge most promising). They see ONLY decision-time
information -- never the subtree-best oracle.

Baselines:
  greedy_decider   -- pick the highest own-accuracy child. This is what DGM's
                      score-based parent selection does. (DGM also adds a
                      child-count novelty term; with fresh forks child counts
                      are ~equal, so greedy-by-score is the faithful stand-in.)
  random_decider   -- pick uniformly at random (Ours-minus-A ablation: no attribution).

Method under test:
  llm_decider      -- Gemini reasons over each child's stated intent, patch, and
                      own per-task pass/fail, then predicts which premise has the
                      most promising subtree. Forward-looking, no downstream leak.
"""

import random

from gemini_client import GeminiClient
from scenarios import Scenario

SYSTEM_PROMPT = """You are analyzing a self-evolving coding agent's evolution tree.
Each node is a version of the agent; an edge is one self-modification.

At a fork, several sibling versions were produced from the same parent. Each
child passed its own evaluation to some degree, but you must judge which child
is the best PREMISE to keep evolving from -- i.e. which one's line of change is
most likely to lead to strong future versions, not just which scores highest now.

A child can score well yet be a dead end: its change may impose a structural
constraint that makes later improvements hard or costly. A lower-scoring child
can be the better stepping stone.

Decide using ONLY the information given (each child's stated change intent, its
code diff, and its current per-task results). You do NOT get to see what the
subtrees actually became. Reason forward.

Reply with a strict JSON object:
{"choice": "<child_id>", "reason": "<one or two sentences>"}"""


def _build_user_prompt(scenario: Scenario) -> str:
    lines = [
        f"Parent version: {scenario.fork_parent}",
        f"Parent change intent: {scenario.parent_intent or '(root / unknown)'}",
        "",
        f"There are {len(scenario.children)} sibling children. Pick the best premise to continue from.",
        "",
    ]
    for i, c in enumerate(scenario.children, 1):
        lines += [
            f"=== Child {i}: {c.id} ===",
            f"Mutation label: {c.entry}",
            f"Own score: resolved {c.n_resolved}/{c.n_submitted} tasks (accuracy {round(c.accuracy, 3)})",
            f"Change intent:\n{c.mutation_intent or '(none)'}",
            f"Code diff (truncated):\n{c.patch or '(none)'}",
            "",
        ]
    lines.append('Respond with JSON only: {"choice": "<child_id>", "reason": "..."}')
    return "\n".join(lines)


def greedy_decider(scenario: Scenario) -> str:
    return max(scenario.children, key=lambda c: c.accuracy).id


def random_decider(scenario: Scenario, rng: random.Random) -> str:
    return rng.choice([c.id for c in scenario.children])


def llm_decider(scenario: Scenario, client: GeminiClient) -> tuple[str, str]:
    """Returns (chosen_child_id, reason). Falls back to greedy on invalid id."""
    result = client.complete_json(SYSTEM_PROMPT, _build_user_prompt(scenario))
    choice = str(result.get("choice", "")).strip()
    reason = str(result.get("reason", "")).strip()
    valid_ids = {c.id for c in scenario.children}
    if choice not in valid_ids:
        # tolerate short-id or prefix answers
        match = [cid for cid in valid_ids if cid.startswith(choice) or choice.startswith(cid)]
        choice = match[0] if match else greedy_decider(scenario)
        reason = f"[fallback] {reason}"
    return choice, reason
