"""
Unit tests for EduSense core WSD engine module.
"""

import unittest
from src.wsd_engine import disambiguate_word


class TestWSDEngine(unittest.TestCase):

    def test_disambiguate_river_bank(self):
        text = "Geologists surveyed the river bank to measure soil erosion along the sloping water edge."
        res = disambiguate_word(text, "bank", window_size=10)
        self.assertTrue(res["success"])
        self.assertEqual(res["predicted_sense"]["synset_name"], "bank.n.01")
        self.assertGreater(res["relative_confidence"], 0.0)

    def test_disambiguate_money_bank(self):
        text = "The economics lecture covered how a commercial bank manages monetary deposits and loan interest rates."
        res = disambiguate_word(text, "bank", window_size=10)
        self.assertTrue(res["success"])
        self.assertEqual(res["predicted_sense"]["synset_name"], "depository_financial_institution.n.01")

    def test_candidate_rankings_order(self):
        text = "Optics physics covers how light waves refract when passing through glass prisms and lenses."
        res = disambiguate_word(text, "light", window_size=10)
        ranks = [c["rank"] for c in res["candidate_rankings"]]
        self.assertEqual(ranks, list(range(1, len(ranks) + 1)))


if __name__ == "__main__":
    unittest.main()
