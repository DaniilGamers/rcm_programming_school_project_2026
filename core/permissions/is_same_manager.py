from rest_framework.permissions import BasePermission


class IsSameManager(BasePermission):
    message = "You cannot comment this order."

    def has_permission(self, request, view):
        return bool(order.manager and order.manager != user_surname)
