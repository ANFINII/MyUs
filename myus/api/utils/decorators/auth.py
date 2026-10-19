from functools import wraps
from api.src.usecase.auth import auth_check
from api.utils.enum.response import ApiResponse


def auth_user(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        ret = auth_check(request)
        if ret.is_err:
            return ApiResponse.SERVER_ERROR.run()

        user_id = ret.ok_value
        if user_id is None:
            return ApiResponse.UNAUTHORIZED.run()
        return func(self, request, *args, **kwargs)
    return wrapper
