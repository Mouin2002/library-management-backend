from django.shortcuts import render

# Create your views here.
from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminOrLibrarian

from .serializers import DashboardSerializer
from .services import DashboardService


class DashboardAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminOrLibrarian,
    ]

    @extend_schema(
        responses={200: DashboardSerializer},
        description="Get library dashboard statistics",
    )
    def get(self, request):

        data = DashboardService.get_dashboard_data()

        return Response(
            {
                "success": True,
                "data": data,
            },
            status=status.HTTP_200_OK,
        )