from django_ulid.models import ulid
from django.http import HttpRequest
from config.settings.base import DOMAIN_URL, MEDIA_URL


def new_ulid() -> str:
    return str(ulid.new())


def create_url(path: str) -> str:
    return f"{DOMAIN_URL}{MEDIA_URL}{path}" if path else ""


def message(error: bool, message: str) -> dict[str, str | bool]:
    return {"error": error, "message": message}


def get_client_ip(request: HttpRequest) -> str:
    forwarded_for = str(request.META.get("HTTP_X_FORWARDED_FOR", ""))
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return str(request.META.get("REMOTE_ADDR", ""))
