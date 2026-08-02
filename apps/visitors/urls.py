from django.urls import path

from .views import (
    CheckInAPIView,
    CheckOutAPIView,
    MyVisitHistoryAPIView,
    CurrentVisitorsAPIView,
    AllVisitorHistoryAPIView,
)


urlpatterns = [
    path(
        "check-in/",
        CheckInAPIView.as_view(),
        name="visitor-check-in"
    ),

    path(
        "check-out/",
        CheckOutAPIView.as_view(),
        name="visitor-check-out"
    ),

    path(
        "my-history/",
        MyVisitHistoryAPIView.as_view(),
        name="my-visit-history"
    ),

    path(
        "current/",
        CurrentVisitorsAPIView.as_view(),
        name="current-visitors"
    ),

    path(
        "history/",
        AllVisitorHistoryAPIView.as_view(),
        name="visitor-history"
    ),
]