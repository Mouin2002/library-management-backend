from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema,OpenApiParameter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminOrLibrarian

from .models import Category,Author,Book,BookCopy
from .serializers import CategorySerializer,AuthorSerializer,BookSerializer,BookCopySerializer
from .services import CategoryService,AuthorService,BookService,BookCopyService


class CategoryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: CategorySerializer(many=True)},
        description="Get all book categories",
    )
    def get(self, request):

        categories = CategoryService.get_all_categories()

        serializer = CategorySerializer(
            categories,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        request=CategorySerializer,
        responses={201: CategorySerializer},
        description="Create a book category",
    )
    def post(self, request):

        self.permission_classes = [
            IsAuthenticated,
            IsAdminOrLibrarian
        ]

        self.check_permissions(request)

        serializer = CategorySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        category = CategoryService.create_category(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Category created successfully.",
                "data": CategorySerializer(category).data
            },
            status=status.HTTP_201_CREATED
        )

class CategoryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_category(self, category_id):

        return get_object_or_404(
            Category,
            id=category_id
        )

    @extend_schema(
        responses={200: CategorySerializer},
        description="Get category details",
    )
    def get(self, request, category_id):

        category = self.get_category(category_id)

        return Response(
            {
                "success": True,
                "data": CategorySerializer(category).data
            }
        )

    @extend_schema(
        request=CategorySerializer,
        responses={200: CategorySerializer},
        description="Update a category",
    )
    def put(self, request, category_id):

        self.permission_classes = [
            IsAuthenticated,
            IsAdminOrLibrarian
        ]

        self.check_permissions(request)

        category = self.get_category(category_id)

        serializer = CategorySerializer(
            category,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        category = CategoryService.update_category(
            category,
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Category updated successfully.",
                "data": CategorySerializer(category).data
            }
        )

    @extend_schema(
        description="Delete a category",
    )
    def delete(self, request, category_id):

        self.permission_classes = [
            IsAuthenticated,
            IsAdminOrLibrarian
        ]

        self.check_permissions(request)

        category = self.get_category(category_id)

        CategoryService.delete_category(category)

        return Response(
            {
                "success": True,
                "message": "Category deleted successfully."
            },
            status=status.HTTP_200_OK
        )

class AuthorListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: AuthorSerializer(many=True)},
        description="Get all authors",
    )
    def get(self, request):

        authors = AuthorService.get_all_authors()

        serializer = AuthorSerializer(
            authors,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        request=AuthorSerializer,
        responses={201: AuthorSerializer},
        description="Create an author",
    )
    def post(self, request):

        self.permission_classes = [
            IsAuthenticated,
            IsAdminOrLibrarian
        ]

        self.check_permissions(request)

        serializer = AuthorSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        author = AuthorService.create_author(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Author created successfully.",
                "data": AuthorSerializer(author).data
            },
            status=status.HTTP_201_CREATED
        )


class AuthorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_author(self, author_id):
        return get_object_or_404(
            Author,
            id=author_id
        )

    @extend_schema(
        responses={200: AuthorSerializer},
        description="Get author details",
    )
    def get(self, request, author_id):

        author = self.get_author(author_id)

        return Response(
            {
                "success": True,
                "data": AuthorSerializer(author).data
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        request=AuthorSerializer,
        responses={200: AuthorSerializer},
        description="Update an author",
    )
    def put(self, request, author_id):

        self.permission_classes = [
            IsAuthenticated,
            IsAdminOrLibrarian
        ]
        self.check_permissions(request)

        author = self.get_author(author_id)

        serializer = AuthorSerializer(
            author,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        author = AuthorService.update_author(
            author,
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Author updated successfully.",
                "data": AuthorSerializer(author).data
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        description="Delete an author",
    )
    def delete(self, request, author_id):

        self.permission_classes = [
            IsAuthenticated,
            IsAdminOrLibrarian
        ]
        self.check_permissions(request)

        author = self.get_author(author_id)

        AuthorService.delete_author(author)

        return Response(
            {
                "success": True,
                "message": "Author deleted successfully."
            },
            status=status.HTTP_200_OK
        )

class BookListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
    parameters=[
        OpenApiParameter(
            name="search",
            type=str,
            description="Search by title, ISBN or publisher",
        ),
        OpenApiParameter(
            name="category",
            type=int,
            description="Filter by category ID",
        ),
        OpenApiParameter(
            name="author",
            type=int,
            description="Filter by author ID",
        ),
        OpenApiParameter(
            name="available",
            type=bool,
            description="Filter by availability",
        ),
        OpenApiParameter(
            name="page",
            type=int,
            description="Page number",
        ),
    ],
    responses={200: BookSerializer(many=True)},
    )
    def get(self, request):
        search = request.query_params.get("search")
        category = request.query_params.get("category")
        author = request.query_params.get("author")
        available = request.query_params.get("available")

        if available is not None:
            available = available.lower() == "true"

        books = BookService.get_all_books(
            search=search,
            category=category,
            author=author,
            available=available,
        )

        paginator = PageNumberPagination()

        page = paginator.paginate_queryset(
            books,
            request,
            view=self
        )

        serializer = BookSerializer(
            page,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )
        @extend_schema(
            responses={200: BookSerializer(many=True)},
            description="Get all books",
        )
        def get(self, request):

            books = BookService.get_all_books()

            serializer = BookSerializer(
                books,
                many=True
            )

            return Response(
                {
                    "success": True,
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

    @extend_schema(
        request=BookSerializer,
        responses={201: BookSerializer},
        description="Create a book",
    )
    def post(self, request):

        self.permission_classes = [
            IsAuthenticated,
            IsAdminOrLibrarian
        ]
        self.check_permissions(request)

        serializer = BookSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        book = BookService.create_book(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Book created successfully.",
                "data": BookSerializer(book).data
            },
            status=status.HTTP_201_CREATED
        )
class BookDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_book(self, book_id):
        return get_object_or_404(
            Book.objects
            .select_related("category")
            .prefetch_related("authors"),
            id=book_id
        )

    @extend_schema(
        responses={200: BookSerializer},
        description="Get book details",
    )
    def get(self, request, book_id):

        book = self.get_book(book_id)

        return Response(
            {
                "success": True,
                "data": BookSerializer(book).data
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        request=BookSerializer,
        responses={200: BookSerializer},
        description="Update a book",
    )
    def put(self, request, book_id):

        self.permission_classes = [
            IsAuthenticated,
            IsAdminOrLibrarian
        ]
        self.check_permissions(request)

        book = self.get_book(book_id)

        serializer = BookSerializer(
            book,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        book = BookService.update_book(
            book,
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Book updated successfully.",
                "data": BookSerializer(book).data
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(description="Delete a book")
    def delete(self, request, book_id):

        self.permission_classes = [
            IsAuthenticated,
            IsAdminOrLibrarian
        ]
        self.check_permissions(request)

        book = self.get_book(book_id)

        BookService.delete_book(book)

        return Response(
            {
                "success": True,
                "message": "Book deleted successfully."
            },
            status=status.HTTP_200_OK
        )

class BookCopyDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_copy(self, copy_id):
        return get_object_or_404(
            BookCopy.objects.select_related("book"),
            id=copy_id
        )

    @extend_schema(
        responses={200: BookCopySerializer},
        description="Get physical book copy details",
    )
    def get(self, request, copy_id):

        book_copy = self.get_copy(copy_id)

        return Response(
            {
                "success": True,
                "data": BookCopySerializer(book_copy).data
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        request=BookCopySerializer,
        responses={200: BookCopySerializer},
        description="Update a physical book copy",
    )
    def put(self, request, copy_id):

        self.permission_classes = [
            IsAuthenticated,
            IsAdminOrLibrarian
        ]
        self.check_permissions(request)

        book_copy = self.get_copy(copy_id)

        serializer = BookCopySerializer(
            book_copy,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        book_copy = BookCopyService.update_copy(
            book_copy,
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Book copy updated successfully.",
                "data": BookCopySerializer(book_copy).data
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(description="Delete a physical book copy")
    def delete(self, request, copy_id):

        self.permission_classes = [
            IsAuthenticated,
            IsAdminOrLibrarian
        ]
        self.check_permissions(request)

        book_copy = self.get_copy(copy_id)

        BookCopyService.delete_copy(book_copy)

        return Response(
            {
                "success": True,
                "message": "Book copy deleted successfully."
            },
            status=status.HTTP_200_OK
        )

class BookCopyListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: BookCopySerializer(many=True)},
        description="Get all physical book copies",
    )
    def get(self, request):

        copies = BookCopyService.get_all_copies()

        return Response(
            {
                "success": True,
                "data": BookCopySerializer(
                    copies,
                    many=True
                ).data
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        request=BookCopySerializer,
        responses={201: BookCopySerializer},
        description="Create a physical book copy",
    )
    def post(self, request):

        self.permission_classes = [
            IsAuthenticated,
            IsAdminOrLibrarian
        ]
        self.check_permissions(request)

        serializer = BookCopySerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        book_copy = BookCopyService.create_copy(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Book copy created successfully.",
                "data": BookCopySerializer(book_copy).data
            },
            status=status.HTTP_201_CREATED
        )