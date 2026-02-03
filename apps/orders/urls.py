from django.urls import path

from apps.orders.views import OrdersListView, EditOrderView, AddGroupView, ExportOrdersView, GetGroupsView, SendCommentView, ViewCommentsView, OrderStatusCountView

urlpatterns = [
    path('/list_orders', OrdersListView.as_view()),
    path('/update_order/<int:id>/', EditOrderView.as_view()),
    path('/create_group/', AddGroupView.as_view()),
    path('/excel_export', ExportOrdersView.as_view()),
    path('/list_groups/', GetGroupsView.as_view()),
    path('/post_comment/<int:order_id>/', SendCommentView.as_view()),
    path('/list_comments/<int:order_id>/', ViewCommentsView.as_view()),
    path('/count_order_status/', OrderStatusCountView.as_view()),
]
