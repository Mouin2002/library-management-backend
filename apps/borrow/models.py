from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models

from apps.books.models import BookCopy


class BorrowRecord(models.Model):

    class Status(models.TextChoices):
        BORROWED = "BORROWED", "Borrowed"
        RETURNED = "RETURNED", "Returned"
        OVERDUE = "OVERDUE", "Overdue"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="borrow_records"
    )

    book_copy = models.ForeignKey(
        BookCopy,
        on_delete=models.PROTECT,
        related_name="borrow_records"
    )
    fine_amount = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0
    )

    borrowed_at = models.DateTimeField(
        auto_now_add=True
    )

    due_date = models.DateTimeField()

    returned_at = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.BORROWED
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
            f"{self.book_copy.accession_number}"
        )