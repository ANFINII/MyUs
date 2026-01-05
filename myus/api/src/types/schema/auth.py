from pydantic import BaseModel
from api.utils.enum.index import GenderType


class SignupIn(BaseModel):
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


class LoginIn(BaseModel):
    username: str
    password: str


class LoginOut(BaseModel):
    access: str
    refresh: str


class RefreshOut(BaseModel):
    access: str
