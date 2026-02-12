from django.urls import path

from apps.users.views import StaffView, BlockStaffView, UnblockStaffView, SetPasswordView, ActivateStaffView, MeView

urlpatterns = [
    path('', StaffView.as_view()),
    path('', StaffView.as_view()),
    path('/<int:pk>/block/', BlockStaffView.as_view()),
    path('/<int:pk>/unblock/', UnblockStaffView.as_view()),
    path('/update_password/<str:token>', SetPasswordView.as_view()),
    path('/<int:pk>/activate/', ActivateStaffView.as_view()),
    path('/me/', MeView.as_view()),
]
