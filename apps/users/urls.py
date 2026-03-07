from django.urls import path

from apps.users.views import StaffView, BlockStaffView, UnblockStaffView, SetPasswordView, ActivateStaffView, MeView

urlpatterns = [
    path('', StaffView.as_view(), name="View staff list"),
    path('/create', StaffView.as_view(), name="Create new manager"),
    path('/<int:pk>/block', BlockStaffView.as_view(), name="Block the manager"),
    path('/<int:pk>/unblock', UnblockStaffView.as_view(), name="Unblock the manager"),
    path('/update_password/<str:token>', SetPasswordView.as_view(), name="Set the password"),
    path('/<int:pk>/activate', ActivateStaffView.as_view(), name="Activate the staff"),
    path('/me', MeView.as_view(), name="Check for current logged user"),
]
