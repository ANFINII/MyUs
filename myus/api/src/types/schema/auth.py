from typing import Annotated
from pydantic import BaseModel, Field
from api.utils.enum.user import GenderType


class LoginIn(BaseModel):
    username: str
    password: str


class SignupEmailIn(BaseModel):
    email: str


class SignupIn(BaseModel):
    token: str
    email: Annotated[str, Field(max_length=255)]
    username: str
    nickname: Annotated[str, Field(max_length=80)]
    password1: str
    password2: str
    last_name: Annotated[str, Field(max_length=50)]
    first_name: Annotated[str, Field(max_length=50)]
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
