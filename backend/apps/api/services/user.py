import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

def get_user_id(request) -> int | None:
    token = request.COOKIES.get('user_token')
    if not token:
        return Response({'error': '認証Tokenがありません!'}, status=HTTP_400_BAD_REQUEST)

    key = settings.SECRET_KEY
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=['HS256'])
        user_id = payload['user_id']
        if not user_id:
            return Response({'error': '認証されていません!'}, status=HTTP_400_BAD_REQUEST)
        return user_id
    except jwt.ExpiredSignatureError:
        return Response({'error': '認証エラーが発生しました!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    except jwt.exceptions.DecodeError:
        return Response({'error': '認証エラーが発生しました!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
