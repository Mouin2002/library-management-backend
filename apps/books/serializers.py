from rest_framework import serializers

from .models import Category,Author,Book,BookCopy


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = [
            "id",
            "name",
            "biography",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class BookSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    author_names = serializers.SerializerMethodField()

    class Meta:
        model = Book

        fields = [
            "id",
            "title",
            "isbn",
            "category",
            "category_name",
            "authors",
            "author_names",
            "publisher",
            "published_date",
            "description",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "category_name",
            "author_names",
            "created_at",
            "updated_at",
        ]

    def get_author_names(self, obj):
        return [
            author.name
            for author in obj.authors.all()
        ]

class BookCopySerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(
        source="book.title",
        read_only=True
    )

    class Meta:
        model = BookCopy

        fields = [
            "id",
            "book",
            "book_title",
            "accession_number",
            "status",
            "shelf_location",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "book_title",
            "created_at",
            "updated_at",
        ]