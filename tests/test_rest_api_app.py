import unittest
from fastapi.testclient import TestClient
from app.rest_api_app import app

class TestRestAPIApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.test_user = {
            "name": "Mtu Wa Kutest",
            "email": "mtuwakutest@gmail.com",
            "phone": "+2547000400600",
            "username": "my_test_01",
            "password": "str$onGP4s$",
            "location": "Nairobi"
        }

    def test_welcome(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["msg"], "Welcome! This shows that the API is up and running fine")

    def test_registration(self):
        response = self.client.post("/register", json=self.test_user)
        self.assertEqual(response.json()["status_code"], 201)
        self.assertEqual(response.json()["msg"], "User created successfully")
        self.assertEqual(response.json()["registered_user"]["email"], self.test_user["email"])

    def test_login(self):
        response = self.client.post("/login", json=self.test_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["msg"], "User logged in successfully")
        self.assertEqual(response.json()["logged_in_user"]["email"], self.test_user["email"])

    def test_view_user(self):
        rsp = self.client.post("/login", json=self.test_user)
        self.assertEqual(rsp.status_code, 200)
        user_id = rsp.json()["logged_in_user"]["id"]
        response = self.client.get(f"/view/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["msg"], "User details returned successfully")
        self.assertEqual(response.json()["viewed_user"]["email"], self.test_user["email"])

    def test_update_user(self):
        rsp = self.client.post("/login", json=self.test_user)
        self.assertEqual(rsp.status_code, 200)
        user_id = rsp.json()["logged_in_user"]["id"]
        response = self.client.put(f"/update/{user_id}", json=self.test_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["msg"], "User details updated successfully")
        self.assertEqual(response.json()["updated_user"]["email"], self.test_user["email"])
        self.assertEqual(response.json()["updated_user"]["username"], self.test_user["username"])