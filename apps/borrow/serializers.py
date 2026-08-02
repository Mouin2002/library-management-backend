from rest_framework import serializers

from apps.books.models import BookCopy
from .models import BorrowRecord


class BorrowBookSerializer(serializers.Serializer):
    book_copy = serializers.PrimaryKeyRelatedField(
        queryset=BookCopy.objects.all()
    )

    due_date = serializers.DateTimeField()


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