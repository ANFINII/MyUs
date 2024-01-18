from django.db.models import Exists, OuterRef

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.api.serializers import VideoSerializer, MusicSerializer, ComicSerializer
from apps.api.serializers import PictureSerializer, BlogSerializer, ChatSerializer, TodoSerializer
from apps.myus.models import Video, Music, Comic, Picture, Blog, Chat, Todo
from apps.myus.modules.search import Search
from apps.api.services.media import get_video_list, get_music_list, get_comic_list, get_picture_list, get_blog_list, get_chat_list, get_todo_list


# Index
class HomeAPI(ListAPIView):
    def get(self, request):
        datas = {
            'videos': get_video_list(8),
            'musics': get_music_list(8),
            'pictures': get_picture_list(8),
            'blogs': get_blog_list(8),
            'chats': get_chat_list(8),
        }
        return Response(datas, status=HTTP_200_OK)


# Recommend
class RecommendAPI(ListAPIView):
    def get(self, request):
        datas = {
            'videos': get_video_list(8),
            'musics': get_music_list(8),
            'pictures': get_picture_list(8),
            'blogs': get_blog_list(8),
            'chats': get_chat_list(8),
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
        data = get_music_list(50)
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


class BlogAPI(APIView):
    def get(self, request, id):
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
        data = get_todo_list(50)
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
