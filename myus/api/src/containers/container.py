from injector import Injector, Module
from api.src.containers.user import UserModule


modules: list[Module] = [
    UserModule(),
]

injector = Injector(modules)
