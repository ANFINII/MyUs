import jwt
import json
from datetime import date

from django.db.models import F, Count, Exists, OuterRef
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView, View
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt import views
from rest_framework_simplejwt import exceptions

from apps.api.serializers import SignUpSerializer, LoginSerializer
from apps.api.serializers import UserSerializer, ProfileSerializer, MyPageSerializer
from apps.api.serializers import VideoSerializer, MusicSerializer, ComicSerializer
from apps.api.serializers import PictureSerializer, BlogSerializer, ChatSerializer, TodoSerializer
from apps.api.utils import get_user_id
from apps.myus.modules.filter_data import DeferData
from apps.myus.modules.validation import has_username, has_email, has_phone, has_postal_code, has_alphabet, has_number
from apps.myus.models import Profile, MyPage, SearchTag, HashTag, NotificationSetting
from apps.myus.models import Notification, Follow, Comment, Message, Advertise
from apps.myus.models import Video, Music, Comic, Picture, Blog, Chat, Todo
from apps.myus.modules.search import Search
from apps.api.services.media import get_video_list, get_music_list, get_comic_list, get_picture_list, get_blog_list, get_chat_list, get_todo_list


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
        return Response({'success': 'logout'}, status=HTTP_204_NO_CONTENT)


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


class UserAPI(APIView):
    def get(self, request):
        user_id = get_user_id(request)
        user = User.objects.filter(id=user_id).defer(*DeferData.user).first()
        data = {'avatar': user.image(), 'nickname': user.nickname, 'is_staff': user.is_staff}
        return Response(data, status=HTTP_200_OK)


