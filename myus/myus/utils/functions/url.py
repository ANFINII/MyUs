from config.settings.base import DOMAIN_URL, MEDIA_URL


def create_url(path: str) -> str:
    return f"{DOMAIN_URL}{MEDIA_URL}{path}" if path else ""
