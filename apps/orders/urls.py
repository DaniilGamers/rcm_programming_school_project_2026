from django.urls import path

from apps.orders.views import OrdersListView, EditOrderView, ExportOrdersView, GroupView, CommentView, OrderStatusCountView

urlpatterns = [
    path('', OrdersListView.as_view()),
    path('/<int:id>/', EditOrderView.as_view()),
    path('/groups', GroupView.as_view()),
    path('/export', ExportOrdersView.as_view()),
    path('/groups', GroupView.as_view()),
    path('/<int:order_id>/comment/', CommentView.as_view()),
    path('/<int:order_id>/comment/', CommentView.as_view()),
    path('/status_count', OrderStatusCountView.as_view()),
]
