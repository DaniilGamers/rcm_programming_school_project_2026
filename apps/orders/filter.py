from django_filters import rest_framework as filters
from apps.orders.models import OrdersModel
from core.services.order_filter_service import OrderFilterService


class OrderFilter(filters.FilterSet):
    name = filters.CharFilter('name', 'icontains')
    surname = filters.CharFilter('surname', 'icontains')
    email = filters.CharFilter('email', 'icontains')
    phone = filters.NumberFilter('phone', 'icontains')
    age = filters.NumberFilter('age', 'icontains')
    course = filters.BaseInFilter('course', lookup_expr='in')
    course_format = filters.BaseInFilter('course_format', lookup_expr='in')
    course_type = filters.BaseInFilter('course_type', lookup_expr='in')
    status = filters.BaseInFilter('status', lookup_expr='in')
    group = filters.CharFilter(field_name='group__name', lookup_expr='iexact')

    start_date = filters.DateFilter(method='filter_by_date_range')
    end_date = filters.DateFilter(method='filter_by_date_range')

    def filter_by_date_range(self, queryset, name, value):
        start = self.data.get('start_date')
        end = self.data.get('end_date')
        return OrderFilterService.filter_by_date(queryset, start, end)

    manager = filters.BaseInFilter('manager')

    order = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('name', 'name'),
            ('surname', 'surname'),
            ('email', 'email'),
            ('phone', 'phone'),
            ('age', 'age'),
            ('course', 'course'),
            ('course_format', 'course_format'),
            ('course_type', 'course_type'),
            ('sum', 'sum'),
            ('alreadyPaid', 'alreadyPaid'),
            ('created_at', 'created_at'),
            ('group__name', 'group'),
            ('status', 'status'),
            ('manager', 'manager')

        )
    )

    class Meta:
        model = OrdersModel
        fields = [
            "name", "surname", "email", "phone", "age",
            "course", "course_format", "course_type", "status",
            "group", "manager"
        ]
