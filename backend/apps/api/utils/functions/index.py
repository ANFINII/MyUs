def is_bool(value: str) -> bool:
    return value.lower() == 'true'


def message(error: bool, message: str | None):
    return {'error': error, 'message': message}
