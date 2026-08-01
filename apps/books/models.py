from django.db import models

# Create your models here.
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=150)
    biography = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)

    isbn = models.CharField(
        max_length=20,
        unique=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="books"
    )

    authors = models.ManyToManyField(
        Author,
        related_name="books"
    )

    publisher = models.CharField(
        max_length=150,
        blank=True
    )

    published_date = models.DateField(
        null=True,
        blank=True
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BookCopy(models.Model):

    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        BORROWED = "BORROWED", "Borrowed"
        LOST = "LOST", "Lost"
        DAMAGED = "DAMAGED", "Damaged"

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="copies"
    )

    accession_number = models.CharField(
        max_length=50,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )

    shelf_location = models.CharField(
        max_length=50,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.accession_number} - {self.book.title}"