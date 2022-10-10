import jwt
from datetime import date

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView, View
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt import views
from rest_framework_simplejwt import exceptions

from apps.api.serializers import SignUpSerializer, LoginSerializer
from apps.api.serializers import UserSerializer, ProfileSerializer, MyPageSerializer
from apps.api.serializers import VideoSerializer, LiveSerializer, MusicSerializer, PictureSerializer
from apps.api.serializers import BlogSerializer, ChatSerializer, CollaboSerializer
from apps.myus.modules.filter_data import DeferData
from apps.myus.modules.validation import has_username, has_email, has_phone, has_postal_code, has_alphabet, has_number
from apps.myus.models import Profile, MyPage, SearchTag, HashTag, NotificationSetting
from apps.myus.models import Notification, Follow, Comment, Message, Advertise
from apps.myus.models import Video, Live, Music, Picture, Blog, Chat, Collabo, Todo


User = get_user_model()


# Auth
class AuthAPI(APIView):
    def get_object(self, user_token):
        key = settings.SECRET_KEY
        try:
            payload = jwt.decode(jwt=user_token, key=key, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return 'Activations link expired'
        except jwt.exceptions.DecodeError:
            return 'Invalid Token'

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

        response = Response(serializer.validated_data, status=HTTP_200_OK)
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
    permission_classes = [IsAuthenticated]

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
        return Response({'success': 'logout'}, status=HTTP_200_OK)


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


class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.COOKIES.get('user_token')
        key = settings.SECRET_KEY
        payload = jwt.decode(jwt=token, key=key, algorithms=['HS256'])
        user = User.objects.filter(id=payload['user_id']).select_related('profile').defer(*DeferData.profile).first()
        gender = {'0':'男性', '1':'女性', '2':'秘密'}

        context = {
            'image': user.image(),
            'email': user.email,
            'username': user.username,
            'nickname': user.nickname,
            'fullname': user.fullname(),
            'lastname': user.profile.last_name,
            'firstname': user.profile.first_name,
            'year': user.year(),
            'month': user.month(),
            'day': user.day(),
            'age': user.age(),
            'gender': gender[user.gender()],
            'phone': user.profile.phone,
            'country_code': user.profile.country_code,
            'postal_code': user.profile.postal_code,
            'city': user.profile.city,
            'address': user.profile.address,
            'building': user.profile.building,
            'introduction': user.profile.introduction,
        }
        return Response(context, status=HTTP_200_OK)

    def post(self, request):
        pass


class MyPageAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.COOKIES.get('user_token')
        key = settings.SECRET_KEY
        payload = jwt.decode(jwt=token, key=key, algorithms=['HS256'])
        user = User.objects.filter(id=payload['user_id']).select_related('mypage').defer(*DeferData.mypage).first()

        context = {
            'banner': user.banner(),
            'nickname': user.nickname,
            'email': user.mypage.email,
            'content': user.mypage.content,
            'follower_num': user.mypage.follower_num,
            'following_num': user.mypage.following_num,
            'plan': user.mypage.plan,
            'plan_date': user.mypage.plan_date,
            'is_advertise': user.mypage.is_advertise,
        }
        return Response(context, status=HTTP_200_OK)

    def post(self, request):
        pass


# Index
class IndexAPI(ListAPIView):

    def get(self, request):
        queryset = Video.objects.all()
        serializer_class = VideoSerializer

        context = {
            'video': VideoSerializer(video).data,
        }

        return Response(context)


# Video
class VideoListAPI(ListAPIView):
    # queryset = Video.objects.select_related('author').all()
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoCreateAPI(CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoDetailAPI(RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


# Music
class MusicListAPI(ListAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


class MusicCreateAPI(CreateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


class MusicDetailAPI(RetrieveAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


# Picture
class PictureListAPI(ListAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureCreateAPI(CreateAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetailAPI(RetrieveAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


# Blog
class BlogListAPI(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogCreateAPI(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogDetailAPI(RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


# Chat
class ChatListAPI(ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class ChatCreateAPI(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class ChatDetailAPI(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

# Collabo
class CollaboListAPI(ListAPIView):
    queryset = Collabo.objects.all()
    serializer_class = CollaboSerializer


class CollaboCreateAPI(CreateAPIView):
    queryset = Collabo.objects.all()
    serializer_class = CollaboSerializer


class CollaboDetailAPI(RetrieveAPIView):
    queryset = Collabo.objects.all()
    serializer_class = CollaboSerializer
