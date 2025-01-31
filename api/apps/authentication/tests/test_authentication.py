from rest_framework.test import APITestCase
from apps.authentication.models import User


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_register_user(self):
        data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
        response = self.client.post("/authentication/register/", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_login_user(self):
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post("/authentication/login/", data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
    
    def test_refresh_token(self):
        data = {"username": "testuser", "password": "password123"}
        login_response = self.client.post("/authentication/login/", data)
        refresh_token = login_response.data["refresh"]

        response = self.client.post("/authentication/token/refresh/", {"refresh": refresh_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
