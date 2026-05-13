from pydantic import BaseModel
from api.utils.enum.user import GenderType


class LoginIn(BaseModel):
    username: str
    password: str


class LoginOut(BaseModel):
    access: str
    refresh: str


class RefreshOut(BaseModel):
    access: str


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


class SignupVerifyOut(BaseModel):
    email: str


class PasswordChangeIn(BaseModel):
    old_password: str
    password1: str
    password2: str


class PasswordResetEmailIn(BaseModel):
    email: str


class PasswordResetIn(BaseModel):
    token: str
    password1: str
    password2: str


class PasswordResetVerifyOut(BaseModel):
    email: str


class WithdrawalIn(BaseModel):
    password: str
