

def apply_ordering(qs, request):
    ALLOWED_ORDER_FIELDS = {
        "id", "name", "surname", "email", "phone",
        "age", "course_format", "course", "course_type", "status", "manager", "created_at"
    }

    order = request.GET.get("order")
    if not order or order.strip() == "":
        return qs  # skip invalid or empty order

    # Remove leading '-' if descending
    field = order[1:] if order.startswith("-") else order

    # Only apply if field is allowed
    if field in ALLOWED_ORDER_FIELDS:
        return qs.order_by(order)

    return qs


def get_filtered_orders(request, qs):

    ALLOWED_ORDER_FIELDS = {
        "id", "name", "surname", "email", "phone",
        "age", "course_format", "course",  "course_type", "status", "manager", "created_at"
    }

    name = request.GET.get("name")
    if name:
        qs = qs.filter(name__icontains=name)

    surname = request.GET.get("surname")
    if surname is not None and surname != '':
        qs = qs.filter(surname__icontains=surname)

    email = request.GET.get("email")
    if email:
        qs = qs.filter(email__icontains=email)

    phone = request.GET.get("phone")
    if phone:
        qs = qs.filter(phone__icontains=phone)

    age = request.GET.get("age")
    if surname:
        qs = qs.filter(age__icontains=age)

    status = request.GET.get("status")
    if status:
        qs = qs.filter(status__iexact=status)

    manager = request.GET.get("manager")
    if manager:
        qs = qs.filter(manager__iexact=manager)

    group = request.GET.get("group")
    if group:
        qs = qs.filter(group__name__iexact=group)

    course = request.GET.get("course")
    if course:
        qs = qs.filter(course__iexact=course)

    course_format = request.GET.get("course_format")
    if course_format:
        qs = qs.filter(course_format__iexact=course_format)

    course_type = request.GET.get("course_type")
    if course_type:
        qs = qs.filter(course_type__iexact=course_type)

    start_date = request.GET.get("start_date")
    if start_date:
        qs = qs.filter(created_at__gte=start_date)

    end_date = request.GET.get("end_date")
    if end_date:
        qs = qs.filter(created_at__lte=end_date)

    order_param = request.GET.get("order")
    if order_param:

        desc = order_param.startswith('-')
        field_name = order_param[1:] if desc else order_param

        if field_name in ALLOWED_ORDER_FIELDS:
            qs = qs.order_by(order_param)

    return apply_ordering(qs, request)
