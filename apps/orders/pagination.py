from rest_framework.pagination import PageNumberPagination
from apps.orders.models import CommentModel
from apps.orders.serializers import GroupSerializer, CommentSerializer


class CustomPagination(PageNumberPagination):
    page_size = 25
    page_query_param = "page"


class CustomGroupPagination(PageNumberPagination):
    queryset = CommentModel.objects.all()
    serializer_class = GroupSerializer

    def get_page_size(self, request):
        qs = getattr(self, 'queryset', None)
        if qs:
            return qs.count()
        return self.page_size


class CustomCommentPagination(PageNumberPagination):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer

    def get_page_size(self, request):
        qs = getattr(self, 'queryset', None)
        if qs:
            return qs.count()
        return self.page_size