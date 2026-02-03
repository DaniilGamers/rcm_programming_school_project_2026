

def apply_ordering(qs, request):
    ALLOWED_ORDER_FIELDS = {
        "id", "name", "surname", "email", "phone",
        "age", "course", "status", "manager", "created_at"
    }

    order = request.GET.get("order")
    if not order:
        return qs

    field = order[1:] if order.startswith("-") else order
    if field in ALLOWED_ORDER_FIELDS:
        return qs.order_by(order)

    return qs


def get_filtered_orders(request, qs):

    ALLOWED_ORDER_FIELDS = {
        "id", "name", "surname", "email", "phone",
        "age", "course", "status", "manager", "created_at"
    }

    name = request.GET.get("name")
    if name:
        qs = qs.filter(name__icontains=name)

    status = request.GET.get("status")
    if status:
        qs = qs.filter(status=status)

    manager = request.GET.get("manager")
    if manager:
        qs = qs.filter(manager=manager)

    group = request.GET.get("group")
    if group:
        qs = qs.filter(group__name__iexact=group)

    course = request.GET.get("course")
    if course:
        qs = qs.filter(course=course)

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
