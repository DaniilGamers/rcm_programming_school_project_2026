from collections import defaultdict

from apps.orders.serializers import OrdersSerializer, GroupSerializer, CommentSerializer

from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

from core.permissions.is_admin_or_manager import IsAdminOrManager

from apps.orders.filter import OrderFilter

from django.db.models import Count, Case, When, Value, CharField, F, Q

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

from django.http import FileResponse, HttpResponse


class CustomPagination(PageNumberPagination):
    page_size = 25
    page_query_param = "page"


class CustomGroupPagination(PageNumberPagination):
    queryset = CommentModel.objects.all()
    serializer_class = GroupSerializer

    def get_page_size(self, request):
        qs = getattr(self, 'queryset', None)
        if qs:
            return qs.count()
        return self.page_size


class CustomCommentPagination(PageNumberPagination):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer

    def get_page_size(self, request):
        qs = getattr(self, 'queryset', None)
        if qs:
            return qs.count()
        return self.page_size


order = OrdersModel()


class OrdersListView(ListAPIView):
    serializer_class = OrdersSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)
    queryset = OrdersModel.objects.all()
    filterset_class = OrderFilter

    def get_queryset(self):
        queryset = OrdersModel.objects.annotate(comments_count=Count('messages')).order_by('-id')

        start_date_str = self.request.query_params.get("start_date")
        end_date_str = self.request.query_params.get("end_date")

        if start_date_str:
            try:
                date_value = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                start_of_day = timezone.make_aware(datetime.combine(date_value, time.min))
                end_of_day = timezone.make_aware(datetime.combine(date_value, time.max))

                queryset = queryset.filter(
                    Q(start_date__range=(start_of_day, end_of_day)) |
                    Q(end_date__range=(start_of_day, end_of_day))
                )
            except ValueError:
                pass  # Ignore invalid dates

        if end_date_str:
            try:
                date_value = datetime.strptime(end_date_str, "%Y-%m-%d").date()
                start_of_day = timezone.make_aware(datetime.combine(date_value, time.min))
                end_of_day = timezone.make_aware(datetime.combine(date_value, time.max))

                queryset = queryset.filter(
                    Q(start_date__range=(start_of_day, end_of_day)) |
                    Q(end_date__range=(start_of_day, end_of_day))
                )
            except ValueError:
                pass  # Ignore invalid dates

        return queryset


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

        qs = OrdersModel.objects.select_related("group").all()

        qs = get_filtered_orders(request, qs)

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

        CommentModel.objects.create(
            order=order,
            text=serializer.validated_data["text"],
            sender_name=request.user.name + ' ' + request.user.surname
        )

        if not order.manager:
            order.manager = request.user.name

        if order.status in (None, "New"):
            order.status = "In Work"

        order.save()

        return Response(
            {"detail": "Comment added successfully"},
            status=status.HTTP_201_CREATED
        )


class OrderStatusCountView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        qs = OrdersModel.objects.all()

        # Replace null/empty/"new" with "New"
        qs = qs.annotate(
            status_grouped=Case(
                When(Q(status__isnull=True) | Q(status__iexact="new") | Q(status=""), then=Value("New")),
                default=F("status"),
                output_field=CharField()
            )
        )

        # Overall counts
        by_status = qs.values("status_grouped").annotate(total=Count("id"))

        # Per-manager counts
        raw = qs.values("manager", "status_grouped").annotate(total=Count("id"))
        by_manager_dict = defaultdict(list)
        for item in raw:
            by_manager_dict[item["manager"]].append({
                "status": item["status_grouped"],
                "total": item["total"]
            })

        by_manager = [
            {"manager": manager, "total": sum(s["total"] for s in statuses), "by_status": statuses}
            for manager, statuses in by_manager_dict.items()
        ]

        return Response({
            "total": qs.count(),
            "by_status": list(by_status),
            "by_manager": by_manager
        })
