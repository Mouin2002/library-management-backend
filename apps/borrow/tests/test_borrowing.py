from datetime import timedelta

from django.utils import timezone

from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.books.models import Category, Book, BookCopy
from apps.borrow.models import BorrowRecord
from apps.borrow.services import BorrowService


class BorrowServiceTest(APITestCase):

    def setUp(self):

        # ---------------------------------------------
        # Create student
        # ---------------------------------------------
        self.student = User.objects.create_user(
            email="student@example.com",
            password="Test@12345",
            first_name="Test",
            last_name="Student",
        )

        # ---------------------------------------------
        # Create category
        # ---------------------------------------------
        self.category = Category.objects.create(
            name="Programming",
            description="Programming books",
        )

        # ---------------------------------------------
        # Create book
        # ---------------------------------------------
        self.book = Book.objects.create(
            title="Clean Code",
            isbn="9780132350884",
            category=self.category,
            publisher="Prentice Hall",
            description="Software development book",
        )

        # ---------------------------------------------
        # Create physical copy
        # ---------------------------------------------
        self.book_copy = BookCopy.objects.create(
            book=self.book,
            accession_number="LIB-001",
            status=BookCopy.Status.AVAILABLE,
            shelf_location="A-01",
        )

    # =====================================================
    # TEST 1
    # Student can borrow an available book
    # =====================================================

    def test_student_can_borrow_available_book(self):

        due_date = timezone.now() + timedelta(days=14)

        borrow_record = BorrowService.borrow_book(
            user=self.student,
            book_copy=self.book_copy,
            due_date=due_date,
        )

        self.assertIsNotNone(
            borrow_record.id
        )

        self.assertEqual(
            borrow_record.status,
            BorrowRecord.Status.BORROWED,
        )

        self.book_copy.refresh_from_db()

        self.assertEqual(
            self.book_copy.status,
            BookCopy.Status.BORROWED,
        )

    # =====================================================
    # TEST 2
    # Borrow record is created
    # =====================================================

    def test_borrow_record_is_created(self):

        due_date = timezone.now() + timedelta(days=14)

        BorrowService.borrow_book(
            user=self.student,
            book_copy=self.book_copy,
            due_date=due_date,
        )

        self.assertEqual(
            BorrowRecord.objects.count(),
            1,
        )

        record = BorrowRecord.objects.first()

        self.assertEqual(
            record.user,
            self.student,
        )

        self.assertEqual(
            record.book_copy,
            self.book_copy,
        )

    # =====================================================
    # TEST 3
    # Borrowed copy cannot be borrowed again
    # =====================================================

    def test_borrowed_copy_cannot_be_borrowed_again(self):

        due_date = timezone.now() + timedelta(days=14)

        BorrowService.borrow_book(
            user=self.student,
            book_copy=self.book_copy,
            due_date=due_date,
        )

        second_student = User.objects.create_user(
            email="student2@example.com",
            password="Test@12345",
            first_name="Second",
            last_name="Student",
        )

        with self.assertRaises(Exception):

            BorrowService.borrow_book(
                user=second_student,
                book_copy=self.book_copy,
                due_date=due_date,
            )

    # =====================================================
    # TEST 4
    # Same student cannot borrow same title twice
    # =====================================================

    def test_student_cannot_borrow_same_book_twice(self):

        second_copy = BookCopy.objects.create(
            book=self.book,
            accession_number="LIB-002",
            status=BookCopy.Status.AVAILABLE,
            shelf_location="A-02",
        )

        due_date = timezone.now() + timedelta(days=14)

        BorrowService.borrow_book(
            user=self.student,
            book_copy=self.book_copy,
            due_date=due_date,
        )

        with self.assertRaises(Exception):

            BorrowService.borrow_book(
                user=self.student,
                book_copy=second_copy,
                due_date=due_date,
            )

    # =====================================================
    # TEST 5
    # Returning book makes copy available again
    # =====================================================

    def test_return_book_makes_copy_available(self):

        due_date = timezone.now() + timedelta(days=14)

        borrow_record = BorrowService.borrow_book(
            user=self.student,
            book_copy=self.book_copy,
            due_date=due_date,
        )

        BorrowService.return_book(
            user=self.student,
            borrow_record_id=borrow_record.id,
        )

        borrow_record.refresh_from_db()
        self.book_copy.refresh_from_db()

        self.assertEqual(
            borrow_record.status,
            BorrowRecord.Status.RETURNED,
        )

        self.assertIsNotNone(
            borrow_record.returned_at
        )

        self.assertEqual(
            self.book_copy.status,
            BookCopy.Status.AVAILABLE,
        )

    # =====================================================
    # TEST 6
    # On-time return has zero fine
    # =====================================================

    def test_on_time_return_has_zero_fine(self):

        due_date = timezone.now() + timedelta(days=14)

        borrow_record = BorrowService.borrow_book(
            user=self.student,
            book_copy=self.book_copy,
            due_date=due_date,
        )

        BorrowService.return_book(
            user=self.student,
            borrow_record_id=borrow_record.id,
        )

        borrow_record.refresh_from_db()

        self.assertEqual(
            borrow_record.fine_amount,
            0,
        )
    def test_student_cannot_borrow_more_than_three_books(self):

        due_date = timezone.now() + timedelta(days=14)

    # Create three different books and borrow them
        for i in range(3):

            book = Book.objects.create(
                title=f"Programming Book {i}",
                isbn=f"978000000000{i}",
                category=self.category,
                publisher="Test Publisher",
                description="Test book",
            )

            copy = BookCopy.objects.create(
                book=book,
                accession_number=f"LIMIT-{i}",
                status=BookCopy.Status.AVAILABLE,
                shelf_location=f"B-{i}",
            )

            BorrowService.borrow_book(
                user=self.student,
                book_copy=copy,
                due_date=due_date,
            )

    # Create a fourth book
        fourth_book = Book.objects.create(
            title="Fourth Programming Book",
            isbn="9789999999999",
            category=self.category,
            publisher="Test Publisher",
            description="Fourth test book",
        )

        fourth_copy = BookCopy.objects.create(
            book=fourth_book,
            accession_number="LIMIT-4",
            status=BookCopy.Status.AVAILABLE,
            shelf_location="B-04",
        )

    # Fourth active borrow must fail
        with self.assertRaises(Exception):

            BorrowService.borrow_book(
                user=self.student,
                book_copy=fourth_copy,
                due_date=due_date,
            )

    # Student should still have exactly 3 active borrows
        active_count = BorrowRecord.objects.filter(
            user=self.student,
            returned_at__isnull=True,
        ).count()

        self.assertEqual(
            active_count,
            3,
        )

    def test_overdue_return_calculates_fine(self):

    # Make the book already borrowed
        self.book_copy.status = BookCopy.Status.BORROWED
        self.book_copy.save()

    # 3 days overdue
        due_date = timezone.now() - timedelta(days=3)

        borrow_record = BorrowRecord.objects.create(
            user=self.student,
            book_copy=self.book_copy,
            due_date=due_date,
            status=BorrowRecord.Status.BORROWED,
        )

        BorrowService.return_book(
            user=self.student,
            borrow_record_id=borrow_record.id,
        )

        borrow_record.refresh_from_db()

        self.assertEqual(
            borrow_record.status,
            BorrowRecord.Status.RETURNED,
        )

        self.assertEqual(
            borrow_record.fine_amount,
            30,
        )