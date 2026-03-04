from django.utils import timezone
from datetime import datetime, time
from django.db.models import Q


class OrderFilterService:
    @staticmethod
    def filter_by_date(queryset, start_date_str, end_date_str):

        if start_date_str:
            try:
                date_value = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                start_of_day = timezone.make_aware(datetime.combine(date_value, time.min))
                end_of_day = timezone.make_aware(datetime.combine(date_value, time.max))
                queryset = queryset.filter(
                    Q(start_date__range=(start_of_day, end_of_day)) |
                    Q(end_date__range=(start_of_day, end_of_day))
                )
            except ValueError:
                pass

        if end_date_str:
            try:
                date_value = datetime.strptime(end_date_str, "%Y-%m-%d").date()
                start_of_day = timezone.make_aware(datetime.combine(date_value, time.min))
                end_of_day = timezone.make_aware(datetime.combine(date_value, time.max))
                queryset = queryset.filter(
                    Q(start_date__range=(start_of_day, end_of_day)) |
                    Q(end_date__range=(start_of_day, end_of_day))
                )
            except ValueError:
                pass

        return queryset
