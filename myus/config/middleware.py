import json
from collections.abc import Callable
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from api.modules.logger import log
from api.src.types.schema.common import ErrorOut, ErrorType


API_PATH_PREFIX = "/api/"
UNSAFE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


class OriginCheckMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.method not in UNSAFE_METHODS or not request.path.startswith(API_PATH_PREFIX):
            return self.get_response(request)

        origin = request.headers.get("Origin")
        if origin is not None and origin not in settings.CSRF_TRUSTED_ORIGINS:
            log.warning("Untrusted origin", path=request.path, origin=origin)
            error = ErrorOut(type=ErrorType.FORBIDDEN, message="Forbidden")
            return JsonResponse(error.model_dump(mode="json"), status=400)

        return self.get_response(request)


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
