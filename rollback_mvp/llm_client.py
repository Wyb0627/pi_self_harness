"""LLM client via the aicolate OpenAI-compatible gateway.

Currently points at deepseek-v4-flash (see config.LLM_MODEL), mirroring
llm_api_samples/multimodal_sample.py multi_modal_deepseek_v4. Lazy-imports
openai so the offline parts of the experiment run without the dependency.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass

from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL


@dataclass(frozen=True)
class LLMResult:
    data: dict
    input_tokens: int
    output_tokens: int
    latency_seconds: float
    attempts: int
    raw_response: str


class LLMClient:
    def __init__(self, model: str = LLM_MODEL):
        from openai import OpenAI  # lazy: only needed when actually calling

        if not LLM_API_KEY:
            raise RuntimeError(
                "Set ROLLBACK_LLM_API_KEY before running an LLM-backed experiment."
            )
        self.model = model
        self.client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

    def complete_json(self, system: str, user: str, max_retries: int = 3) -> dict:
        """Return the model's reply parsed as JSON.

        The prompt asks for a strict JSON object; we strip common code-fence
        wrapping before parsing and retry on transient failures.
        """
        return self.complete_json_with_telemetry(
            system,
            user,
            max_retries=max_retries,
        ).data

    def complete_json_with_telemetry(
        self,
        system: str,
        user: str,
        max_retries: int = 3,
        max_tokens: int | None = None,
    ) -> LLMResult:
        """Return parsed JSON plus usage, latency, retry, and raw-response data."""
        last_err: Exception | None = None
        started = time.monotonic()
        for attempt in range(1, max_retries + 1):
            try:
                request = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                }
                if max_tokens is not None:
                    request["max_tokens"] = max_tokens
                completion = self.client.chat.completions.create(
                    **request,
                )
                text = completion.choices[0].message.content or ""
                usage = completion.usage
                return LLMResult(
                    data=_parse_json(text),
                    input_tokens=usage.prompt_tokens if usage else 0,
                    output_tokens=usage.completion_tokens if usage else 0,
                    latency_seconds=time.monotonic() - started,
                    attempts=attempt,
                    raw_response=text,
                )
            except Exception as e:  # network or parse
                last_err = e
        raise RuntimeError(f"LLM call failed after {max_retries} tries: {last_err}")


def _parse_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        # strip ```json ... ``` fences
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip().rstrip("`").strip()
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        text = text[start : end + 1]
    return json.loads(text)
