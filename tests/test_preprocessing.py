"""
Unit tests for EduSense text preprocessing module.
"""

import unittest
from src.preprocessing import (
    normalize_text,
    tokenize_text,
    remove_punctuation_and_stopwords,
    lemmatize_tokens,
    preprocess_text
)


class TestPreprocessing(unittest.TestCase):

    def test_normalize_text(self):
        raw = "   Hello World!  THIS IS A TEST.  "
        expected = "hello world! this is a test."
        self.assertEqual(normalize_text(raw), expected)

    def test_tokenize_text(self):
        text = "the river bank was eroded by monsoon rain."
        tokens = tokenize_text(text)
        self.assertIn("river", tokens)
        self.assertIn("bank", tokens)

    def test_remove_stopwords(self):
        tokens = ["the", "river", "bank", "was", "eroded"]
        filtered = remove_punctuation_and_stopwords(tokens)
        self.assertNotIn("the", filtered)
        self.assertNotIn("was", filtered)
        self.assertIn("river", filtered)
        self.assertIn("bank", filtered)

    def test_lemmatize_tokens(self):
        tokens = ["banks", "running", "better"]
        lemmas = lemmatize_tokens(tokens)
        self.assertIn("bank", lemmas)
        self.assertIn("run", lemmas)

    def test_preprocess_text_pipeline(self):
        res = preprocess_text("The commercial bank accepts deposits.", preserve_target="bank")
        self.assertIn("bank", res["filtered_tokens"])
        self.assertIn("deposit", res["unique_lemmas"])


if __name__ == "__main__":
    unittest.main()
