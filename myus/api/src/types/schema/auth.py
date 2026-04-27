from pydantic import BaseModel
from api.utils.enum.index import GenderType


class SignupEmailIn(BaseModel):
    email: str


class SignupIn(BaseModel):
    token: str
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


class PasswordChangeIn(BaseModel):
    old_password: str
    new_password1: str
    new_password2: str


class WithdrawalIn(BaseModel):
    password: str


class SignupVerifyOut(BaseModel):
    email: str


class LoginOut(BaseModel):
    access: str
    refresh: str


class RefreshOut(BaseModel):
    access: str
