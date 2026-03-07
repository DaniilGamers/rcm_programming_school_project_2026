from datetime import datetime


class OrderFilterService:
    @staticmethod
    def filter_by_date(queryset, start, end):
        start_date = datetime.strptime(start, "%m/%d/%Y").date() if start else None
        end_date = datetime.strptime(end, "%m/%d/%Y").date() if end else None

        if start_date and end_date:
            return queryset.filter(created_at__date__range=(start_date, end_date))
        elif start_date:
            return queryset.filter(created_at__date=start_date)
        elif end_date:
            return queryset.filter(created_at__date=end_date)
        return queryset
