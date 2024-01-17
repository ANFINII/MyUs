import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

def get_user_id(request):
    token = request.COOKIES.get('user_token')
    if not token:
        return None

    key = settings.SECRET_KEY
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=['HS256'])
        user_id = payload['user_id']
        if not user_id:
            return Response({'error': '認証されていません!'}, status=HTTP_400_BAD_REQUEST)
        return user_id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.exceptions.DecodeError:
        return None
