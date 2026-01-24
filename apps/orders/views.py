from django.shortcuts import render

from apps.orders.serializers import OrdersSerializer

from apps.orders.models import OrdersModel

from rest_framework.permissions import AllowAny

from rest_framework.generics import (GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView)


class OrdersListView(ListAPIView):
    serializer_class = OrdersSerializer
    permission_classes = (AllowAny,)
    queryset = OrdersModel.objects.all()
    #filterset_class = AdFilter