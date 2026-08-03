from rest_framework import serializers
from django.utils import timezone
from apps.books.models import BookCopy
from .models import BorrowRecord
from apps.accounts.models import User

class BorrowBookSerializer(serializers.Serializer):
    book_copy = serializers.PrimaryKeyRelatedField(
        queryset=BookCopy.objects.all()
    )

    due_date = serializers.DateTimeField()

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "Due date must be in the future."
            )

        return value

class BorrowRecordSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    book_title = serializers.CharField(
        source="book_copy.book.title",
        read_only=True
    )

    accession_number = serializers.CharField(
        source="book_copy.accession_number",
        read_only=True
    )

    class Meta:
        model = BorrowRecord

        fields = [
            "id",
            "user",
            "user_email",
            "book_copy",
            "book_title",
            "accession_number",
            "borrowed_at",
            "due_date",
            "returned_at",
            "status",
        ]

        read_only_fields = fields

class ReturnBookSerializer(serializers.Serializer):
    borrow_record_id = serializers.IntegerField(
        min_value=1
    )
class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
        ]

class StudentBorrowSummarySerializer(serializers.Serializer):

    total_borrowed = serializers.IntegerField()

    currently_borrowed = serializers.IntegerField()

    overdue = serializers.IntegerField()

    returned = serializers.IntegerField()

    total_fines = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )

class StudentBorrowReportSerializer(serializers.Serializer):

    student = StudentSerializer()

    summary = StudentBorrowSummarySerializer()

    active_books = BorrowRecordSerializer(
        many=True
    )

    overdue_books = BorrowRecordSerializer(
        many=True
    )

    history = BorrowRecordSerializer(
        many=True
    )