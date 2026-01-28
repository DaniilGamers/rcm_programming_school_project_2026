from django.contrib.auth import get_user_model

from rest_framework import status

import jwt

from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, AllowAny

from core.permissions.is_superAdmin import IsSuperAdmin

from django.conf import settings

from apps.users.serializers import UserSerializer, SetPasswordSerializer

from core.services.activate_link_generator import generate_activation_token

from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.pagination import PageNumberPagination

UserModel = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size = 25
    page_query_param = "page"


class StaffListCreateView(CreateAPIView):
    permission_classes = (IsSuperAdmin,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class StaffListCheckView(ListAPIView):
    permission_classes = (IsSuperAdmin,)
    pagination_class = CustomPagination
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

    def post(self, request, pk):
        user = get_object_or_404(UserModel, id=pk)
        token = generate_activation_token(user)
        link = f"http://localhost:3000/activate/{token}"
        return Response({"link": link})


class SetPasswordView(GenericAPIView):
    authentication_classes = []
    permission_classes = (AllowAny,)

    def post(self, request, token):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return Response({"detail": "Token expired"}, status=400)
        except jwt.InvalidTokenError:
            return Response({"detail": "Invalid token"}, status=400)

        if payload.get("token_type") != "activation":
            return Response({"detail": "Wrong token type"}, status=400)

        user = UserModel.objects.get(id=payload["user_id"])

        user.set_password(request.data["password"])
        user.is_active = True
        user.save()

        return Response({"detail": "Account activated"})


class MeView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
        })
