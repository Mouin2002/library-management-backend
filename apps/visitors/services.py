from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import VisitorRecord


class VisitorService:

    @staticmethod
    @transaction.atomic
    def check_in(user):

        existing_record = (
            VisitorRecord.objects
            .select_for_update()
            .filter(
                user=user,
                check_out_time__isnull=True
            )
            .first()
        )

        if existing_record:
            raise ValidationError(
                {
                    "visitor": "You are already checked in."
                }
            )

        return VisitorRecord.objects.create(
            user=user
        )

    @staticmethod
    @transaction.atomic
    def check_out(user):

        visitor_record = (
            VisitorRecord.objects
            .select_for_update()
            .filter(
                user=user,
                check_out_time__isnull=True
            )
            .order_by("-check_in_time")
            .first()
        )

        if visitor_record is None:
            raise ValidationError(
                {
                    "visitor": "No active check-in found."
                }
            )

        visitor_record.check_out_time = timezone.now()

        visitor_record.save(
            update_fields=[
                "check_out_time",
                "updated_at",
            ]
        )

        return visitor_record

    @staticmethod
    def get_my_visits(user):

        return (
            VisitorRecord.objects
            .filter(user=user)
            .select_related("user")
            .order_by("-check_in_time")
        )

    @staticmethod
    def get_current_visitors():

        return (
            VisitorRecord.objects
            .filter(
                check_out_time__isnull=True
            )
            .select_related("user")
            .order_by("-check_in_time")
        )

    @staticmethod
    def get_all_visits():

        return (
            VisitorRecord.objects
            .select_related("user")
            .all()
            .order_by("-check_in_time")
        )