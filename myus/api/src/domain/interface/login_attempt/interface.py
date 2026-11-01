from abc import ABC, abstractmethod
from api.utils.common.result import FatalError, Result


class LoginAttemptInterface(ABC):
    @abstractmethod
    def get_failure_count(self, username: str) -> Result[int, FatalError]:
        ...

    @abstractmethod
    def add_failure(self, username: str) -> Result[None, FatalError]:
        ...

    @abstractmethod
    def clear_failures(self, username: str) -> Result[None, FatalError]:
        ...
