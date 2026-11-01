import hashlib
from django.core.cache import cache
from api.utils.constants.auth import LOGIN_LOCK_SECONDS


def login_failure_key(username: str) -> str:
    digest = hashlib.sha256(username.lower().encode()).hexdigest()
    return f"login_failure:{digest}"


def get_failure_count(username: str) -> int:
    count: int = cache.get(login_failure_key(username), 0)
    return count


def add_failure(username: str) -> None:
    key = login_failure_key(username)
    cache.add(key, 0, LOGIN_LOCK_SECONDS)
    cache.incr(key)
    cache.touch(key, LOGIN_LOCK_SECONDS)


def clear_failures(username: str) -> None:
    cache.delete(login_failure_key(username))
