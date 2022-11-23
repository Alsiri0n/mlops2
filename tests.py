"""
Tests for application
"""
import unittest
from config import Config
from app import create_app


class TestConfig(Config):
    """
    Creating test envs
    """
    TESTING = True


class TestMLOPS(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        """
        Check index page
        """
        response = self.client.get('/')
        html = response.data.decode()
        assert response.status_code == 200
        assert "Hello World" in html


if __name__ == '__main__':
    unittest.main(verbosity=2)
