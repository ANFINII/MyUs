import hashlib
from django.core.cache import cache
from api.src.domain.interface.login_attempt.interface import LoginAttemptInterface
from api.utils.common.result import FatalError, Result
from api.utils.constants.auth import LOGIN_LOCK_SECONDS


class LoginAttemptRepository(LoginAttemptInterface):
    def cache_key(self, username: str) -> str:
        digest = hashlib.sha256(username.lower().encode()).hexdigest()
        return f"login_failure:{digest}"

    @Result.shield_exception()
    def get_failure_count(self, username: str) -> Result[int, FatalError]:
        count: int = cache.get(self.cache_key(username), 0)
        return Result.ok(count)

    @Result.shield_exception()
    def add_failure(self, username: str) -> Result[None, FatalError]:
        key = self.cache_key(username)
        cache.add(key, 0, LOGIN_LOCK_SECONDS)
        cache.incr(key)
        cache.touch(key, LOGIN_LOCK_SECONDS)
        return Result.ok(None)

    @Result.shield_exception()
    def clear_failures(self, username: str) -> Result[None, FatalError]:
        cache.delete(self.cache_key(username))
        return Result.ok(None)
