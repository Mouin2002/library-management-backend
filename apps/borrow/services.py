from django.db import transaction
from django.utils import timezone

from rest_framework.exceptions import ValidationError

from apps.books.models import BookCopy

from .models import BorrowRecord


class BorrowService:

    # =========================================================
    # BORROW / ISSUE BOOK
    # =========================================================

    @staticmethod
    @transaction.atomic
    def borrow_book(user, book_copy, due_date):

        # Lock the physical copy while processing the request.
        # This helps prevent two users borrowing the same copy
        # at exactly the same time.
        book_copy = (
            BookCopy.objects
            .select_for_update()
            .select_related("book")
            .get(id=book_copy.id)
        )

        # -----------------------------------------------------
        # 1. Check whether the physical copy is available
        # -----------------------------------------------------

        if book_copy.status != BookCopy.Status.AVAILABLE:
            raise ValidationError(
                {
                    "book_copy":
                    "This book copy is not available."
                }
            )

        # -----------------------------------------------------
        # 2. Maximum 3 active books per student
        # -----------------------------------------------------

        active_borrow_count = (
            BorrowRecord.objects
            .filter(
                user=user,
                returned_at__isnull=True,
                status__in=[
                    BorrowRecord.Status.BORROWED,
                    BorrowRecord.Status.OVERDUE,
                ],
            )
            .count()
        )

        if active_borrow_count >= 3:
            raise ValidationError(
                {
                    "borrow":
                    "You cannot borrow more than "
                    "3 books at the same time."
                }
            )

        # -----------------------------------------------------
        # 3. Prevent same student borrowing same book twice
        # -----------------------------------------------------

        already_borrowed = (
            BorrowRecord.objects
            .filter(
                user=user,
                book_copy__book=book_copy.book,
                returned_at__isnull=True,
                status__in=[
                    BorrowRecord.Status.BORROWED,
                    BorrowRecord.Status.OVERDUE,
                ],
            )
            .exists()
        )

        if already_borrowed:
            raise ValidationError(
                {
                    "book":
                    "You already have an active copy "
                    "of this book."
                }
            )

        # -----------------------------------------------------
        # 4. Create borrow record
        # -----------------------------------------------------

        borrow_record = BorrowRecord.objects.create(
            user=user,
            book_copy=book_copy,
            due_date=due_date,
            status=BorrowRecord.Status.BORROWED,
        )

        # -----------------------------------------------------
        # 5. Change physical copy status
        # AVAILABLE -> BORROWED
        # -----------------------------------------------------

        book_copy.status = BookCopy.Status.BORROWED

        book_copy.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return borrow_record

    # =========================================================
    # GET STUDENT COMPLETE BORROW HISTORY
    # =========================================================

    @staticmethod
    def get_user_borrow_records(user):

        return (
            BorrowRecord.objects
            .filter(user=user)
            .select_related(
                "book_copy",
                "book_copy__book",
            )
            .order_by("-borrowed_at")
        )

    # =========================================================
    # GET STUDENT ACTIVE BORROWED BOOKS
    # =========================================================

    @staticmethod
    def get_user_active_borrows(user):

        return (
            BorrowRecord.objects
            .filter(
                user=user,
                returned_at__isnull=True,
                status__in=[
                    BorrowRecord.Status.BORROWED,
                    BorrowRecord.Status.OVERDUE,
                ],
            )
            .select_related(
                "book_copy",
                "book_copy__book",
            )
            .order_by("due_date")
        )

    # =========================================================
    # RETURN BOOK
    # =========================================================

    @staticmethod
    @transaction.atomic
    def return_book(user, borrow_record_id):

        borrow_record = (
            BorrowRecord.objects
            .select_for_update()
            .select_related("book_copy")
            .filter(
                id=borrow_record_id,
                user=user,
            )
            .first()
        )

        # Borrow record doesn't exist for this user
        if borrow_record is None:
            raise ValidationError(
                {
                    "borrow_record":
                    "Borrow record not found."
                }
            )

        # Prevent returning the same book twice
        if (
            borrow_record.status
            == BorrowRecord.Status.RETURNED
        ):
            raise ValidationError(
                {
                    "borrow_record":
                    "This book has already been returned."
                }
            )

        # -----------------------------------------------------
        # Update BorrowRecord
        # -----------------------------------------------------

        borrow_record.status = (
            BorrowRecord.Status.RETURNED
        )

        borrow_record.returned_at = timezone.now()

        borrow_record.save(
            update_fields=[
                "status",
                "returned_at",
                "updated_at",
            ]
        )

        # -----------------------------------------------------
        # Make physical copy available again
        # BORROWED -> AVAILABLE
        # -----------------------------------------------------

        book_copy = borrow_record.book_copy

        book_copy.status = BookCopy.Status.AVAILABLE

        book_copy.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return borrow_record

    # =========================================================
    # ADMIN/LIBRARIAN - PENDING RETURNS
    # =========================================================

    @staticmethod
    def get_pending_borrows():

        return (
            BorrowRecord.objects
            .filter(
                returned_at__isnull=True,
                status__in=[
                    BorrowRecord.Status.BORROWED,
                    BorrowRecord.Status.OVERDUE,
                ],
            )
            .select_related(
                "user",
                "book_copy",
                "book_copy__book",
            )
            .order_by("due_date")
        )

    # =========================================================
    # ADMIN/LIBRARIAN - OVERDUE BOOKS
    # =========================================================

    @staticmethod
    def get_overdue_borrows():

        now = timezone.now()

        # Convert expired BORROWED records to OVERDUE
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