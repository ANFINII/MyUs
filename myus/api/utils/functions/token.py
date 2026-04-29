import datetime
import jwt
from django.conf import settings


def access_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "type": "access",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def refresh_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30),
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def signup_token(email: str) -> str:
    payload = {
        "email": email,
        "type": "signup",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=12),
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def password_reset_token(user_id: int, email: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "type": "password_reset",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
