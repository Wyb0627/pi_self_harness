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
  llm_decider      -- The LLM performs a structured, per-child analysis over
                      stated intent, patch, and own per-task pass/fail, then
                      predicts which premise has the most promising subtree.
                      Forward-looking, no downstream leak.
"""

import json
import random

from llm_client import LLMClient
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

Follow these steps in order:
1. Analyze EVERY child independently before comparing scores. For each child,
   identify:
   - the capability it adds and whether it affects the core agent loop;
   - structural constraints, coupling, brittleness, or irreversible choices;
   - how general the change is across repositories and task families;
   - whether future improvements can compose cleanly on top of it;
   - likely downstream failure modes and repair cost.
2. Compare the children as long-term premises. Explicitly identify any child
   that looks locally successful but risks becoming a toxic stepping stone.
3. Only after the structural comparison, use current score as weak evidence.
   Do not choose the highest score unless the structural analysis independently
   supports it.
4. Select exactly one child.

Return concise, auditable reasoning rather than hidden or unstructured thought.
Reply with a strict JSON object using this schema:
{
  "analysis": [
    {
      "child_id": "<child_id>",
      "capability": "<what it adds>",
      "structural_risks": "<constraints/coupling/brittleness>",
      "evolvability": "<how well future changes can build on it>",
      "downstream_risk": "<likely failures and repair cost>"
    }
  ],
  "comparison": "<why one premise compounds better than the others>",
  "choice": "<child_id>",
  "reason": "<one or two sentence final justification>"
}"""


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
    lines.append(
        "Return JSON only, using the full analysis/comparison/choice/reason "
        "schema from the system prompt."
    )
    return "\n".join(lines)


def greedy_decider(scenario: Scenario) -> str:
    return min(scenario.greedy_children)


def random_decider(scenario: Scenario, rng: random.Random) -> str:
    return rng.choice([c.id for c in scenario.children])


def llm_decider(scenario: Scenario, client: LLMClient) -> tuple[str, str]:
    """Returns (chosen_child_id, reason). Invalid IDs become abstentions."""
    result = client.complete_json(SYSTEM_PROMPT, _build_user_prompt(scenario))
    choice = str(result.get("choice", "")).strip()
    reasoning = {
        "analysis": result.get("analysis", []),
        "comparison": result.get("comparison", ""),
        "reason": result.get("reason", ""),
    }
    reason = json.dumps(reasoning, ensure_ascii=False)
    valid_ids = {c.id for c in scenario.children}
    if choice not in valid_ids:
        # tolerate short-id or prefix answers
        match = [cid for cid in valid_ids if cid.startswith(choice) or choice.startswith(cid)]
        choice = match[0] if len(match) == 1 else ""
        if not choice:
            reason = f"[abstain-invalid-choice] {reason}"
    return choice, reason
