import jwt
from django.conf import settings
from datetime import datetime, timedelta


def generate_activation_token(user):
    payload = {
        "token_type": "activation",
        "user_id": user.id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token
