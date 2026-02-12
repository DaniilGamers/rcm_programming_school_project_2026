from rest_framework.permissions import BasePermission


class IsSameManager(BasePermission):
    message = "You cannot comment this order."

    def has_object_permission(self, request, view, obj):

        if not obj.manager:
            return True
        return obj.manager == request.user.name
