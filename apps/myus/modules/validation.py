import re


# バリデーション関数定義
def has_username(text):
    if re.fullmatch('^[a-zA-Z0-9_]+$', text) is not None:
        return False
    return True

def has_email(text):
    if re.fullmatch('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z.]+$', text) is not None:
        return False
    return True

def has_phone(text):
    if re.fullmatch('\d{2,4}-?\d{2,4}-?\d{3,4}', text) is not None:
        return False
    return True

def has_alphabet(text):
    if re.search('[a-zA-Z]', text) is not None:
        return True
    return False

def has_number(text):
    if re.search('[0-9０-９]', text) is not None:
        return True
    return False
