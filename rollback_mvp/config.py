"""Shared configuration for the offline rollback-decision experiment.

First version validates factors A+B (failure attribution + rollback point
selection) by replaying DGM's released SWE evolution tree offline. No Docker,
no re-running: we read DGM's literal tree and per-task scores.

See EVOLUTION_ROLLBACK_DIRECTION.md section 4.2 (usage C) for the design.
"""

import os

# Root of DGM's released SWE results (already extracted in the repo).
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DGM_SWE_ROOT = os.path.join(REPO_ROOT, "DGM_results", "swe_results", "swe_dgm")

# Decision LLM: deepseek-v4-flash via the aicolate OpenAI-compatible gateway
# (same endpoint/key as llm_api_samples/multimodal_sample.py
# multi_modal_deepseek_v4). Kept overridable by env so the key is not the only
# source of truth.
LLM_BASE_URL = os.environ.get(
    "ROLLBACK_LLM_BASE_URL",
    "https://aicolate.tiktok-row.net/ai-gateway/openai/v1",
)
LLM_API_KEY = os.environ.get("ROLLBACK_LLM_API_KEY", "")
LLM_MODEL = os.environ.get("ROLLBACK_LLM_MODEL", "byteplus/deepseek-v4-flash-ga")

# Where run outputs go.
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
