from django.urls import path

from apps.orders.views import OrdersListView, EditOrderView, ExportOrdersView, GroupView, CommentView, OrderStatusCountView

urlpatterns = [
    path('', OrdersListView.as_view(), name="Order list"),
    path('/<int:id>', EditOrderView.as_view(), name="Edit order"),
    path('/groups_get', GroupView.as_view(), name="Group list"),
    path('/export', ExportOrdersView.as_view(), name="Export order list"),
    path('/groups_post', GroupView.as_view(), name="Create new group"),
    path('/<int:order_id>/comment_post', CommentView.as_view(), name="Post new comment"),
    path('/<int:order_id>/comment_get', CommentView.as_view(), name="Get user comments"),
    path('/status_count', OrderStatusCountView.as_view(), name="Count statuses"),
]
