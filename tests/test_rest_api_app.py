import unittest
from fastapi.testclient import TestClient
from app.rest_api_app import app

class TestRestAPIApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_welcome_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["msg"], "Welcome! This shows that the API is up and running fine")
