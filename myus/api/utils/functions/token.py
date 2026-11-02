import datetime
import hashlib
import hmac
import jwt
import uuid
from django.conf import settings
from django.core.cache import cache


def password_fingerprint(password_hash: str) -> str:
    return hmac.new(settings.SECRET_KEY.encode(), password_hash.encode(), hashlib.sha256).hexdigest()[:16]


def access_token(user_id: int, password_hash: str) -> str:
    payload = {
        "user_id": user_id,
        "type": "access",
        "jti": uuid.uuid4().hex,
        "pwd": password_fingerprint(password_hash),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def refresh_token(user_id: int, password_hash: str) -> str:
    payload = {
        "user_id": user_id,
        "type": "refresh",
        "jti": uuid.uuid4().hex,
        "pwd": password_fingerprint(password_hash),
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


def password_reset_token(user_id: int, email: str, password_hash: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "type": "password_reset",
        "pwd": password_fingerprint(password_hash),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def revoked_token_key(jti: str) -> str:
    return f"revoked_token:{jti}"


def is_revoked(jti: str) -> bool:
    return cache.get(revoked_token_key(jti)) is not None


def revoke(jti: str, expires_at: datetime.datetime) -> None:
    timeout = int((expires_at - datetime.datetime.now(datetime.timezone.utc)).total_seconds())
    if timeout <= 0:
        return

    cache.set(revoked_token_key(jti), True, timeout)
