from django.urls import path

from apps.users.views import StaffListCreateView, StaffListCheckView, BlockStaffView, UnblockStaffView, SetPasswordView

urlpatterns = [
    path('/create_manager', StaffListCreateView.as_view()),
    path('/view_managerList', StaffListCheckView.as_view()),
    path('/block_manager/<int:pk>', BlockStaffView.as_view()),
    path('/unblock_manager/<int:pk>', UnblockStaffView.as_view()),
    path('/set_password', SetPasswordView.as_view())
]