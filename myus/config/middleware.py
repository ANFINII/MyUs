import json
from collections.abc import Callable
from django.http import HttpRequest, HttpResponse
from api.modules.logger import log


API_PATH_PREFIX = "/api/"


class ErrorResponseLogMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        if response.status_code < 400 or not request.path.startswith(API_PATH_PREFIX):
            return response

        error_type = response_error_type(response)
        if response.status_code >= 500:
            log.error("API error response", path=request.path, status=response.status_code, type=error_type)
        else:
            log.warning("API error response", path=request.path, status=response.status_code, type=error_type)
        return response


def response_error_type(response: HttpResponse) -> str:
    if response.streaming or not response.get("Content-Type", "").startswith("application/json"):
        return ""

    try:
        body = json.loads(response.content)
    except ValueError:
        return ""

    if not isinstance(body, dict):
        return ""

    error_type = body.get("type")
    return error_type if isinstance(error_type, str) else ""
