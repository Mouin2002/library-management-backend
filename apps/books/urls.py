from django.urls import path

from .views import (
    CategoryListCreateAPIView,
    CategoryDetailAPIView,
    AuthorListCreateAPIView,
    AuthorDetailAPIView,
    BookListCreateAPIView,
    BookDetailAPIView,
    BookCopyListCreateAPIView,
    BookCopyDetailAPIView,
)


urlpatterns = [
    # Categories
    path(
        "categories/",
        CategoryListCreateAPIView.as_view(),
        name="category-list-create",
    ),
    path(
        "categories/<int:category_id>/",
        CategoryDetailAPIView.as_view(),
        name="category-detail",
    ),

    # Authors
    path(
        "authors/",
        AuthorListCreateAPIView.as_view(),
        name="author-list-create",
    ),
    path(
        "authors/<int:author_id>/",
        AuthorDetailAPIView.as_view(),
        name="author-detail",
    ),

    # Books
    path(
        "books/",
        BookListCreateAPIView.as_view(),
        name="book-list-create",
    ),
    path(
        "books/<int:book_id>/",
        BookDetailAPIView.as_view(),
        name="book-detail",
    ),

    # Book Copies
    path(
        "copies/",
        BookCopyListCreateAPIView.as_view(),
        name="book-copy-list-create",
    ),
    path(
        "copies/<int:copy_id>/",
        BookCopyDetailAPIView.as_view(),
        name="book-copy-detail",
    ),
]