class ProfileAPI(APIView):
    def get(self, request):
        user_id = get_user_id(request)
        user = User.objects.filter(id=user_id).select_related('profile').defer(*DeferData.profile).first()
        gender = {'0':'男性', '1':'女性', '2':'秘密'}

        data = {
            'avatar': user.image(),
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
        return Response(data, status=HTTP_200_OK)

    def post(self, request):
        pass


class MyPageAPI(APIView):
    def get(self, request):
        user_id = get_user_id(request)
        user = User.objects.filter(id=user_id).select_related('mypage').defer(*DeferData.mypage).first()

        data = {
            'banner': user.banner(),
            'nickname': user.nickname,
            'email': user.mypage.email,
            'content': user.mypage.content,
            'follower_count': user.mypage.follower_count,
            'following_count': user.mypage.following_count,
            'plan': user.plan(),
            'plan_start_date': user.plan_start_date(),
            'plan_end_date': user.plan_end_date(),
            'is_advertise': user.mypage.is_advertise,
        }
        return Response(data, status=HTTP_200_OK)

    def post(self, request):
        pass


class NotificationAPI(APIView):
    def get(self, request):
        user_id = get_user_id(request)
        notification_setting = NotificationSetting.objects.filter(id=user_id).first()

        data = {
            'is_video': notification_setting.is_video,
            'is_music': notification_setting.is_music,
            'is_comic': notification_setting.is_comic,
            'is_picture': notification_setting.is_picture,
            'is_blog': notification_setting.is_blog,
            'is_chat': notification_setting.is_chat,
            'is_follow': notification_setting.is_follow,
            'is_reply': notification_setting.is_reply,
            'is_like': notification_setting.is_like,
            'is_views': notification_setting.is_views,
        }
        return Response(data, status=HTTP_200_OK)

    def post(self, request):
        pass


# Index
class HomeAPI(ListAPIView):
    def get(self, request):
        datas = {
            'videos': get_video_list(8),
            'musics': get_music_list(8),
            'pictures': get_picture_list(8),
            # 'blogs': get_blog_list(8),
            'chats': get_chat_list(8),
        }
        return Response(datas, status=HTTP_200_OK)


# Recommend
class RecommendAPI(ListAPIView):
    def get(self, request):
        datas = {
            'videos': get_video_list(8),
            'musics': get_video_list(8),
            'pictures': get_picture_list(8),
            'blogs': get_blog_list(8),
            'chats': get_picture_list(8),
        }
        return Response(datas, status=HTTP_200_OK)


# Video
class VideoListAPI(APIView):
    def get(self, request):
        data = get_video_list(50)
        return Response(data, status=HTTP_200_OK)

    def get_queryset(self):
        return Search.search_models(self, Video)


class VideoCreateAPI(CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoAPI(RetrieveAPIView):
    def get(self, id):
        obj = Video.objects.filter(id=id, publish=True).first()
        if not obj:
            return Response('not objects', status=HTTP_400_BAD_REQUEST)

        user_id = obj.author.id
        filter_kwargs = {'id': OuterRef('pk'), 'like': user_id}
        subquery = obj.comment.filter(**filter_kwargs)
        comments = obj.comment.filter(parent__isnull=True).annotate(is_comment_like=Exists(subquery))

        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'image': obj.image.url,
            'video': obj.video.url,
            'convert': obj.convert.url,
            'comment': [{
                'id': comment.id,
                'text': comment.text,
                'reply_count': comment.reply_count(),
                'created': comment.created,
                'author': comment.author.id,
                'image': comment.author.image(),
                'nickname': comment.author.nickname
            } for comment in comments],
            'hashtag': [hashtag.jp_name for hashtag in obj.hashtag.all()],
            'like': obj.total_like(),
            'read': obj.read,
            'comment_count': obj.comment_count(),
            'publish': obj.publish,
            'created': obj.created,
            'updated': obj.updated,
            'author': {
                'id': obj.author.id,
                'nickname': obj.author.nickname,
                'image': obj.author.image(),
            }
        }
        return Response(data, status=HTTP_200_OK)


# Music
class MusicListAPI(APIView):
    def get(self, request):
        data = get_music_list(50)
        return Response(data, status=HTTP_200_OK)


class MusicCreateAPI(CreateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


class MusicAPI(RetrieveAPIView):
    def get(self, id):
        obj = Music.objects.filter(id=id, publish=True).first()
        if not obj:
            return Response('not objects', status=HTTP_400_BAD_REQUEST)

        user_id = obj.author.id
        filter_kwargs = {'id': OuterRef('pk'), 'like': user_id}
        subquery = obj.comment.filter(**filter_kwargs)
        comments = obj.comment.filter(parent__isnull=True).annotate(is_comment_like=Exists(subquery))

        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'lyric': obj.lyric,
            'music': obj.music.url,
            'comment': [{
                'id': comment.id,
                'text': comment.text,
                'reply_count': comment.reply_count(),
                'created': comment.created,
                'author': comment.author.id,
                'image': comment.author.image(),
                'nickname': comment.author.nickname
            } for comment in comments],
            'hashtag': [hashtag.jp_name for hashtag in obj.hashtag.all()],
            'like': obj.total_like(),
            'read': obj.read,
            'comment_count': obj.comment_count(),
            'pubsh': obj.publish,
            'created': obj.created,
            'updated': obj.updated,
            'author': {
                'id': obj.author.id,
                'nickname': obj.author.nickname,
                'image': obj.author.image(),
            }
        }
        return Response(data, status=HTTP_200_OK)


# Comic
class ComicListAPI(APIView):
    def get(self, request):
        data = get_comic_list(50)
        return Response(data, status=HTTP_200_OK)


class ComicCreateAPI(CreateAPIView):
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer


class ComicAPI(RetrieveAPIView):
    def get(self, id):
        obj = Comic.objects.filter(id=id, publish=True).first()
        if not obj:
            return Response('not objects', status=HTTP_400_BAD_REQUEST)

        user_id = obj.author.id
        filter_kwargs = {'id': OuterRef('pk'), 'like': user_id}
        subquery = obj.comment.filter(**filter_kwargs)
        comments = obj.comment.filter(parent__isnull=True).annotate(is_comment_like=Exists(subquery))

        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'comment': [{
                'id': comment.id,
                'text': comment.text,
                'reply_count': comment.reply_count(),
                'created': comment.created,
                'author': comment.author.id,
                'image': comment.author.image(),
                'nickname': comment.author.nickname
            } for comment in comments],
            'hashtag': [hashtag.jp_name for hashtag in obj.hashtag.all()],
            'like': obj.total_like(),
            'read': obj.read,
            'comment_count': obj.comment_count(),
            'pubsh': obj.publish,
            'created': obj.created,
            'updated': obj.updated,
            'author': {
                'id': obj.author.id,
                'nickname': obj.author.nickname,
                'image': obj.author.image(),
            }
        }
        return Response(data, status=HTTP_200_OK)


# Picture
class PictureListAPI(APIView):
    def get(self, request):
        data = get_picture_list(50)
        return Response(data, status=HTTP_200_OK)


class PictureCreateAPI(CreateAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureAPI(RetrieveAPIView):
    def get(self, id):
        obj = Picture.objects.filter(id=id, publish=True).first()
        if not obj:
            return Response('not objects', status=HTTP_400_BAD_REQUEST)

        user_id = obj.author.id
        filter_kwargs = {'id': OuterRef('pk'), 'like': user_id}
        subquery = obj.comment.filter(**filter_kwargs)
        comments = obj.comment.filter(parent__isnull=True).annotate(is_comment_like=Exists(subquery))

        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'image': obj.image.url,
            'comment': [{
                'id': comment.id,
                'text': comment.text,
                'reply_count': comment.reply_count(),
                'created': comment.created,
                'author': comment.author.id,
                'image': comment.author.image(),
                'nickname': comment.author.nickname
            } for comment in comments],
            'hashtag': [hashtag.jp_name for hashtag in obj.hashtag.all()],
            'like': obj.total_like(),
            'read': obj.read,
            'comment_count': obj.comment_count(),
            'pubsh': obj.publish,
            'created': obj.created,
            'updated': obj.updated,
            'author': {
                'id': obj.author.id,
                'nickname': obj.author.nickname,
                'image': obj.author.image(),
            }
        }
        return Response(data, status=HTTP_200_OK)


