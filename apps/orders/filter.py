from django_filters import rest_framework as filters
from apps.orders.models import OrdersModel
from datetime import datetime
from django.db.models import Q


class OrderFilter(filters.FilterSet):
    name = filters.CharFilter('name', 'icontains')
    surname = filters.CharFilter('surname', 'icontains')
    email = filters.CharFilter('email', 'icontains')
    phone = filters.NumberFilter('phone', 'icontains')
    age = filters.NumberFilter('age', 'icontains')
    course = filters.BaseInFilter('course')
    course_format = filters.BaseInFilter('course_format')
    course_type = filters.BaseInFilter('course_type')
    status = filters.BaseInFilter('status')
    group = filters.CharFilter(field_name='group__name', lookup_expr='iexact')

    start_date = filters.DateFilter(method='filter_by_same_day')
    end_date = filters.DateFilter(method='filter_by_same_day')

    def filter_by_same_day(self, queryset, name, value):
        start = self.data.get('start_date')
        end = self.data.get('end_date')

        if not start and not end:
            return queryset

        start_date = datetime.strptime(start, "%m/%d/%Y").date() if start else None
        end_date = datetime.strptime(end, "%m/%d/%Y").date() if end else None

        if start_date and end_date:
            # full range between start and end
            return queryset.filter(created_at__date__range=(start_date, end_date))
        elif start_date:
            return queryset.filter(created_at__date=start_date)
        elif end_date:
            return queryset.filter(created_at__date=end_date)

        return queryset

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
