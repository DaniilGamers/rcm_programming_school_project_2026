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
    group = filters.CharFilter(field_name='group__name', lookup_expr='iexact')
    date_startswith = filters.DateFilter('created_at', 'gte')
    date_endswith = filters.DateFilter('created_at', 'lte')
    manager = filters.BaseInFilter('manager')

    order = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('name', 'name'),
            ('email', 'email'),
            ('phone', 'phone'),
            ('age', 'age'),
            ('course', 'course'),
            ('course_format', 'course_format'),
            ('course_type', 'course_type'),
            ('sum', 'sum'),
            ('alreadyPaid', 'alreadyPaid'),
            ('created_at', 'created_at'),
            ('utm', 'utm'),
            ('msg', 'msg'),
            ('group', 'group'),
            ('status', 'status'),
            ('manager', 'manager')

        )
    )

    class Meta:
        model = OrdersModel
        fields = []
