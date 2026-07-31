from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.Role.choices)

def validate_email(self, value):

    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError(
            "Email already registered."
        )

    return value
def validate_phone_number(self, value):

    if len(value) != 10:
        raise serializers.ValidationError(
            "Phone number must contain 10 digits."
        )

    return value
def validate(self, attrs):

    if attrs["password"] != attrs["confirm_password"]:
        raise serializers.ValidationError(
            {
                "confirm_password":
                "Passwords do not match."
            }
        )

    return attrs
def create(self, validated_data):

    validated_data.pop("confirm_password")

    password = validated_data.pop("password")

    user = User.objects.create_user(
        password=password,
        **validated_data
    )

    return user