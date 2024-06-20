import unittest
from main import flask_app  # zaimportuj swoją aplikację Flask

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Konfiguracja aplikacji testowej
        flask_app.config['TESTING'] = True
        self.app = flask_app.test_client()

    def test_home_redirect(self):
        # Test, czy strona główna przekierowuje na odpowiedni URL
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('http://localhost:8501', response.location)

    def test_404_redirect(self):
        # Test, czy błędna strona przekierowuje na stronę główną Streamlit
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 302)
        self.assertIn('http://localhost:8501', response.location)

if __name__ == '__main__':
    unittest.main()
