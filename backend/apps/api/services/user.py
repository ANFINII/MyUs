import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


User = get_user_model()


def get_user_id(request) -> Response:
    token = request.COOKIES.get('user_token')
    if not token:
        return Response({'message': '認証されていません!'}, status=HTTP_400_BAD_REQUEST)

    key = settings.SECRET_KEY
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=['HS256'])
        user_id = payload['user_id']
        if not user_id:
            return Response({'message': '認証されていません!'}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=user_id).first()
        if not user.is_active:
            return Response({'message': '退会済みです!'}, status=HTTP_400_BAD_REQUEST)
        return Response({'user_id': user_id}, status=HTTP_200_OK)
    except jwt.ExpiredSignatureError:
        return Response({'message': '認証エラーが発生しました!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    except jwt.exceptions.DecodeError:
        return Response({'message': '認証エラーが発生しました!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


def get_user(request) -> Response:
    token = request.COOKIES.get('user_token')
    if not token:
        return None

    key = settings.SECRET_KEY
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=['HS256'])
        user_id = payload['user_id']
        if not user_id:
            return None

        user = User.objects.filter(id=user_id).first()
        if not user.is_active:
            return None
        return user
    except jwt.ExpiredSignatureError:
        return None
    except jwt.exceptions.DecodeError:
        return None
