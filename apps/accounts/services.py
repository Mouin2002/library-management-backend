from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class AccountService:

    @staticmethod
    def register_user(validated_data):
        return User.objects.create_user(**validated_data)

    @staticmethod
    def login_user(email, password):

        user = authenticate(
            email=email,
            password=password
        )

        if user is None:
            raise AuthenticationFailed(
                "Invalid email or password."
            )

        if not user.is_active:
            raise AuthenticationFailed(
                "Your account is inactive."
            )

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }