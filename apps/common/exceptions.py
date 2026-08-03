from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    # Unexpected exception.
    # Let Django handle it as a normal 500 error.
    if response is None:
        return None

    # Validation errors
    if isinstance(exc, ValidationError):
        return Response(
            {
                "success": False,
                "message": "Validation failed.",
                "errors": response.data,
            },
            status=response.status_code,
        )

    # JWT / authentication errors
    if isinstance(
        exc,
        (NotAuthenticated, AuthenticationFailed),
    ):
        return Response(
            {
                "success": False,
                "message": "Authentication failed.",
                "errors": response.data,
            },
            status=response.status_code,
        )

    # Permission errors
    if isinstance(exc, PermissionDenied):
        return Response(
            {
                "success": False,
                "message": "You do not have permission to perform this action.",
                "errors": response.data,
            },
            status=response.status_code,
        )

    # 404
    if isinstance(exc, NotFound):
        return Response(
            {
                "success": False,
                "message": "Resource not found.",
                "errors": response.data,
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # Other DRF exceptions
    return Response(
        {
            "success": False,
            "message": "Request failed.",
            "errors": response.data,
        },
        status=response.status_code,
    )