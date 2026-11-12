from django_ulid.models import ulid
from config.settings.base import DOMAIN_URL, MEDIA_URL


def new_ulid() -> str:
    return str(ulid.new())


def create_url(path: str) -> str:
    return f"{DOMAIN_URL}{MEDIA_URL}{path}" if path else ""
