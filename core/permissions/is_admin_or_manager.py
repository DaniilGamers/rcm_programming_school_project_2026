from rest_framework.permissions import BasePermission


class IsAdminOrManager(BasePermission):
    message = "Only admin or manager can edit order or message order."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))
