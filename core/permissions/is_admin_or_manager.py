from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "Only admin can block/unblock users."

    def has_permission(self, request):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff and request.user.is_superuser)


class IsManager(BasePermission):
    message = "Only admin can block/unblock users."

    def has_permission(self, request):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
