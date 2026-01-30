from apps.orders.serializers import OrdersSerializer, GroupSerializer, CommentSerializer

from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

from core.permissions.is_admin_or_manager import IsAdminOrManager

from apps.orders.filter import OrderFilter

from django.db.models import Count

from apps.orders.models import OrdersModel, GroupModel, CommentModel

from django.views import View

from django.shortcuts import get_object_or_404

from datetime import datetime

from rest_framework.generics import (ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView)

from rest_framework.pagination import PageNumberPagination

import xlwt

from io import BytesIO

from django.http import FileResponse

from rest_framework.response import Response

from rest_framework import status


class CustomPagination(PageNumberPagination):
    page_size = 25
    page_query_param = "page"


class CustomGroupPagination(PageNumberPagination):
    queryset = GroupModel.objects.all()
    serializer_class = GroupSerializer

    def get_page_size(self, request):
        # dynamically compute page_size if needed
        qs = self.queryset if hasattr(self, 'queryset') else None
        if qs:
            return len(qs)
        return self.page_size


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

    def get(self, request, *args, **kwargs):

        palette_index = 23
        xlwt.add_palette_colour("mygreen", palette_index)

        xlwt.Style.colour_map["mygreen"] = palette_index
        xlwt.Style.colour_map[palette_index] = "mygreen"

        wb = xlwt.Workbook()
        wb.set_colour_RGB(palette_index, 118, 184, 82)
        ws = wb.add_sheet("Orders")

        headers = ["ID", "Name", "Surname", "Email", "Phone", "Age",
                   "Course", "Course Format", "Course Type", "Sum",
                   "Already Paid", "Created At", "Group", "UTM", "Msg",
                   "Status", "Manager"]

        max_widths = [len(header) for header in headers]

        header_style = xlwt.easyxf(
            "font: bold on, color white, height 280;"
            "pattern: pattern solid, fore_color mygreen;"
            "align: wrap on, horiz center;"
        )

        body_style = xlwt.easyxf(
            "font: height 240;"  # 12pt
        )

        for col_num, header in enumerate(headers):
            ws.write(0, col_num, header, header_style)

        def excel_nullable(value):
            """
            Convert value for Excel:
            - None or empty string -> 'NULL' (as text)
            - Otherwise -> str(value)
            """
            if value is None or value == "":
                return "null"
            return str(value)

        orders = OrdersModel.objects.select_related("group").all()

        for row_num, o in enumerate(orders, start=1):
            row = [
                excel_nullable(o.id),
                excel_nullable(o.name),
                excel_nullable(o.surname),
                excel_nullable(o.email),
                excel_nullable(o.phone),
                excel_nullable(o.age),
                excel_nullable(o.course),
                excel_nullable(o.course_format),
                excel_nullable(o.course_type),
                excel_nullable(o.sum),
                excel_nullable(o.alreadyPaid),
                excel_nullable(o.created_at.strftime("%d-%m-%Y") if o.created_at else None),
                excel_nullable(o.group.name if o.group else None),
                excel_nullable(o.utm),
                excel_nullable(o.msg),
                excel_nullable(o.status),
                excel_nullable(o.manager),
            ]
            style = body_style

            for col_num, value in enumerate(row):
                ws.write(row_num, col_num, value, style)
                max_widths[col_num] = max(max_widths[col_num], len(str(value)))

        for col_num, width in enumerate(max_widths):
            ws.col(col_num).width = min(256 * (width + 2), 65535)

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        filename = f"orders_{datetime.now().strftime('%m.%d.%Y')}.xls"

        return FileResponse(
            buffer,
            as_attachment=True,
            filename=filename,
            content_type="application/vnd.ms-excel"
        )


class GetGroupsView(ListAPIView):
    permission_classes = (IsAdminOrManager,)
    queryset = GroupModel.objects.all()
    pagination_class = CustomGroupPagination
    serializer_class = GroupSerializer


class SendCommentView(APIView):
    permission_classes = (IsAdminOrManager,)

    def post(self, request, order_id):
        order = get_object_or_404(OrdersModel, id=order_id)
        user_surname = request.user.name

        # 🔒 RULE:
        # comment allowed only if manager is null OR current user
        if order.manager and order.manager != user_surname:
            return Response(
                {"detail": "You cannot comment this order"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 💬 create comment
        CommentModel.objects.create(
            order=order,
            text=serializer.validated_data["text"],
            sender_name=request.user.name + ' ' + request.user.surname
        )

        # 👤 assign manager if empty
        if not order.manager:
            order.manager = user_surname

        # 🔄 update status
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
