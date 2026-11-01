from datetime import UTC, datetime
from django.core.cache import cache


def revoked_token_key(jti: str) -> str:
    return f"revoked_token:{jti}"


def is_revoked(jti: str) -> bool:
    return cache.get(revoked_token_key(jti)) is not None


def revoke(jti: str, expires_at: datetime) -> None:
    timeout = int((expires_at - datetime.now(UTC)).total_seconds())
    if timeout <= 0:
        return

    cache.set(revoked_token_key(jti), True, timeout)
