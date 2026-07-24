from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.core.models import Tenant, User


class AuthAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tenant = Tenant.objects.create(
            name="Test Corp", slug="test-corp", contact_email="test@test.com"
        )
        self.register_url = reverse("auth-register")
        self.login_url = reverse("auth-login")

    def test_user_registration(self):
        data = {
            "email": "newuser@test.com",
            "username": "newuser",
            "password": "StrongPass@123",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)

    def test_login_invalid_credentials(self):
        data = {"email": "nonexist@test.com", "password": "wrongpass"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_success(self):
        User.objects.create_user(
            email="valid@test.com",
            username="validuser",
            password="Valid@123",
            tenant=self.tenant,
        )
        data = {"email": "valid@test.com", "password": "Valid@123"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
