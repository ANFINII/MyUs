from injector import Module, provider
from api.src.domain.entity.user.repository import UserRepository
from api.src.domain.interface.user.interface import UserInterface


class UserModule(Module):
    @provider
    def provide_user_repository(self) -> UserInterface:
        return UserRepository()
