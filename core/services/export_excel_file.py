import openpyxl
from django.http import HttpResponse
from apps.orders.models import OrdersModel
from datetime import datetime


def generate_orders_excel(queryset=None):
    # Use provided queryset or fetch all
    orders = queryset or OrdersModel.objects.all().select_related("group")

    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Orders"

    # Columns
    columns = [
        "ID", "Name", "Surname", "Email", "Phone", "Age",
        "Course", "Course Format", "Course Type",
        "Sum", "Already Paid", "Created At",
        "Group", "UTM", "Msg", "Status", "Manager"
    ]
    ws.append(columns)

    # Fill data
    for o in orders:
        ws.append([
            o.id,
            o.name,
            o.surname,
            o.email,
            o.phone,
            o.age,
            o.course,
            o.course_format,
            o.course_type,
            o.sum,
            o.alreadyPaid,
            o.created_at.strftime("%d-%m, %Y") if o.created_at else "",
            o.group.name if o.group else "",
            o.utm,
            o.msg,
            o.status,
            o.manager,
        ])

    timestamp = datetime.now().strftime("%d.%m.%Y")
    filename = f"{timestamp}.xlsx"

    # Prepare response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response
