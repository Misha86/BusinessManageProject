"""Module with permissions for api application."""

from rest_framework import permissions


class IsBusinessOwnerOrManager(permissions.BasePermission):
    """IsBusinessOwnerOrManager permission class.

    Permission to only allow owners of a business or managers to review and edit it.
    """

    def has_permission(self, request, view):
        """Checks if user belongs to owner or manager group."""
        user = request.user
        return user.is_authenticated and (user.is_manager or user.is_superuser)


class IsBusinessOwnerOrAdmin(permissions.BasePermission):
    """IsBusinessOwnerOrAdmin permission class.

    Permission to only allow owners of a business or admins to review and edit it.
    """

    def has_permission(self, request, view):
        """Checks if user belongs to owner or manager group."""
        user = request.user
        return user.is_authenticated and (user.is_admin or user.is_superuser)


class ReadOnly(permissions.BasePermission):
    """ReadOnly permission class.

    Permission to only allow to review if request.method in ('GET', 'HEAD', 'OPTIONS').
    """

    def has_permission(self, request, view):
        """Checks if request.method in ('GET', 'HEAD', 'OPTIONS')."""
        return request.method in permissions.SAFE_METHODS
