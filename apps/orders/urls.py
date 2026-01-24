from django.urls import path

from apps.orders.views import OrdersListView

urlpatterns = [
    path('', OrdersListView.as_view())
]
