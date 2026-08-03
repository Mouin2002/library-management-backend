from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from apps.accounts.models import User
from rest_framework.exceptions import ValidationError

from apps.books.models import BookCopy

# BorrowRecord comes from apps/borrow/models.py
from .models import BorrowRecord


class BorrowService:

    # =========================================================
    # ISSUE / BORROW BOOK
    # =========================================================

    @staticmethod
    @transaction.atomic
    def borrow_book(user, book_copy, due_date):

        # Lock this physical copy during the transaction
        book_copy = (
            BookCopy.objects
            .select_for_update()
            .select_related("book")
            .get(id=book_copy.id)
        )

        # 1. Book copy must be available
        if book_copy.status != BookCopy.Status.AVAILABLE:
            raise ValidationError(
                {
                    "book_copy":
                    "This book copy is not available."
                }
            )

        # 2. Student can have maximum 3 active books
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

        # 3. Student cannot borrow another copy
        # of the same book while already holding one
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

        # 4. Create borrow record
        borrow_record = BorrowRecord.objects.create(
            user=user,
            book_copy=book_copy,
            due_date=due_date,
            status=BorrowRecord.Status.BORROWED,
        )

        # 5. Change physical copy to BORROWED
        book_copy.status = BookCopy.Status.BORROWED

        book_copy.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return borrow_record

    # =========================================================
    # STUDENT - COMPLETE BORROW HISTORY
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
    # STUDENT - CURRENTLY BORROWED BOOKS
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

        # Find and lock the student's borrow record
        borrow_record = (
            BorrowRecord.objects
            .select_for_update()
            .select_related(
                "book_copy",
                "book_copy__book",
            )
            .filter(
                id=borrow_record_id,
                user=user,
            )
            .first()
        )

        # Borrow record doesn't exist
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

        # Current return time
        return_time = timezone.now()

        borrow_record.returned_at = return_time
        borrow_record.status = BorrowRecord.Status.RETURNED

        # =====================================================
        # CALCULATE OVERDUE FINE
        # ₹10 PER LATE DAY
        # =====================================================

        if return_time > borrow_record.due_date:

            overdue_duration = (
                return_time - borrow_record.due_date
            )

            overdue_days = overdue_duration.days

            # Example:
            # 1 day + 2 hours late = 2 fine days
            if overdue_duration.seconds > 0:
                overdue_days += 1

            fine_per_day = Decimal("10.00")

            borrow_record.fine_amount = (
                Decimal(overdue_days)
                * fine_per_day
            )

        else:

            # Returned on time
            borrow_record.fine_amount = Decimal("0.00")

        # Save borrow record
        borrow_record.save(
            update_fields=[
                "status",
                "returned_at",
                "fine_amount",
                "updated_at",
            ]
        )

        # =====================================================
        # MAKE BOOK COPY AVAILABLE AGAIN
        # =====================================================

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
    # ADMIN / LIBRARIAN - PENDING RETURNS
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
    # ADMIN / LIBRARIAN - OVERDUE BOOKS
    # =========================================================

    @staticmethod
    def get_overdue_borrows():

        now = timezone.now()

        # Change expired BORROWED records to OVERDUE
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

    @staticmethod
    def get_students():

        return (
            User.objects
            .filter(role="STUDENT")
            .order_by("first_name", "last_name")
            )


    @staticmethod
    def get_student_borrow_report(user_id):

        try:
            student = User.objects.get(
                id=user_id,
                role="STUDENT"
            )

        except User.DoesNotExist:
            raise ValidationError(
                {
                    "student": "Student not found."
                }
            )

        history = (
            BorrowRecord.objects
            .filter(user=student)
            .select_related(
                "book_copy",
                "book_copy__book",
            )
            .order_by("-borrowed_at")
        )

        active_books = history.filter(
            returned_at__isnull=True,
            status__in=[
                BorrowRecord.Status.BORROWED,
                BorrowRecord.Status.OVERDUE,
            ],
        )

        overdue_books = history.filter(
            returned_at__isnull=True,
            due_date__lt=timezone.now(),
        )

        total_borrowed = history.count()

        currently_borrowed = active_books.count()

        overdue_count = overdue_books.count()

        returned_count = history.filter(
            status=BorrowRecord.Status.RETURNED
        ).count()

        total_fines = sum(
            record.fine_amount
            for record in history
        )

        return {
            "student": student,

            "summary": {
                "total_borrowed": total_borrowed,
                "currently_borrowed": currently_borrowed,
                "overdue": overdue_count,
                "returned": returned_count,
                "total_fines": total_fines,
            },

            "active_books": active_books,
            "overdue_books": overdue_books,
            "history": history,
        }