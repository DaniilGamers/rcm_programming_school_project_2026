from django.shortcuts import render

from apps.orders.serializers import OrdersSerializer, GroupSerializer

from rest_framework.permissions import IsAuthenticated

from core.permissions.is_admin_or_manager import IsAdminOrManager

from apps.orders.filter import OrderFilter

from apps.orders.models import OrdersModel, GroupModel

from core.services.export_excel_file import generate_orders_excel

from rest_framework.generics import (GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView)

order = OrdersModel()


class OrdersListView(ListAPIView):
    serializer_class = OrdersSerializer
    permission_classes = (IsAuthenticated,)
    queryset = OrdersModel.objects.all()
    filterset_class = OrderFilter


class EditOrderView(RetrieveUpdateAPIView):
    permission_classes = (IsAdminOrManager,)
    queryset = OrdersModel.objects.all()
    serializer_class = OrdersSerializer
    lookup_field = "id"


class AddGroupView(ListCreateAPIView):
    permission_classes = (IsAdminOrManager,)
    queryset = GroupModel.objects.all()
    serializer_class = GroupSerializer


class ExportOrdersView(ListAPIView):
    permission_classes = (IsAdminOrManager,)
    queryset = OrdersModel.objects.all()
    serializer_class = OrdersSerializer

    def get(self, request):
        return generate_orders_excel()
