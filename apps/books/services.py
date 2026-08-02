from .models import Category, Author,Book,BookCopy
from django.db import models

class CategoryService:

    @staticmethod
    def get_all_categories():
        return Category.objects.all().order_by("name")

    @staticmethod
    def get_category(category_id):
        return Category.objects.get(id=category_id)

    @staticmethod
    def create_category(validated_data):
        return Category.objects.create(**validated_data)

    @staticmethod
    def update_category(category, validated_data):

        for field, value in validated_data.items():
            setattr(category, field, value)

        category.save()

        return category

    @staticmethod
    def delete_category(category):
        category.delete()

class AuthorService:

    @staticmethod
    def get_all_authors():
        return Author.objects.all().order_by("name")

    @staticmethod
    def create_author(validated_data):
        return Author.objects.create(**validated_data)

    @staticmethod
    def update_author(author, validated_data):
        for field, value in validated_data.items():
            setattr(author, field, value)

        author.save()

        return author

    @staticmethod
    def delete_author(author):
        author.delete()

class BookService:

    @staticmethod
    def get_all_books(
        search=None,
        category=None,
        author=None,
        available=None,
    ):
        books = (
            Book.objects
            .select_related("category")
            .prefetch_related("authors", "copies")
            .all()
        )

        if search:
            books = books.filter(
                models.Q(title__icontains=search)
                |models.Q(isbn__icontains=search)
                |models.Q(publisher__icontains=search)
            )

        if category:
            books = books.filter(
                category_id=category
            )

        if author:
            books = books.filter(
                authors__id=author
            )

        if available is True:
            books = books.filter(
                copies__status=BookCopy.Status.AVAILABLE
            )

        if available is False:
            books = books.exclude(
                copies__status=BookCopy.Status.AVAILABLE
            )

        return books.distinct().order_by("title")

    @staticmethod
    def create_book(validated_data):

        authors = validated_data.pop("authors", [])

        book = Book.objects.create(
            **validated_data
        )

        book.authors.set(authors)

        return book

    @staticmethod
    def update_book(book, validated_data):

        authors = validated_data.pop(
            "authors",
            None
        )

        for field, value in validated_data.items():
            setattr(book, field, value)

        book.save()

        if authors is not None:
            book.authors.set(authors)

        return book

    @staticmethod
    def delete_book(book):
        book.delete()


class BookCopyService:

    @staticmethod
    def get_all_copies():
        return (
            BookCopy.objects
            .select_related("book")
            .all()
            .order_by("accession_number")
        )

    @staticmethod
    def create_copy(validated_data):
        return BookCopy.objects.create(**validated_data)

    @staticmethod
    def update_copy(book_copy, validated_data):

        for field, value in validated_data.items():
            setattr(book_copy, field, value)

        book_copy.save()

        return book_copy

    @staticmethod
    def delete_copy(book_copy):
        book_copy.delete()