import re
from datetime import datetime


# バリデーション関数定義
def has_username(text: str) -> bool:
    if re.fullmatch("^[a-zA-Z0-9_]+$", text):
        return False
    return True

def has_email(text: str) -> bool:
    if re.fullmatch("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z.]+$", text):
        return False
    return True

def has_phone(text: str) -> bool:
    if re.fullmatch("\d{2,4}-?\d{2,4}-?\d{3,4}", text):
        return False
    return True

def has_postal_code(text: str) -> bool:
    if re.fullmatch("\d{3,3}-?\d{4,4}", text):
        return False
    return True

def has_alphabet(text: str) -> bool:
    if re.search("[a-zA-Z]", text):
        return True
    return False

def has_number(text: str) -> bool:
    if re.search("[0-9０-９]", text):
        return True
    return False

def has_birthday(year: int, month: int, day: int) -> bool:
    try:
        datetime(year, month, day)
        return False
    except ValueError:
        return True
