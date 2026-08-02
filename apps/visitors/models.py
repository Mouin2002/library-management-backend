from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class VisitorRecord(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="visitor_records"
    )

    check_in_time = models.DateTimeField(
        auto_now_add=True
    )

    check_out_time = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.user.email} - "
            f"{self.check_in_time}"
        )