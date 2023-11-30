import unittest
from unittest.mock import patch, Mock
import openai
from ai.embedder import embed
from typing import List


class TestEmbedFunction(unittest.TestCase):
    @patch("openai.Embedding.create")
    def test_valid_input(self, mock_openai: Mock) -> None:
        mock_openai.return_value = {
            "data": [
                {"index": 0, "embedding": [0.1, 0.2, 0.3]},
                {"index": 1, "embedding": [0.4, 0.5, 0.6]},
            ]
        }
        messages: List[str] = ["hello", "world"]
        result = embed(messages)
        self.assertEqual(result, [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])

    def test_empty_strings_in_input(self) -> None:
        messages: List[str] = ["hello", "", "world"]
        result = embed(messages)
        self.assertEqual(len(result), 2)

    def test_invalid_number_of_messages(self) -> None:
        messages: List[str] = []  # Testing with no messages
        with self.assertRaises(AssertionError):
            embed(messages)

        messages = ["message"] * 2001  # Testing with more than 2000 messages
        with self.assertRaises(AssertionError):
            embed(messages)

    @patch("openai.Embedding.create")
    @patch("time.sleep", return_value=None)
    def test_rate_limit_error_handling(
        self, mock_sleep: Mock, mock_openai: Mock
    ) -> None:
        mock_openai.side_effect = [
            openai.error.RateLimitError("rate limit exceeded"),  # type: ignore
            {"data": [{"index": 0, "embedding": [0.1, 0.2, 0.3]}]},
        ]
        messages: List[str] = ["hello"]
        result = embed(messages)
        self.assertEqual(result, [[0.1, 0.2, 0.3]])
        self.assertEqual(mock_openai.call_count, 2)
        mock_sleep.assert_called_once()

    @patch("openai.Embedding.create")
    def test_embedding_order(self, mock_openai: Mock) -> None:
        mock_openai.return_value = {
            "data": [
                {"index": 1, "embedding": [0.4, 0.5, 0.6]},
                {"index": 0, "embedding": [0.1, 0.2, 0.3]},
            ]
        }
        messages: List[str] = ["hello", "world"]
        with self.assertRaises(AssertionError):
            embed(messages)
