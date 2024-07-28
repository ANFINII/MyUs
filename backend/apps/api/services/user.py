import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from apps.api.utils.functions.index import message
from apps.myus.modules.validation import has_alphabet, has_username, has_email, has_phone, has_postal_code, has_number, has_birthday


User = get_user_model()


def get_user_id(request) -> Response:
    token = request.COOKIES.get('access_token')
    if not token:
        return Response(message(True, '認証されていません!'), status=HTTP_400_BAD_REQUEST)

    key = settings.SECRET_KEY
    try:
        payload = jwt.decode(jwt=token, key=key, algorithms=['HS256'])
        user_id = payload['user_id']
        if not user_id:
            return Response(message(True, '認証されていません!'), status=HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=user_id).first()
        if not user.is_active:
            return Response(message(True, '退会済みです!'), status=HTTP_400_BAD_REQUEST)
        return Response({'user_id': user_id}, status=HTTP_200_OK)
    except jwt.ExpiredSignatureError:
        return Response(message(True, '認証エラーが発生しました!'), status=HTTP_500_INTERNAL_SERVER_ERROR)
    except jwt.exceptions.DecodeError:
        return Response(message(True, '認証エラーが発生しました!'), status=HTTP_500_INTERNAL_SERVER_ERROR)


def get_user(request) -> AbstractBaseUser | None:
    token = request.COOKIES.get('access_token')
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


def profile_check(profile) -> str | None:
    if has_email(profile['email']):
        return 'メールアドレスの形式が違います!'

    if has_username(profile['username']):
        return 'ユーザー名は半角英数字のみ入力できます!'

    if has_number(profile['last_name']):
        return '姓に数字が含まれております!'

    if has_number(profile['first_name']):
        return '名に数字が含まれております!'

    if has_phone(profile['phone']):
        return '電話番号の形式が違います!'

    if has_postal_code(profile['postal_code']):
        return '郵便番号の形式が違います!'

    if has_birthday(int(profile['year']), int(profile['month']), int(profile['day'])):
        return f'{profile['year']}年{profile['month']}月{profile['day']}日は存在しない日付です!'


def signup_check(user) -> str | None:
    password1 = user['password1']
    password2 = user['password2']

    if has_email(user['email']):
        return 'メールアドレスの形式が違います!'

    if has_username(user['username']):
        return 'ユーザー名は半角英数字のみ入力できます!'

    if has_number(user['last_name']):
        return '姓に数字が含まれております!'

    if has_number(user['first_name']):
        return '名に数字が含まれております!'

    if has_birthday(int(user['year']), int(user['month']), int(user['day'])):
        return f'{user['year']}年{user['month']}月{user['day']}日は存在しない日付です!'

    if password1 != password2:
        return 'パスワードが一致していません!'

    if not has_number(password1) and not has_alphabet(password1):
        return 'パスワードは半角8文字以上で英数字を含む必要があります!'

    if User.objects.filter(email=user['email']).exists():
        return 'メールアドレスは既に登録されています!'

    if User.objects.filter(username=user['username']).exists():
        return 'ユーザー名は既に登録されています!'

    if User.objects.filter(nickname=user['nickname']).exists():
        return '投稿者名は既に登録されています!'
