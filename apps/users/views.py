from django.contrib.auth import get_user_model


from rest_framework.generics import GenericAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser,IsAuthenticated

from apps.users.serializers import UserSerializer
UserModel = get_user_model()


class UserListCreateView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
