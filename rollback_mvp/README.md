# Rollback MVP: offline diagnosis-guided rollback on DGM's SWE tree

First version validating factors A+B (failure attribution + rollback point
selection) from `EVOLUTION_ROLLBACK_DIRECTION.md` (section 4.2, usage C).

We replay DGM's released SWE evolution tree offline. No Docker, no re-running:
we read DGM's literal tree and per-task scores from
`../DGM_results/swe_results/swe_dgm`.

## What it does

At each sibling fork (a parent with >= 2 scored children), a decider picks the
child that is the best *premise* to keep evolving from. We compare:

- `greedy` -- pick highest own accuracy. DGM-style score-based parent selection.
- `random` -- uniform random (Ours-minus-A ablation, no attribution).
- `llm`    -- Gemini reasons over each child's intent/diff/own results and
              predicts the most promising subtree. Forward-looking.

Each choice is scored against the **subtree-best oracle** (the child whose real
downstream subtree reaches the highest accuracy). Metrics: hit rate and mean
regret (oracle subtree-best minus chosen subtree-best).

### Information isolation (core rule)

The decider sees only decision-time info (child id, mutation intent, patch, own
per-task pass/fail). It never sees downstream subtree results. The oracle uses
real downstream, for scoring only. This keeps the method free of survivorship
bias; the oracle's survivorship bias is a known, documented limitation.

## Setup

```bash
python3 -m pip install openai   # only needed for the llm decider
```

Gemini goes through the aicolate OpenAI-compatible gateway (see `config.py`).
Override with `ROLLBACK_GEMINI_API_KEY` / `ROLLBACK_GEMINI_MODEL` if needed.

## Run

```bash
python3 run.py --offline            # baselines only, no API calls
python3 run.py                      # includes the Gemini decider (11 forks, 5 votes each)
python3 run.py --only-disagreement  # restrict to greedy != oracle forks
```

Results are written to `outputs/results.jsonl`.

## Files

- `config.py`   -- paths and Gemini gateway settings
- `evo_tree.py` -- parse DGM tree; subset-intersection comparison; subtree-best
- `scenarios.py`-- build fork decision points; compute oracle labels
- `deciders.py` -- greedy / random / llm deciders (llm prompt lives here)
- `gemini_client.py` -- Gemini call + JSON parsing
- `scorer.py`   -- hit rate + regret against the oracle
- `run.py`      -- orchestration and comparison report

## Known limits (see EVOLUTION_ROLLBACK_DIRECTION.md 4.2)

- Nodes are DGM's coding-agent code, not pi harness: this validates the rollback
  decider, not a pi harness loop.
- Tree is shallow (83 nodes, 53 leaves); only 4 of 11 forks are disagreement
  cases. Case-study evidence, not statistically significant.
- Factor C (re-evolution after rollback) is not testable offline; it needs real
  runs (Docker), deferred to the main-result stage.
