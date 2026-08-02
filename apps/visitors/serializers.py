from rest_framework import serializers

from .models import VisitorRecord


class VisitorRecordSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    user_name = serializers.SerializerMethodField()

    class Meta:
        model = VisitorRecord

        fields = [
            "id",
            "user",
            "user_name",
            "user_email",
            "check_in_time",
            "check_out_time",
        ]

        read_only_fields = fields

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()