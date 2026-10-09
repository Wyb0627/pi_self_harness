import io
import json
import unittest
import urllib.error
from email.message import Message
from unittest.mock import patch

from openai_buffered_sse_proxy import fetch_completion, response_events


class BufferedSseProxyTest(unittest.TestCase):
    def test_retries_rate_limit_after_minimum_wait(self):
        headers = Message()
        headers["Retry-After"] = "2"
        rate_limit = urllib.error.HTTPError(
            "https://example.test/v1/chat/completions",
            429,
            "rate limited",
            headers,
            io.BytesIO(b'{"error":"rate limited"}'),
        )
        response = io.BytesIO(json.dumps({"choices": []}).encode())

        with (
            patch(
                "openai_buffered_sse_proxy.urllib.request.urlopen",
                side_effect=[rate_limit, response],
            ) as urlopen,
            patch("openai_buffered_sse_proxy.time.sleep") as sleep,
        ):
            payload = fetch_completion(
                "https://example.test/v1",
                {"model": "test"},
                "Bearer test",
                max_rate_limit_retries=1,
                rate_limit_wait_seconds=1,
            )

        self.assertEqual(payload, {"choices": []})
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(2.0)

    def test_does_not_retry_other_http_errors(self):
        headers = Message()
        upstream_error = urllib.error.HTTPError(
            "https://example.test/v1/chat/completions",
            500,
            "server error",
            headers,
            io.BytesIO(b'{"error":"server error"}'),
        )

        with (
            patch(
                "openai_buffered_sse_proxy.urllib.request.urlopen",
                side_effect=upstream_error,
            ),
            patch("openai_buffered_sse_proxy.time.sleep") as sleep,
            self.assertRaises(urllib.error.HTTPError),
        ):
            fetch_completion(
                "https://example.test/v1",
                {"model": "test"},
                "Bearer test",
                max_rate_limit_retries=3,
                rate_limit_wait_seconds=65,
            )

        sleep.assert_not_called()

    def test_converts_text_and_usage(self):
        events = response_events(
            {
                "id": "completion-1",
                "created": 1,
                "model": "test-model",
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": "OK"},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 2, "completion_tokens": 1, "total_tokens": 3},
            }
        )

        self.assertEqual(events[0]["choices"][0]["delta"]["content"], "OK")
        self.assertEqual(events[0]["choices"][0]["finish_reason"], "stop")
        self.assertEqual(events[1]["choices"], [])
        self.assertEqual(events[1]["usage"]["total_tokens"], 3)

    def test_preserves_tool_calls_and_reasoning(self):
        tool_calls = [
            {
                "id": "call-1",
                "type": "function",
                "function": {"name": "read", "arguments": '{"path":"README.md"}'},
            }
        ]
        events = response_events(
            {
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": None,
                            "reasoning_content": "inspect",
                            "tool_calls": tool_calls,
                        },
                        "finish_reason": "tool_calls",
                    }
                ]
            }
        )

        delta = events[0]["choices"][0]["delta"]
        self.assertEqual(delta["reasoning_content"], "inspect")
        self.assertEqual(delta["tool_calls"], tool_calls)


if __name__ == "__main__":
    unittest.main()
