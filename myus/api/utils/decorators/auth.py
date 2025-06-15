from functools import wraps
from api.services.user import get_user
from api.utils.enum.response import ApiResponse


def auth_user(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = get_user(request)
        if not user:
            return ApiResponse.UNAUTHORIZED.run()
        return func(self, request, *args, **kwargs)
    return wrapper
