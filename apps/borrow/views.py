from django.shortcuts import render

# Create your views here.
from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import (
    IsStudent,
    IsAdminOrLibrarian,
)

from .serializers import (
    BorrowBookSerializer,
    BorrowRecordSerializer,
    ReturnBookSerializer,
)
from .services import BorrowService


class BorrowBookAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsStudent,
    ]

    @extend_schema(
        request=BorrowBookSerializer,
        responses={201: BorrowRecordSerializer},
        description="Borrow an available physical book copy",
    )
    def post(self, request):

        serializer = BorrowBookSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        borrow_record = BorrowService.borrow_book(
            user=request.user,
            book_copy=serializer.validated_data["book_copy"],
            due_date=serializer.validated_data["due_date"],
        )

        return Response(
            {
                "success": True,
                "message": "Book borrowed successfully.",
                "data": BorrowRecordSerializer(
                    borrow_record
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )

class MyBorrowRecordsAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsStudent,
    ]

    @extend_schema(
        responses={200: BorrowRecordSerializer(many=True)},
        description="Get logged-in student's complete borrowing history",
    )
    def get(self, request):

        records = BorrowService.get_user_borrow_records(
            request.user
        )

        serializer = BorrowRecordSerializer(
            records,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class MyActiveBorrowsAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsStudent,
    ]

    @extend_schema(
        responses={200: BorrowRecordSerializer(many=True)},
        description="Get books currently borrowed by logged-in student",
    )
    def get(self, request):

        records = BorrowService.get_user_active_borrows(
            request.user
        )

        serializer = BorrowRecordSerializer(
            records,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class ReturnBookAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsStudent,
    ]

    @extend_schema(
        request=ReturnBookSerializer,
        responses={200: BorrowRecordSerializer},
        description="Return a currently borrowed book",
    )
    def post(self, request):

        serializer = ReturnBookSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        borrow_record = BorrowService.return_book(
            user=request.user,
            borrow_record_id=serializer.validated_data[
                "borrow_record_id"
            ],
        )

        return Response(
            {
                "success": True,
                "message": "Book returned successfully.",
                "data": BorrowRecordSerializer(
                    borrow_record
                ).data,
            },
            status=status.HTTP_200_OK,
        )
class PendingBorrowAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminOrLibrarian,
    ]

    @extend_schema(
        responses={
            200: BorrowRecordSerializer(many=True)
        },
        description="Get all books pending for return",
    )
    def get(self, request):

        records = BorrowService.get_pending_borrows()

        serializer = BorrowRecordSerializer(
            records,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class OverdueBorrowAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminOrLibrarian,
    ]

    @extend_schema(
        responses={
            200: BorrowRecordSerializer(many=True)
        },
        description="Get all overdue books",
    )
    def get(self, request):

        records = BorrowService.get_overdue_borrows()

        serializer = BorrowRecordSerializer(
            records,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )