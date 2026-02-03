import jwt

from django.conf import settings

from django.contrib.auth import get_user_model

from rest_framework.response import Response

UserModel = get_user_model()


def token_expireDate_check(request, token):

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

    return None
