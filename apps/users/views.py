from django.contrib.auth import get_user_model

from rest_framework import status

from django.utils import timezone

from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from core.permissions.is_superAdmin import IsSuperAdmin
from apps.users.serializers import UserSerializer, SetPasswordSerializer

from django.shortcuts import get_object_or_404

from rest_framework.response import Response

UserModel = get_user_model()


class StaffListCreateView(CreateAPIView):
    permission_classes = (IsSuperAdmin,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class StaffListCheckView(ListAPIView):
    permission_classes = (IsSuperAdmin,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class BlockStaffView(GenericAPIView):
    permission_classes = (IsSuperAdmin,)

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if user.is_active:
            user.is_active = False
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UnblockStaffView(GenericAPIView):
    permission_classes = (IsSuperAdmin,)

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if not user.is_active:
            user.is_active = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class ActivateStaffView(GenericAPIView):
    permission_classes = (IsSuperAdmin,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class SetPasswordView(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = get_object_or_404(UserModel, id=pk)

        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data['password'])
        user.is_active = True
        user.last_login = timezone.now()
        user.save()

        return Response(
            {"detail": "Password set successfully"}
        )