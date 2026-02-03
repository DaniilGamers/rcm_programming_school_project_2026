from django.contrib.auth import get_user_model

from rest_framework import status

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt

from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView

from rest_framework.permissions import IsAuthenticated, AllowAny

from core.permissions.is_superAdmin import IsSuperAdmin

from apps.users.serializers import UserSerializer

from core.services.activate_link_generator import generate_activation_token

from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination

from core.services.token_expireDate_check import token_expireDate_check

UserModel = get_user_model()


class CustomPagination(PageNumberPagination):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class StaffListCreateView(CreateAPIView):
    permission_classes = (IsSuperAdmin,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class StaffListCheckView(ListAPIView):
    permission_classes = (IsSuperAdmin,)
    pagination_class = CustomPagination
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = UserModel.objects.all()

        if self.request.user.is_superuser:
            qs = qs.filter(is_staff=True, is_superuser=False)

        return qs


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

    def post(self, request, pk):
        user = get_object_or_404(UserModel, id=pk)
        token = generate_activation_token(user)
        link = f"http://localhost:3000/activate/{token}"
        return Response({"link": link})


class SetPasswordView(GenericAPIView):
    authentication_classes = []
    permission_classes = (AllowAny,)

    def post(self, request, token):
        response = token_expireDate_check(request, token)

        if isinstance(response, Response):
            return response

        return Response(
            {"detail": "Password set successfully"},
            status=status.HTTP_200_OK
        )


class MeView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
