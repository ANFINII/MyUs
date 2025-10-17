from dataclasses import dataclass
from ninja import Schema


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
    gender: int
    year: int
    month: int
    day: int


class LoginDataIn(Schema):
    username: str
    password: str


@dataclass(frozen=True, slots=True)
class UserLoginData:
    avatar: str
    ulid: str
    nickname: str
    is_staff: bool


@dataclass(frozen=True, slots=True)
class LoginOutData:
    access: str
    refresh: str
    user: UserLoginData


class RefreshDataIn(Schema):
    refresh: str


@dataclass(frozen=True, slots=True)
class RefreshOutData:
    access: str
