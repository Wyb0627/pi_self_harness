"""Gemini client via the aicolate OpenAI-compatible gateway.

Mirrors llm_api_samples/chat_sample.py chat_gemini. Lazy-imports openai so the
offline parts of the experiment run without the dependency installed.
"""

import json

from config import GEMINI_API_KEY, GEMINI_BASE_URL, GEMINI_MODEL


class GeminiClient:
    def __init__(self, model: str = GEMINI_MODEL):
        from openai import OpenAI  # lazy: only needed when actually calling

        self.model = model
        self.client = OpenAI(api_key=GEMINI_API_KEY, base_url=GEMINI_BASE_URL)

    def complete_json(self, system: str, user: str, max_retries: int = 3) -> dict:
        """Return the model's reply parsed as JSON.

        The prompt asks for a strict JSON object; we strip common code-fence
        wrapping before parsing and retry on transient failures.
        """
        last_err: Exception | None = None
        for _ in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                )
                text = completion.choices[0].message.content or ""
                return _parse_json(text)
            except Exception as e:  # network or parse
                last_err = e
        raise RuntimeError(f"Gemini call failed after {max_retries} tries: {last_err}")


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
