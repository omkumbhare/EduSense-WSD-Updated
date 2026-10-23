"""
Unit tests for EduSense context extraction module.
"""

import unittest
from src.context_extractor import extract_context, find_target_occurrences


class TestContextExtractor(unittest.TestCase):

    def setUp(self):
        self.transcript = "The teacher explained the bank of the river and how water erosion affects the surrounding soil."

    def test_find_occurrences(self):
        occs = find_target_occurrences(self.transcript, "bank")
        self.assertGreaterEqual(len(occs), 1)
        self.assertEqual(occs[0]["token_text"].lower(), "bank")

    def test_extract_context_window(self):
        ctx = extract_context(self.transcript, "bank", window_size=3)
        self.assertTrue(ctx["found"])
        self.assertIn("bank", ctx["context_text"].lower())
        self.assertIn("wsd-highlight", ctx["highlighted_html"])

    def test_missing_target_word(self):
        ctx = extract_context(self.transcript, "quantum", window_size=5)
        self.assertFalse(ctx["found"])
        self.assertIsNotNone(ctx["error_message"])


if __name__ == "__main__":
    unittest.main()
