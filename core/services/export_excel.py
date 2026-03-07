import xlwt

from io import BytesIO


def export_excel(qs):
    if not qs:
        return None

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

    for row_num, order in enumerate(qs, start=1):
        row = [
            excel_nullable(order.id),
            excel_nullable(order.name),
            excel_nullable(order.surname),
            excel_nullable(order.email),
            excel_nullable(order.phone),
            excel_nullable(order.age),
            excel_nullable(order.course),
            excel_nullable(order.course_format),
            excel_nullable(order.course_type),
            excel_nullable(order.sum),
            excel_nullable(order.alreadyPaid),
            excel_nullable(order.created_at.strftime("%d-%m-%Y") if order.created_at else None),
            excel_nullable(order.group.name if order.group else None),
            excel_nullable(order.utm),
            excel_nullable(order.msg),
            excel_nullable(order.status),
            excel_nullable(order.manager),
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

    return buffer
