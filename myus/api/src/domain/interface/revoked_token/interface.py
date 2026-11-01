from abc import ABC, abstractmethod
from datetime import datetime
from api.utils.common.result import FatalError, Result


class RevokedTokenInterface(ABC):
    @abstractmethod
    def is_revoked(self, jti: str) -> Result[bool, FatalError]:
        ...

    @abstractmethod
    def revoke(self, jti: str, expires_at: datetime) -> Result[None, FatalError]:
        ...
