from apps.orders.serializers import OrdersSerializer, GroupSerializer, CommentSerializer

from rest_framework.permissions import IsAuthenticated

from core.permissions.is_admin_or_manager import IsAdminOrManager

from apps.orders.filter import OrderFilter

from django.db.models import Count

from apps.orders.models import OrdersModel, GroupModel, CommentModel

from django.views import View

from datetime import datetime

from django.shortcuts import get_object_or_404

from rest_framework.generics import (ListAPIView, RetrieveUpdateAPIView, GenericAPIView)

from apps.orders.pagination import CustomPagination, CustomGroupPagination, CustomCommentPagination

from rest_framework.response import Response

from rest_framework import status

from core.permissions.is_same_manager import IsSameManager

from core.services.export_excel import export_excel

from core.services.filter_orders import get_filtered_orders

from django.http import FileResponse, HttpResponse

from core.services.order_filter_service import OrderFilterService

from core.services.sendComment import SendCommentService

from core.services.order_status_count import OrderStatusCountService

order = OrdersModel()


class OrdersListView(ListAPIView):
    serializer_class = OrdersSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)
    queryset = OrdersModel.objects.all()
    filterset_class = OrderFilter

    def get_queryset(self):
        queryset = OrdersModel.objects.annotate(comments_count=Count('messages')).order_by('-id')

        return OrderFilterService.filter_by_date(
            queryset,
            self.request.query_params.get("start_date"),
            self.request.query_params.get("end_date")
        )


class EditOrderView(RetrieveUpdateAPIView):
    permission_classes = (IsAdminOrManager,)
    queryset = OrdersModel.objects.all()
    serializer_class = OrdersSerializer
    lookup_field = "id"


class GroupView(GenericAPIView):
    permission_classes = (IsAdminOrManager,)
    queryset = GroupModel.objects.all()
    pagination_class = CustomGroupPagination
    serializer_class = GroupSerializer

    def get(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExportOrdersView(View):

    def get(self, request):

        qs = get_filtered_orders(request, OrdersModel.objects.select_related("group").all())

        buffer = export_excel(qs)

        if not buffer:
            return HttpResponse("No data to export", status=400)

        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f"{datetime.now().strftime('%m.%d.%Y')}.xls",
            content_type="application/vnd.ms-excel"
        )


class CommentView(GenericAPIView):
    permission_classes = (IsSameManager,)
    serializer_class = CommentSerializer
    pagination_class = CustomCommentPagination

    def get_queryset(self):
        order_id = self.kwargs.get("order_id")  # get order_id from URL
        return CommentModel.objects.filter(order__id=order_id).order_by("created_at")

    def get(self, request, order_id):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, order_id):
        order = get_object_or_404(OrdersModel, id=order_id)
        self.check_object_permissions(request, order)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        SendCommentService.send_comment(order, request.user, serializer.validated_data["text"])

        return Response(
            {"detail": "Comment added successfully"},
            status=status.HTTP_201_CREATED
        )


class OrderStatusCountView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        return Response(OrderStatusCountService.get_order_status_count())
