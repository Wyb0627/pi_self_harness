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

# Gemini via the aicolate OpenAI-compatible gateway (same as
# llm_api_samples/chat_sample.py chat_gemini). Kept overridable by env so the
# key is not the only source of truth.
GEMINI_BASE_URL = os.environ.get(
    "ROLLBACK_GEMINI_BASE_URL",
    "https://aicolate.tiktok-row.net/ai-gateway/openai/v1",
)
GEMINI_API_KEY = os.environ.get(
    "ROLLBACK_GEMINI_API_KEY",
    "aigateway://gateway/sub_business/i18n_business_144.group_control_mllm"
    "?auth_type=secret&secret_id=xov&secret_key=b6b4fb0424a912700295ec994f24ea8eaa2900bd",
)
GEMINI_MODEL = os.environ.get("ROLLBACK_GEMINI_MODEL", "google/gemini-3.5-flash")

# Where run outputs go.
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
