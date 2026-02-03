from apps.orders.serializers import OrdersSerializer, GroupSerializer, CommentSerializer

from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

from core.permissions.is_admin_or_manager import IsAdminOrManager

from apps.orders.filter import OrderFilter

from django.db.models import Count

from apps.orders.models import OrdersModel, GroupModel, CommentModel

from django.views import View

from datetime import datetime

from django.shortcuts import get_object_or_404

from rest_framework.generics import (ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, GenericAPIView)

from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response

from rest_framework import status

from core.permissions.is_same_manager import IsSameManager
from core.services.export_excel import export_excel

from core.services.filter_orders import get_filtered_orders

from django.http import FileResponse


class CustomPagination(PageNumberPagination):
    page_size = 25
    page_query_param = "page"


class CustomGroupPagination(PageNumberPagination):
    queryset = GroupModel.objects.all()
    serializer_class = GroupSerializer

    page_size = -0


class CustomCommentPagination(PageNumberPagination):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer

    def get_page_size(self, request):
        # dynamically compute page_size if needed
        qs = self.queryset if hasattr(self, 'queryset') else None
        if qs:
            return len(qs)
        return self.page_size


order = OrdersModel()


class OrdersListView(ListAPIView):
    serializer_class = OrdersSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)
    queryset = OrdersModel.objects.all()
    filterset_class = OrderFilter

    def get_queryset(self):
        return OrdersModel.objects.annotate(comments_count=Count('messages')).order_by('-id')


class EditOrderView(RetrieveUpdateAPIView):
    permission_classes = (IsAdminOrManager,)
    queryset = OrdersModel.objects.all()
    serializer_class = OrdersSerializer
    lookup_field = "id"


class AddGroupView(ListCreateAPIView):
    permission_classes = (IsAdminOrManager,)
    queryset = GroupModel.objects.all()
    serializer_class = GroupSerializer


class ExportOrdersView(View):

    def get(self, request):

        qs = OrdersModel.objects.select_related("group").all()

        qs = get_filtered_orders(request, qs)

        buffer = export_excel(qs)

        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f"{datetime.now().strftime('%m.%d.%Y')}.xls",
            content_type="application/vnd.ms-excel"
        )


class GetGroupsView(ListAPIView):
    permission_classes = (IsAdminOrManager,)
    queryset = GroupModel.objects.all()
    pagination_class = CustomGroupPagination
    serializer_class = GroupSerializer


class SendCommentView(GenericAPIView):
    permission_classes = (IsSameManager,)

    def post(self, request, order_id):
        order = get_object_or_404(OrdersModel, id=order_id)
        user_surname = request.user.name

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        CommentModel.objects.create(
            order=order,
            text=serializer.validated_data["text"],
            sender_name=request.user.name + ' ' + request.user.surname
        )

        if not order.manager:
            order.manager = user_surname

        if order.status in (None, "New"):
            order.status = "In Work"

        order.save()

        return Response(
            {"detail": "Comment added successfully"},
            status=status.HTTP_201_CREATED
        )


class ViewCommentsView(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CustomCommentPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        order_id = self.kwargs.get("order_id")  # get order_id from URL
        return CommentModel.objects.filter(order__id=order_id).order_by("created_at")


class OrderStatusCountView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        manager = request.query_params.get('manager')
        qs = OrdersModel.objects.all()
        if manager:
            qs = qs.filter(manager=manager)

        by_status = qs.values('status').annotate(total=Count('id'))
        total = qs.count()

        return Response({
            "total": total,
            "by_status": by_status
        })