# Blog
class BlogListAPI(APIView):
    def get(self, request):
        data = get_blog_list(50)
        return Response(data, status=HTTP_200_OK)


class BlogCreateAPI(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogAPI(RetrieveAPIView):
    def get(self, id):
        obj = Blog.objects.filter(id=id, publish=True).first()
        if not obj:
            return Response('not objects', status=HTTP_400_BAD_REQUEST)

        user_id = obj.author.id
        filter_kwargs = {'id': OuterRef('pk'), 'like': user_id}
        subquery = obj.comment.filter(**filter_kwargs)
        comments = obj.comment.filter(parent__isnull=True).annotate(is_comment_like=Exists(subquery))

        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'richtext': obj.richtext,
            'delta': obj.delta,
            'image': obj.image.url,
            'comment': [{
                'id': comment.id,
                'text': comment.text,
                'reply_count': comment.reply_count(),
                'created': comment.created,
                'author': comment.author.id,
                'image': comment.author.image(),
                'nickname': comment.author.nickname
            } for comment in comments],
            'hashtag': [hashtag.jp_name for hashtag in obj.hashtag.all()],
            'like': obj.total_like(),
            'read': obj.read,
            'comment_count': obj.comment_count(),
            'pubsh': obj.publish,
            'created': obj.created,
            'updated': obj.updated,
            'author': {
                'id': obj.author.id,
                'nickname': obj.author.nickname,
                'image': obj.author.image(),
            }
        }
        return Response(data, status=HTTP_200_OK)



# Chat
class ChatListAPI(APIView):
    def get(self, request):
        data = get_chat_list(50)
        return Response(data, status=HTTP_200_OK)


class ChatCreateAPI(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class ChatAPI(RetrieveAPIView):
    def get(self, id):
        obj = Chat.objects.filter(id=id, publish=True).first()
        if not obj:
            return Response('not objects', status=HTTP_400_BAD_REQUEST)

        messages = obj.message.filter(parent__isnull=True).select_related('author')

        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'message': [{
                'id': message.id,
                'text': message.text,
                'reply_count': message.reply_count,
                'created': message.created,
                'author': message.author.id,
                'image': message.author.image(),
                'nickname': message.author.nickname
            } for message in messages],
            'hashtag': [hashtag.jp_name for hashtag in obj.hashtag.all()],
            'like': obj.total_like(),
            'read': obj.read,
            'thread': obj.thread,
            'joined': obj.joined,
            'period': obj.period,
            'publish': obj.publish,
            'created': obj.created,
            'updated': obj.updated,
            'author': {
                'id': obj.author.id,
                'nickname': obj.author.nickname,
                'image': obj.author.image(),
            }
        }
        return Response(data, status=HTTP_200_OK)


# Todo
class TodoListAPI(APIView):
    def get(self, request, count=50):
        data = get_todo_list(50)
        return Response(data, status=HTTP_200_OK)


class TodoCreateAPI(CreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class TodoAPI(RetrieveAPIView):
    def get(self, id):
        obj = Todo.objects.filter(id=id, publish=True).first()
        if not obj:
            return Response('not objects', status=HTTP_400_BAD_REQUEST)

        user_id = obj.author.id
        filter_kwargs = {'id': OuterRef('pk'), 'like': user_id}
        subquery = obj.comment.filter(**filter_kwargs)
        comments = obj.comment.all().annotate(is_comment_like=Exists(subquery))

        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'priority': obj.priority,
            'progress': obj.progress,
            'comment': [{
                'id': comment.id,
                'text': comment.text,
                'reply_count': comment.reply_count(),
                'created': comment.created,
                'author': comment.author.id,
                'image': comment.author.image(),
                'nickname': comment.author.nickname
            } for comment in comments],
            'hashtag': [hashtag.jp_name for hashtag in obj.hashtag.all()],
            'like': obj.total_like(),
            'read': obj.read,
            'comment_count': obj.comment_count(),
            'duete': obj.duedate,
            'created': obj.created,
            'updated': obj.updated,
            'author': {
                'id': obj.author.id,
                'nickname': obj.author.nickname,
                'image': obj.author.image(),
            }
        }
        return Response(data, status=HTTP_200_OK)
