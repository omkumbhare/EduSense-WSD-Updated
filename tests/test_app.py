"""
Flask App Integration Tests for EduSense Web Application.
"""

import unittest
from app import app


class TestAppRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EduSense', response.data)

    def test_analyzer_page_get(self):
        response = self.app.get('/analyzer')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Interactive WSD Analyzer', response.data)

    def test_analyzer_page_post(self):
        response = self.app.post('/analyzer', data={
            'transcript': 'Geologists surveyed the river bank to measure soil erosion.',
            'target_word': 'bank',
            'window_size': 10
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Disambiguation Results', response.data)
        self.assertIn(b'bank.n.01', response.data)

    def test_api_disambiguate(self):
        response = self.app.post('/api/disambiguate', json={
            'transcript': 'The economics lecture covered how a commercial bank manages monetary deposits.',
            'target_word': 'bank',
            'window_size': 10
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['predicted_sense']['synset_name'], 'depository_financial_institution.n.01')

    def test_evaluation_page(self):
        response = self.app.get('/evaluation')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Empirical Evaluation Dashboard', response.data)

    def test_about_page(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Methodology, Architecture', response.data)


if __name__ == '__main__':
    unittest.main()
