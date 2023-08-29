from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerAdminOrReadOnly(BasePermission):
    """
    Must be author of the instance or admin
    to edit or delate objects. Other users could only read.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.is_admin
        )
