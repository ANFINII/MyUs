from config.settings.base import DOMAIN_URL


def is_bool(value: str) -> bool:
    return value.lower() == "true"


def create_url(path: str) -> str:
    return f"{DOMAIN_URL}{path}" if path else ""


def message(error: bool, message: str | None):
    return {"error": error, "message": message}
