from django.shortcuts import render

# Create your views here.
from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminOrLibrarian

from .serializers import VisitorRecordSerializer
from .services import VisitorService


class CheckInAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={201: VisitorRecordSerializer},
        description="Check into the library",
    )
    def post(self, request):

        visitor_record = VisitorService.check_in(
            request.user
        )

        return Response(
            {
                "success": True,
                "message": "Checked in successfully.",
                "data": VisitorRecordSerializer(
                    visitor_record
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


class CheckOutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: VisitorRecordSerializer},
        description="Check out from the library",
    )
    def post(self, request):

        visitor_record = VisitorService.check_out(
            request.user
        )

        return Response(
            {
                "success": True,
                "message": "Checked out successfully.",
                "data": VisitorRecordSerializer(
                    visitor_record
                ).data,
            },
            status=status.HTTP_200_OK,
        )

class MyVisitHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: VisitorRecordSerializer(many=True)
        },
        description="Get logged-in user's library visit history",
    )
    def get(self, request):

        records = VisitorService.get_my_visits(
            request.user
        )

        return Response(
            {
                "success": True,
                "data": VisitorRecordSerializer(
                    records,
                    many=True
                ).data,
            },
            status=status.HTTP_200_OK,
        )

class CurrentVisitorsAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminOrLibrarian,
    ]

    @extend_schema(
        responses={
            200: VisitorRecordSerializer(many=True)
        },
        description="Get users currently inside the library",
    )
    def get(self, request):

        records = VisitorService.get_current_visitors()

        return Response(
            {
                "success": True,
                "data": VisitorRecordSerializer(
                    records,
                    many=True
                ).data,
            },
            status=status.HTTP_200_OK,
        )

class AllVisitorHistoryAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminOrLibrarian,
    ]

    @extend_schema(
        responses={
            200: VisitorRecordSerializer(many=True)
        },
        description="Get complete library visitor history",
    )
    def get(self, request):

        records = VisitorService.get_all_visits()

        return Response(
            {
                "success": True,
                "data": VisitorRecordSerializer(
                    records,
                    many=True
                ).data,
            },
            status=status.HTTP_200_OK,
        )