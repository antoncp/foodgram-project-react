from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Must be an authenticated superuser or an admin user
    to delete and/or edit objects.
    Other users may only view a single object or a list of objects.

    """
    message = "Editing or deleting this item is not allowed."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser)
            )
        )
