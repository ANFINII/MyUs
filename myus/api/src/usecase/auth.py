import jwt
from django.conf import settings
from django.http import HttpRequest
from api.src.usecase.user import get_user_data


def auth_check(request: HttpRequest) -> int | None:
    token = request.COOKIES.get("access_token")
    if token is None:
        return None

    key = settings.SECRET_KEY
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=["HS256"])
        user_id = payload["user_id"]
        if user_id is None:
            return None

        data = get_user_data(user_id)
        if data is None:
            return None

        if not data.user.is_active:
            return None
        return data.user.id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.exceptions.DecodeError:
        return None
