from django.http import HttpRequest
from api.src.usecase.auth import verify_token
from api.utils.common.result import FatalError, Result


def auth_check(request: HttpRequest) -> Result[int | None, FatalError]:
    token = request.COOKIES.get("access_token")
    if token is None:
        return Result.ok(None)

    ret = verify_token(token, "access")
    if ret.is_err:
        return Result.err(ret.err_value)

    user_id = ret.ok_value
    return Result.ok(user_id)
