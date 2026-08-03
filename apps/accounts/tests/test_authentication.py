from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User


class RegistrationAPITest(APITestCase):

    def test_student_can_register(self):

        data = {
            "first_name": "Rahul",
            "last_name": "Kumar",
            "email": "rahul@example.com",
            "phone_number": "9876543210",
            "password": "Test@12345",
            "confirm_password": "Test@12345",
        }

        response = self.client.post(
            reverse("register"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                email="rahul@example.com"
            ).exists()
        )

        user = User.objects.get(
            email="rahul@example.com"
        )

        self.assertEqual(
            user.role,
            "STUDENT"
        )
    def test_duplicate_email_registration_fails(self):

        User.objects.create_user(
            email="rahul@example.com",
            password="Test@12345",
            first_name="Rahul",
            last_name="Kumar",
        )

        data = {
            "first_name": "Another",
            "last_name": "User",
            "email": "rahul@example.com",
            "phone_number": "9999999999",
            "password": "Test@12345",
            "confirm_password": "Test@12345",
        }

        response = self.client.post(
            reverse("register"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_password_mismatch_fails(self):

        data = {
            "first_name": "Rahul",
            "last_name": "Kumar",
            "email": "rahul@example.com",
            "phone_number": "9876543210",
            "password": "Test@12345",
            "confirm_password": "Wrong@12345",
        }

        response = self.client.post(
            reverse("register"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

from rest_framework_simplejwt.tokens import RefreshToken


class LoginAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="student@example.com",
            password="Test@12345",
            first_name="Test",
            last_name="Student",
        )

    def test_user_can_login(self):

        data = {
            "email": "student@example.com",
            "password": "Test@12345",
        }

        response = self.client.post(
            reverse("login"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            response.data["data"],
        )

        self.assertIn(
            "refresh",
            response.data["data"],
        )

    def test_login_with_wrong_password_fails(self):

        data = {
            "email": "student@example.com",
            "password": "WrongPassword123",
        }

        response = self.client.post(
            reverse("login"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )