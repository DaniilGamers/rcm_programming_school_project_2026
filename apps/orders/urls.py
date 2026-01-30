from django.urls import path

from apps.orders.views import OrdersListView, EditOrderView, AddGroupView, ExportOrdersView, GetGroupsView, SendCommentView, ViewCommentsView

urlpatterns = [
    path('', OrdersListView.as_view()),
    path('/edit_order/<int:id>/', EditOrderView.as_view()),
    path('/add_group', AddGroupView.as_view()),
    path('/export', ExportOrdersView.as_view()),
    path('/view_groups', GetGroupsView.as_view()),
    path('/send_comment/<int:order_id>/', SendCommentView.as_view()),
    path('/view_comments/<int:order_id>/', ViewCommentsView.as_view()),
]
