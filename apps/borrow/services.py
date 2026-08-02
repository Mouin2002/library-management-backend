from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from apps.books.models import BookCopy

from .models import BorrowRecord


class BorrowService:

    @staticmethod
    @transaction.atomic
    def borrow_book(user, book_copy, due_date):

        book_copy = (
            BookCopy.objects
            .select_for_update()
            .get(id=book_copy.id)
        )

        if book_copy.status != BookCopy.Status.AVAILABLE:
            raise ValidationError(
                {
                    "book_copy": "This book copy is not available."
                }
            )

        borrow_record = BorrowRecord.objects.create(
            user=user,
            book_copy=book_copy,
            due_date=due_date,
            status=BorrowRecord.Status.BORROWED,
        )

        book_copy.status = BookCopy.Status.BORROWED
        book_copy.save(update_fields=["status"])

        return borrow_record

    @staticmethod
    def get_user_borrow_records(user):
        return (
            BorrowRecord.objects
            .filter(user=user)
            .select_related(
                "book_copy",
                "book_copy__book"
            )
            .order_by("-borrowed_at")
        )


    @staticmethod
    def get_user_active_borrows(user):
        return (
            BorrowRecord.objects
            .filter(
                user=user,
                status__in=[
                    BorrowRecord.Status.BORROWED,
                    BorrowRecord.Status.OVERDUE,
                ]
            )
            .select_related(
                "book_copy",
                "book_copy__book"
            )
            .order_by("due_date")
        )
    @staticmethod
    @transaction.atomic
    def return_book(user, borrow_record_id):

        borrow_record = (
            BorrowRecord.objects
            .select_for_update()
            .select_related("book_copy")
            .filter(
                id=borrow_record_id,
                user=user
            )
            .first()
        )

        if borrow_record is None:
            raise ValidationError(
                {
                    "borrow_record": "Borrow record not found."
                }
            )

        if borrow_record.status == BorrowRecord.Status.RETURNED:
            raise ValidationError(
                {
                    "borrow_record": "This book has already been returned."
                }
            )

        borrow_record.status = BorrowRecord.Status.RETURNED
        borrow_record.returned_at = timezone.now()

        borrow_record.save(
            update_fields=[
                "status",
                "returned_at",
                "updated_at",
            ]
        )

        book_copy = borrow_record.book_copy

        book_copy.status = BookCopy.Status.AVAILABLE

        book_copy.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return borrow_record
    @staticmethod
    def get_pending_borrows():
        return (
            BorrowRecord.objects
            .filter(
                status__in=[
                    BorrowRecord.Status.BORROWED,
                    BorrowRecord.Status.OVERDUE,
                ]
            )
            .select_related(
                "user",
                "book_copy",
                "book_copy__book",
            )
            .order_by("due_date")
        )
    @staticmethod
    def get_overdue_borrows():

        now = timezone.now()

        BorrowRecord.objects.filter(
            status=BorrowRecord.Status.BORROWED,
            due_date__lt=now,
            returned_at__isnull=True,
        ).update(
            status=BorrowRecord.Status.OVERDUE
        )

        return (
            BorrowRecord.objects
            .filter(
                status=BorrowRecord.Status.OVERDUE,
                returned_at__isnull=True,
            )
            .select_related(
                "user",
                "book_copy",
                "book_copy__book",
            )
            .order_by("due_date")
        )