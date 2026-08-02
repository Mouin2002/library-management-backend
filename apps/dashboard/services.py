from django.utils import timezone

from apps.accounts.models import User, UserRole
from apps.books.models import Book, BookCopy
from apps.borrow.models import BorrowRecord
from apps.visitors.models import VisitorRecord


class DashboardService:

    @staticmethod
    def get_dashboard_data():

        today = timezone.localdate()

        total_books = Book.objects.count()

        total_copies = BookCopy.objects.count()

        available_copies = BookCopy.objects.filter(
            status=BookCopy.Status.AVAILABLE
        ).count()

        borrowed_copies = BookCopy.objects.filter(
            status=BookCopy.Status.BORROWED
        ).count()

        damaged_copies = BookCopy.objects.filter(
            status=BookCopy.Status.DAMAGED
        ).count()

        pending_returns = BorrowRecord.objects.filter(
            status__in=[
                BorrowRecord.Status.BORROWED,
                BorrowRecord.Status.OVERDUE,
            ],
            returned_at__isnull=True,
        ).count()

        overdue_books = BorrowRecord.objects.filter(
            due_date__lt=timezone.now(),
            returned_at__isnull=True,
        ).count()

        total_students = User.objects.filter(
            role=UserRole.STUDENT
        ).count()

        current_visitors = VisitorRecord.objects.filter(
            check_out_time__isnull=True
        ).count()

        today_visits = VisitorRecord.objects.filter(
            check_in_time__date=today
        ).count()

        return {
            "total_books": total_books,
            "total_copies": total_copies,
            "available_copies": available_copies,
            "borrowed_copies": borrowed_copies,
            "damaged_copies": damaged_copies,
            "pending_returns": pending_returns,
            "overdue_books": overdue_books,
            "total_students": total_students,
            "current_visitors": current_visitors,
            "today_visits": today_visits,
        }