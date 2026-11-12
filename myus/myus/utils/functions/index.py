from django_ulid.models import ulid
from django.conf import settings
from django.http import HttpRequest
from config.settings.base import DOMAIN_URL, MEDIA_URL


def new_ulid() -> str:
    return str(ulid.new())


def create_url(path: str) -> str:
    return f"{DOMAIN_URL}{MEDIA_URL}{path}" if path else ""


def message(error: bool, message: str) -> dict[str, str | bool]:
    return {"error": error, "message": message}


def get_client_ip(request: HttpRequest) -> str:
    remote_addr = str(request.META.get("REMOTE_ADDR", ""))
    forwarded_for = str(request.META.get("HTTP_X_FORWARDED_FOR", ""))
    num_proxies = settings.NINJA_NUM_PROXIES
    if num_proxies == 0 or not forwarded_for:
        return remote_addr

    addrs = [addr.strip() for addr in forwarded_for.split(",")]
    return addrs[-min(num_proxies, len(addrs))]
