import jwt
from django.conf import settings


def get_user_id(request):
    token = request.COOKIES.get('user_token')
    if not token:
        return None

    key = settings.SECRET_KEY
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.exceptions.DecodeError:
        return None
