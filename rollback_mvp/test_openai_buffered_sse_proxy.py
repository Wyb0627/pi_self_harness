import unittest

from openai_buffered_sse_proxy import response_events


class BufferedSseProxyTest(unittest.TestCase):
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
