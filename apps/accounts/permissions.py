from rest_framework.permissions import BasePermission

from .models import UserRole


class IsAdmin(BasePermission):
    message = "Only administrators can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )


class IsLibrarian(BasePermission):
    message = "Only librarians can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.LIBRARIAN
        )


class IsStudent(BasePermission):
    message = "Only students can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.STUDENT
        )


class IsAdminOrLibrarian(BasePermission):
    message = "Only administrators or librarians can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role
            in [UserRole.ADMIN, UserRole.LIBRARIAN]
        )