from apps.orders.models import OrdersModel
from django.db.models import Count, Case, When, Value, CharField, F, Q
from collections import defaultdict


class OrderStatusCountService:
    @staticmethod
    def get_order_status_count():

        qs = OrdersModel.objects.all()
        qs = qs.annotate(
            status_grouped=Case(
                When(Q(status__isnull=True) | Q(status__iexact="new") | Q(status=""), then=Value("New")),
                default=F("status"),
                output_field=CharField()
            )
        )

        # Overall counts
        by_status = qs.values("status_grouped").annotate(total=Count("id"))

        # Per-manager counts
        raw = qs.values("manager", "status_grouped").annotate(total=Count("id"))
        by_manager_dict = defaultdict(list)
        for item in raw:
            by_manager_dict[item["manager"]].append({
                "status": item["status_grouped"],
                "total": item["total"]
            })

        by_manager = [
            {"manager": manager, "total": sum(s["total"] for s in statuses), "by_status": statuses}
            for manager, statuses in by_manager_dict.items()
        ]

        return {
            "total": qs.count(),
            "by_status": list(by_status),
            "by_manager": by_manager
        }
