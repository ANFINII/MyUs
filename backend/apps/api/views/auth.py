import jwt
from datetime import date

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView
from rest_framework_simplejwt import views
from rest_framework_simplejwt import exceptions

from apps.api.serializers import SignUpSerializer
from apps.myus.models import Profile
from apps.myus.modules.validation import has_username, has_email, has_alphabet, has_number


User = get_user_model()


# Auth
class AuthAPI(APIView):
    def get_object(self, user_token):
        key = settings.SECRET_KEY
        try:
            payload = jwt.decode(jwt=user_token, key=key, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return Response({'error': '認証エラーが発生しました!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        except jwt.exceptions.DecodeError:
            return Response({'error': '認証エラーが発生しました!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        user_token = request.COOKIES.get('user_token')
        if not user_token:
            return Response({'error': '認証されていません!'}, status=HTTP_400_BAD_REQUEST)

        user_id = self.get_object(user_token)
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'error': '未登録です!'}, status=HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({'error': '退会済みです!'}, status=HTTP_400_BAD_REQUEST)
        return Response({'success': '認証済みです!'}, status=HTTP_200_OK)


class RefreshAPI(views.TokenRefreshView):
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        access = serializer.validated_data['access']
        response = Response(serializer.validated_data, status=HTTP_200_OK)
        response.delete_cookie('user_token')
        response.set_cookie('user_token', access, max_age=60 * 24 * 24 * 30, httponly=True)
        return response


class SignUpAPI(CreateAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        data = request.data
        email = data['email']
        username = data['username']
        nickname = data['nickname']
        password1 = data['password1']
        password2 = data['password2']
        last_name = data['last_name']
        first_name = data['first_name']
        year = data['year']
        month = data['month']
        day = data['day']
        gender = data['gender']

        if has_email(email):
            return Response({'error': 'メールアドレスの形式が違います!'}, status=HTTP_400_BAD_REQUEST)
        if has_username(username):
            return Response({'error': 'ユーザー名は半角英数字になります!'}, status=HTTP_400_BAD_REQUEST)
        if has_number(last_name):
            return Response({'error': '姓に数字が含まれています!'}, status=HTTP_400_BAD_REQUEST)
        if has_number(first_name):
            return Response({'error': '名に数字が含まれています!'}, status=HTTP_400_BAD_REQUEST)
        if password1 != password2:
            return Response({'error': 'パスワードが一致していません!'}, status=HTTP_400_BAD_REQUEST)
        if not has_number(password1) and not has_alphabet(password1):
            return Response({'error': 'パスワードは半角8文字以上で英数字を含む必要があります!'}, status=HTTP_400_BAD_REQUEST)
        if not has_number(year):
            return Response({'error': '生年月日の年を入力してください!'}, status=HTTP_400_BAD_REQUEST)
        if not has_number(month):
            return Response({'error': '生年月日の月を入力してください!'}, status=HTTP_400_BAD_REQUEST)
        if not has_number(day):
            return Response({'error': '生年月日の日を入力してください!'}, status=HTTP_400_BAD_REQUEST)
        if year and month and day:
            try:
                birthday = date(year=int(year), month=int(month), day=int(day)).isoformat()
            except ValueError:
                return Response({'error': f'{year}年{month}月{day}日は存在しない日付です!'}, status=HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'メールアドレスは既に登録されています!'}, status=HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'ユーザー名は既に登録されています!'}, status=HTTP_400_BAD_REQUEST)
        if User.objects.filter(nickname=nickname).exists():
            return Response({'error': '投稿者名は既に登録されています!'}, status=HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(email, username, nickname, password1)
            profile = Profile.objects.get(user=user)
            profile.last_name = last_name
            profile.first_name = first_name
            profile.gender = gender
            profile.birthday = birthday
            profile.save()
            return Response({'succss': 'アカウント登録が完了しました!'}, status=HTTP_201_CREATED)
        except Exception:
            return Response({'error': 'アカウント登録に失敗しました!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPI(views.TokenObtainPairView):
    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)
        if not user:
            user = authenticate(email=username, password=password)

        if not user:
            return Response({'error': 'ID又はパスワードが違います!'}, status=HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({'error': '退会済みのユーザーです!'}, status=HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=HTTP_204_NO_CONTENT)
        try:
            response.delete_cookie('user_token')
        except Exception:
            return Response({'error': 'not user_token'}, status=HTTP_400_BAD_REQUEST)

        access = serializer.validated_data['access']
        refresh = serializer.validated_data['refresh']
        response.set_cookie('user_token', access, max_age=60 * 60 * 24 * 10, httponly=True)
        response.set_cookie('refresh_token', refresh, max_age=60 * 60 * 24 * 30, httponly=True)
        return response


class LogoutAPI(views.TokenObtainPairView):
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=HTTP_200_OK)
        try:
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
        except Exception:
            return Response({'error': 'error'}, status=HTTP_400_BAD_REQUEST)
        return Response({'success': 'logout'}, status=HTTP_204_NO_CONTENT)
