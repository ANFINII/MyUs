from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef

# from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.myus.models import Video, Music, Comic, ComicPage, Picture, Blog, Chat, Todo
from apps.myus.modules.search import Search
from apps.api.serializers import VideoSerializer, MusicSerializer, ComicSerializer
from apps.api.serializers import PictureSerializer, BlogSerializer, ChatSerializer, TodoSerializer
from apps.api.services.media import get_home, get_recommend, get_videos, get_musics, get_comics, get_pictures, get_blogs, get_chats, get_todos
from apps.api.services.user import get_user
from rest_framework.response import Response


# Index
class HomeAPI(APIView):
    def get(self, request):
        data = get_home(8)
        return Response(data, status=HTTP_200_OK)


# Recommend
class RecommendAPI(APIView):
    def get(self, request):
        data = get_recommend(8)
        return Response(data, status=HTTP_200_OK)


# Video
class VideoListAPI(APIView):
    def get(self, request):
        data = get_videos(50)
        return Response(data, status=HTTP_200_OK)

    def get_queryset(self):
        return Search.search_models(self, Video)


class VideoCreateAPI(CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoAPI(APIView):
    def get(self, request, id):
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
        data = get_musics(50)
        return Response(data, status=HTTP_200_OK)


class MusicCreateAPI(CreateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


class MusicAPI(APIView):
    def get(self, request, id):
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


# Comic
class ComicListAPI(APIView):
    def get(self, request):
        data = get_comics(50)
        return Response(data, status=HTTP_200_OK)


class ComicCreateAPI(CreateAPIView):
    def post(self, request) -> Response:
        author = get_user(request)
        if not author:
            return Response({'message': '認証されていません!'}, status=HTTP_400_BAD_REQUEST)

        data = request.data
        title = data.get('title')
        content = data.get('content')
        image = data.get('image')
        images = data.getlist('images[]')

        obj = Comic.objects.create(author=author, title=title, content=content, image=image)
        for sequence, image in enumerate(images, start=1):
            ComicPage.objects.create(comic=obj, image=image, sequence=sequence)

        data = {'id': obj.id}
        return Response(data, status=HTTP_201_CREATED)


class ComicAPI(APIView):
    def get(self, request, id):
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


# Picture
class PictureListAPI(APIView):
    def get(self, request):
        data = get_pictures(50)
        return Response(data, status=HTTP_200_OK)


class PictureCreateAPI(APIView):
    def post(self, request):
        author = get_user(request)
        if not author:
            return Response({'message': '認証されていません!'}, status=HTTP_400_BAD_REQUEST)

        data = request.data
        title = data.get('title')
        content = data.get('content')
        image = data.get('image')
        obj = Picture.objects.create(author=author, title=title, content=content, image=image)
        data = {'id': obj.id}
        return Response(data, status=HTTP_201_CREATED)


class PictureAPI(APIView):
    def get(self, request, id):
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


# Blog
class BlogListAPI(APIView):
    def get(self, request):
        data = get_blogs(50)
        return Response(data, status=HTTP_200_OK)


class BlogCreateAPI(APIView):
    def post(self, request) -> Response:
        author = get_user(request)
        if not author:
            return Response({'message': '認証されていません!'}, status=HTTP_400_BAD_REQUEST)

        data = request.data
        title = data.get('title')
        content = data.get('content')
        image = data.get('image')
        richtext = data.get('richtext')

        obj = Blog.objects.create(author=author, title=title, content=content, image=image, richtext=richtext)
        data = {'id': obj.id}
        return Response(data, status=HTTP_201_CREATED)


class BlogAPI(APIView):
    def get(self, request, id):
        obj = Blog.objects.filter(id=id, publish=True).first()
        if not obj:
            return Response('not objects', status=HTTP_400_BAD_REQUEST)

        author = obj.author
        user = get_user(request)
        filter_kwargs = {'id': OuterRef('pk'), 'like': author.id}
        subquery = obj.comment.filter(**filter_kwargs)
        comments = obj.comment.filter(parent__isnull=True).annotate(is_comment_like=Exists(subquery))

        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'richtext': obj.richtext,
            # 'delta': obj.delta,
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
            'publish': obj.publish,
            'created': obj.created,
            'updated': obj.updated,
            'author': {
                'nickname': author.nickname,
                'image': author.image(),
                'follower_count': author.mypage.follower_count
            },
        }
        if user:
            data['user'] = {
                'nickname': user.nickname,
                'image': user.image(),
                'is_like': obj.like.filter(id=user.id).exists()
            }
        return Response(data, status=HTTP_200_OK)



# Chat
class ChatListAPI(APIView):
    def get(self, request):
        data = get_chats(50)
        return Response(data, status=HTTP_200_OK)


class ChatCreateAPI(CreateAPIView):
    def post(self, request) -> Response:
        author = get_user(request)
        if not author:
            return Response({'message': '認証されていません!'}, status=HTTP_400_BAD_REQUEST)

        data = request.data
        title = data.get('title')
        content = data.get('content')
        period = data.get('period')

        obj = Chat.objects.create(author=author, title=title, content=content, period=period)
        data = {'id': obj.id}
        return Response(data, status=HTTP_201_CREATED)


class ChatAPI(APIView):
    def get(self, request, id):
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
    def get(self, request):
        data = get_todos(50)
        return Response(data, status=HTTP_200_OK)


class TodoCreateAPI(CreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class TodoAPI(APIView):
    def get(self, request, id):
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
