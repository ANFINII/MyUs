import hashlib
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.core.exceptions import ValidationError
from myus.db.models.user import User
from ..constants.auth import LOGIN_LOCK_SECONDS


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


def has_weak_password(password: str, username: str, email: str, nickname: str) -> bool:
    try:
        validate_password(password, User(username=username, email=email, nickname=nickname))
        return False
    except ValidationError:
        return True
