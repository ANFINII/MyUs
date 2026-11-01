import re
from datetime import datetime
from urllib.parse import urlparse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from api.db.models.user import User


PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 64


# バリデーション関数定義
def has_username(text: str) -> bool:
    if re.fullmatch(r"^[a-zA-Z0-9_]+$", text):
        return False
    return True

def has_email(text: str) -> bool:
    if re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)+$", text):
        return False
    return True

def has_phone(text: str) -> bool:
    if re.fullmatch(r"\d{2,4}-?\d{2,4}-?\d{3,4}", text):
        return False
    return True

def has_postal_code(text: str) -> bool:
    if re.fullmatch(r"\d{3,3}-?\d{4,4}", text):
        return False
    return True

def has_url(text: str) -> bool:
    url = urlparse(text)
    if url.scheme == "https" and url.netloc:
        return False
    return True

def has_alphabet(text: str) -> bool:
    if re.search(r"[a-zA-Z]", text):
        return True
    return False

def has_number(text: str) -> bool:
    if re.search(r"[0-9０-９]", text):
        return True
    return False

def has_password(text: str) -> bool:
    if len(text) < PASSWORD_MIN_LENGTH or len(text) > PASSWORD_MAX_LENGTH:
        return True
    if not has_number(text) or not has_alphabet(text):
        return True
    return False

def has_weak_password(password: str, username: str, email: str, nickname: str) -> bool:
    try:
        validate_password(password, User(username=username, email=email, nickname=nickname))
        return False
    except ValidationError:
        return True

def has_birthday(year: int, month: int, day: int) -> bool:
    try:
        datetime(year, month, day)
        return False
    except ValueError:
        return True
