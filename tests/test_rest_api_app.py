import unittest
from fastapi.testclient import TestClient
from app.rest_api_app import app,lifespan

class TestRestAPIApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.test_user = {
            "name": "Sebastian Malewa Wanjala",
            "email": "sebastian.wanjala@gmail.com",
            "phone": "+254702916648",
            "username": "seba__tian001",
            "password": "1234pass$",
            "location": "Kisumu"
        }
        self.test_update_user = {
            "name": "Sebastian Malewa Wafula",
            "email": "sebastian.wafula4@gmail.com",
            "phone": "+254706330627",
            "username": "seb__tian001",
            "password": "345frttr$",
            "location": "Eldoret"
        }
        self.test_login_user = {
            "username": "seba__tian001",
            "password": "1234pass$"
        }

    def test_welcome_page(self):
        with TestClient(app) as client:
            response = client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["msg"], "Welcome! This shows that the API is up and running fine")

    def test_registration_endpoint(self):
        with TestClient(app) as client:
            response = client.post("/register", json=self.test_user)
            self.assertEqual(response.json()["status_code"], 201)
            self.assertEqual(response.json()["msg"], "User created successfully")
            self.assertEqual(response.json()["registered_user"]["email"], self.test_user["email"])

    def test_login_endpoint(self):
        with TestClient(app) as client:
            client.post("/register", json=self.test_user)
            response = client.post("/login", json=self.test_login_user)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["msg"], "User logged in successfully")
            self.assertEqual(response.json()["logged_in_user"]["email"], self.test_user["email"])

    def test_view_user_endpoint(self):
        with TestClient(app) as client:
            client.post("/register", json=self.test_user)
            response = client.get("/view/1")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["msg"], "User details returned successfully")
            self.assertEqual(response.json()["user"]["email"], self.test_user["email"])

    def test_update_user_endpoint(self):
        with TestClient(app) as client:
            client.post("/register", json=self.test_user)
            response = client.put("/update/1", json=self.test_update_user)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["msg"], "User details updated successfully")
            self.assertEqual(response.json()["updated_user"]["email"], self.test_update_user["email"])
            self.assertEqual(response.json()["updated_user"]["username"], self.test_update_user["username"])