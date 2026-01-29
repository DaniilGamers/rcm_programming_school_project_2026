from apps.orders.serializers import OrdersSerializer, GroupSerializer

from rest_framework.permissions import IsAuthenticated

from core.permissions.is_admin_or_manager import IsAdminOrManager

from apps.orders.filter import OrderFilter

from apps.orders.models import OrdersModel, GroupModel

from django.views import View

from datetime import datetime

from rest_framework.generics import (GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView)

from rest_framework.pagination import PageNumberPagination

import xlwt

from io import BytesIO

from django.http import FileResponse, HttpResponseForbidden


class CustomPagination(PageNumberPagination):
    page_size = 25
    page_query_param = "page"


class CustomGroupPagination(PageNumberPagination):
    queryset = GroupModel.objects.all()
    serializer_class = GroupSerializer

    page_size = len(queryset)


order = OrdersModel()


class OrdersListView(ListAPIView):
    serializer_class = OrdersSerializer
    pagination_class = CustomPagination
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
