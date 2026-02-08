import jwt
from django.conf import settings
from django.http import HttpRequest


def auth_check(request: HttpRequest) -> int | None:
    token = request.COOKIES.get("access_token")
    if token is None:
        return None

    key = settings.SECRET_KEY
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=["HS256"])
        user_id: int | None = payload["user_id"]
        if user_id is None:
            return None

        return user_id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.exceptions.DecodeError:
        return None
