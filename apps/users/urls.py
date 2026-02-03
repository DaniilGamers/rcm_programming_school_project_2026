from django.urls import path

from apps.users.views import StaffListCreateView, StaffListCheckView, BlockStaffView, UnblockStaffView, SetPasswordView, ActivateStaffView, MeView

urlpatterns = [
    path('/create_manager/', StaffListCreateView.as_view()),
    path('/list_managers/', StaffListCheckView.as_view()),
    path('/block_manager/<int:pk>/', BlockStaffView.as_view()),
    path('/unblock_manager/<int:pk>/', UnblockStaffView.as_view()),
    path('/update_password/<str:token>', SetPasswordView.as_view()),
    path('/post_activate_manager/<int:pk>/', ActivateStaffView.as_view()),
    path('/get_user/', MeView.as_view()),
]
