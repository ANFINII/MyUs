from datetime import UTC, datetime
from django.core.cache import cache
from api.src.domain.interface.revoked_token.interface import RevokedTokenInterface
from api.utils.common.result import FatalError, Result


class RevokedTokenRepository(RevokedTokenInterface):
    def cache_key(self, jti: str) -> str:
        return f"revoked_token:{jti}"

    @Result.shield_exception()
    def is_revoked(self, jti: str) -> Result[bool, FatalError]:
        return Result.ok(cache.get(self.cache_key(jti)) is not None)

    @Result.shield_exception()
    def revoke(self, jti: str, expires_at: datetime) -> Result[None, FatalError]:
        timeout = int((expires_at - datetime.now(UTC)).total_seconds())
        if timeout <= 0:
            return Result.ok(None)

        cache.set(self.cache_key(jti), True, timeout)
        return Result.ok(None)
