from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminOrLibrarian

from .models import Category
from .serializers import CategorySerializer
from .services import CategoryService


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