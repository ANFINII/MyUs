from typing import TypeVar
from config.settings.base import DOMAIN_URL
from django_ulid.models import ulid


T = TypeVar('T')
V = TypeVar('V')


def is_bool(value: str) -> bool:
    return value.lower() == "true"


def new_ulid() -> str:
    return str(ulid.new())


def set_attr(obj: T, key: str, value: V) -> dict[str, V]:
    cls = type(obj)

    for base in cls.__mro__:
        if '__setattr__' in base.__dict__:
            base.__dict__['__setattr__'](obj, key, value)
            return vars(obj) if hasattr(obj, '__dict__') else {key: value}

    if hasattr(obj, '__dict__'):
        obj.__dict__[key] = value
        return vars(obj)
    else:
        object.__setattr__(obj, key, value)
        return {key: value}


def create_url(path: str) -> str:
    return f"{DOMAIN_URL}{path}" if path else ""


def message(error: bool, message: str) -> dict[str, str | bool]:
    return {"error": error, "message": message}
