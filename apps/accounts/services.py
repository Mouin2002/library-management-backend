from .models import User


class AccountService:

    @staticmethod
    def register_user(validated_data):
        return User.objects.create_user(**validated_data)