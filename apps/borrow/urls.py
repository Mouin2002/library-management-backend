from django.urls import path

from .views import BorrowBookAPIView,MyBorrowRecordsAPIView,MyActiveBorrowsAPIView,ReturnBookAPIView,PendingBorrowAPIView,OverdueBorrowAPIView


urlpatterns = [
    path(
        "issue/",
        BorrowBookAPIView.as_view(),
        name="borrow-book",
    ),

    path(
        "my-books/",
        MyActiveBorrowsAPIView.as_view(),
        name="my-active-borrows",
    ),

    path(
        "my-history/",
        MyBorrowRecordsAPIView.as_view(),
        name="my-borrow-history",
    ),
    path(
    "return/",
    ReturnBookAPIView.as_view(),
    name="return-book",
    ),
    path(
    "pending/",
    PendingBorrowAPIView.as_view(),
    name="pending-borrows",
    ),

    path(
    "overdue/",
    OverdueBorrowAPIView.as_view(),
    name="overdue-borrows",
    ),
]