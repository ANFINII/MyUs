from dataclasses import dataclass
from ninja import Schema
from api.utils.enum.index import GenderType


@dataclass(frozen=True, slots=True)
class MessageData:
    error: bool
    message: str


class SignUpDataIn(Schema):
    email: str
    username: str
    nickname: str
    password1: str
    password2: str
    last_name: str
    first_name: str
    year: int
    month: int
    day: int
    gender: GenderType


class LoginDataIn(Schema):
    username: str
    password: str


@dataclass(frozen=True, slots=True)
class LoginOutData:
    access: str
    refresh: str


class RefreshDataIn(Schema):
    refresh: str


@dataclass(frozen=True, slots=True)
class RefreshOutData:
    access: str
