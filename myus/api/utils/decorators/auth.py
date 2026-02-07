from functools import wraps
from api.src.usecase.auth import auth_check
from api.utils.enum.response import ApiResponse


def auth_user(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        if auth_check(request) is None:
            return ApiResponse.UNAUTHORIZED.run()
        return func(self, request, *args, **kwargs)
    return wrapper
