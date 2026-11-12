from django.conf import settings
from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> str:
    remote_addr = str(request.META.get("REMOTE_ADDR", ""))
    forwarded_for = str(request.META.get("HTTP_X_FORWARDED_FOR", ""))
    num_proxies = settings.NINJA_NUM_PROXIES
    if num_proxies == 0 or not forwarded_for:
        return remote_addr

    addrs = [addr.strip() for addr in forwarded_for.split(",")]
    return addrs[-min(num_proxies, len(addrs))]
