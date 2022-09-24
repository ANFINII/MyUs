import jwt
from datetime import date

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import JsonResponse

from rest_framework import authentication, permissions
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView, View
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt import views
from rest_framework_simplejwt import exceptions

from apps.myus.api.serializers import UserSerializer, SignUpSerializer, LoginSerializer
from apps.myus.modules.validation import has_username, has_email, has_phone, has_postal_code, has_alphabet, has_number
from apps.myus.models import Profile, MyPage, SearchTag, HashTag, NotificationSetting
from apps.myus.models import Notification, Follow, Comment, Message, Advertise
from apps.myus.models import Video, Live, Music, Picture, Blog, Chat, Collabo, Todo


User = get_user_model()


class SignUpAPI(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
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


# JWT Token Auth
class LoginView(views.TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({'error': 'ID又はパスワードが違います!'}, status=HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({'error': '退会済みのユーザーです!'}, status=HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        res = Response(serializer.validated_data, status=HTTP_200_OK)
        try:
            res.delete_cookie('user_token')
        except Exception:
            return Response({'error': 'not user_token'}, status=HTTP_400_BAD_REQUEST)

        access = serializer.validated_data['access']
        refresh = serializer.validated_data['refresh']
        res.set_cookie('user_token', access, max_age=60 * 60 * 24 * 10, httponly=True)
        res.set_cookie('refresh_token', refresh, max_age=60 * 60 * 24 * 30, httponly=True)
        return res


class LogoutAPI(views.TokenObtainPairView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        res = Response(serializer.validated_data, status=HTTP_200_OK)
        try:
            res.delete_cookie('access_token')
            res.delete_cookie('refresh_token')
        except Exception:
            return Response({'error': 'error'}, status=HTTP_400_BAD_REQUEST)
        return Response({'success': 'logout'}, status=HTTP_200_OK)


def refresh_get(request):
    try:
        refresh_token = request.COOKIES['refresh_token']
        return JsonResponse({'refresh': refresh_token}, safe=False)
    except Exception:
        return Response({'error': 'Token refresh failure'}, status=HTTP_400_BAD_REQUEST)


class TokenRefresh(views.TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        access = serializer.validated_data['access']
        res = Response(serializer.validated_data, status=HTTP_200_OK)
        res.delete_cookie('user_token')
        res.set_cookie('user_token', access, max_age=60 * 24 * 24 * 30, httponly=True)
        return res


class UserAPI(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get_object(self, user_token):
        key = settings.SECRET_KEY
        try:
            payload = jwt.decode(jwt=user_token, key=key, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return 'Activations link expired'
        except jwt.exceptions.DecodeError:
            return 'Invalid Token'

    def get(self, request, format=None):
        user_token = request.COOKIES.get('user_token')
        if not user_token:
            return Response({'error': 'tokenがありません!'}, status=HTTP_400_BAD_REQUEST)

        user_id = self.get_object(user_token)
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'error': '存在しないユーザーです!'}, status=HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({'error': '退会済みのユーザーです!'}, status=HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class Index(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        nicknames = [user.nickname for user in User.objects.all()]
        return Response(nicknames)

    def post(self, request):
        usernames = request.POST.getlist('username')
        users = [User(username=username) for username in usernames]
        User.objects.bulk_create(users)
