from django_filters import rest_framework as filters
from apps.orders.models import OrdersModel


class OrderFilter(filters.FilterSet):
    name = filters.CharFilter('name', 'icontains')
    surname = filters.CharFilter('surname', 'icontains')
    email = filters.CharFilter('email', 'icontains')
    phone = filters.NumberFilter('phone')
    age = filters.NumberFilter('age')
    course = filters.BaseInFilter('course')
    course_format = filters.BaseInFilter('course_format')
    course_type = filters.BaseInFilter('course_type')
    status = filters.BaseInFilter('status')
    group = filters.BaseInFilter('group')
    date_startswith = filters.DateFilter('created_at', 'gte')
    date_endswith = filters.DateFilter('created_at', 'lte')
    manager = filters.BaseInFilter('manager')

    order = filters.OrderingFilter(
        fields=(
            'id',
            'name',
            'email',
            'phone',
            'age',
            'course',
            'course_format',
            'course_type',
            'sum',
            'alreadyPaid',
            'created_at',
            'utm',
            'msg',
            'group',
            'status',
            'manager'

        )
    )

    class Meta:
        model = OrdersModel
        fields = []
