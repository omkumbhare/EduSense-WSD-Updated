"""
Unit tests for EduSense evaluation benchmark module.
"""

import unittest
from src.evaluation import run_evaluation_benchmark


class TestEvaluation(unittest.TestCase):

    def test_run_benchmark(self):
        res = run_evaluation_benchmark()
        self.assertIn("total_samples", res)
        self.assertIn("custom_accuracy", res)
        self.assertIn("baseline_accuracy", res)
        self.assertEqual(res["total_samples"], 25)
        self.assertGreater(res["custom_accuracy"], 0.0)


if __name__ == "__main__":
    unittest.main()
