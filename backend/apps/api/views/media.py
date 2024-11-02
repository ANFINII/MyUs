import json
import os

from django.db.models import Exists, OuterRef
from django.conf import settings

from config.settings.base import DOMAIN_URL
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.myus.models import Video, Music, Comic, ComicPage, Picture, Blog, Chat, Todo
from apps.myus.modules.search import Search
from apps.myus.convert.convert_hls import convert_exe
from apps.api.services.media import get_home, get_recommend, get_videos, get_musics, get_comics, get_pictures, get_blogs, get_chats, get_todos
from apps.api.services.user import get_user
from apps.api.utils.enum.response import ApiResponse
from apps.api.utils.functions.index import is_bool
from apps.api.utils.functions.comment import get_comment, get_comments
from apps.api.utils.functions.response import DataResponse
from apps.api.utils.functions.user import get_author, get_media_user


# Index
class HomeAPI(APIView):
    def get(self, request):
        search = request.query_params.get('search')
        data = get_home(8, search)
        return DataResponse(data, HTTP_200_OK)


# Recommend
class RecommendAPI(APIView):
    def get(self, request):
        search = request.query_params.get('search')
        data = get_recommend(8, search)
        return DataResponse(data, HTTP_200_OK)


# Video
class VideoListAPI(APIView):
    def get(self, request):
        search = request.query_params.get('search')
        data = get_videos(50, search)
        return DataResponse(data, HTTP_200_OK)


class VideoAPI(APIView):
    def get(self, request, id):
        obj = Video.objects.filter(id=id, publish=True).first()
        if not obj:
            return ApiResponse.NOT_FOUND.run()

        comments = get_comments(obj)

        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'image': obj.image.url,
            'video': obj.video.url,
            'convert': obj.convert.url,
            'comment': [get_comment(comment) for comment in comments],
            'hashtag': [hashtag.jp_name for hashtag in obj.hashtag.all()],
            'like': obj.total_like(),
            'read': obj.read,
            'comment_count': obj.comment_count(),
            'publish': obj.publish,
            'created': obj.created,
            'updated': obj.updated,
            'author': get_author(obj.author),
        }
        return DataResponse(data, HTTP_200_OK)

    def post(self, request):
        author = get_user(request)
        if not author:
            return ApiResponse.UNAUTHORIZED.run()

        data = request.data
        field = {
            'author': author,
            'title': data.get('title'),
            'content': data.get('content'),
            'image': data.get('image'),
        }

        obj = Video.objects.create(**field)
        obj_id = f'object_{obj.id}'
        user_id = f'user_{obj.author.id}'
        media_root = settings.MEDIA_ROOT
        video_path = os.path.join(media_root, 'videos', 'videos_video', user_id, obj_id)
        video_file = os.path.join(video_path, os.path.basename(f'{obj.convert}'))
        file_path = convert_exe(video_file, video_path, media_root)

        obj.convert = file_path['mp4_path']
        obj.video = file_path['hls_path']
        obj.save()

        data = {'id': obj.id}
        return DataResponse(data, HTTP_201_CREATED)


# Music
class MusicListAPI(APIView):
    def get(self, request):
        search = request.query_params.get('search')
        data = get_musics(50, search)
        return DataResponse(data, HTTP_200_OK)


class MusicAPI(APIView):
    def get(self, request, id):
        obj = Music.objects.filter(id=id, publish=True).first()
        if not obj:
            return ApiResponse.NOT_FOUND.run()

        comments = get_comments(obj)

        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'lyric': obj.lyric,
            'music': obj.music.url,
            'comment': [get_comment(comment) for comment in comments],
            'hashtag': [hashtag.jp_name for hashtag in obj.hashtag.all()],
            'like': obj.total_like(),
            'read': obj.read,
            'comment_count': obj.comment_count(),
            'publish': obj.publish,
            'created': obj.created,
            'updated': obj.updated,
            'author': get_author(obj.author),
        }
        return DataResponse(data, HTTP_200_OK)


    def post(self, request) -> Response:
        author = get_user(request)
        if not author:
            return ApiResponse.UNAUTHORIZED.run()

        data = request.data
        field = {
            'author': author,
            'title': data.get('title'),
            'content': data.get('content'),
            'lyric': data.get('lyric'),
            'music': data.get('music'),
            'download': is_bool(data.get('download')),
        }
        obj = Music.objects.create(**field)
        data = {'id': obj.id}
        return DataResponse(data, HTTP_201_CREATED)


# Comic
class ComicListAPI(APIView):
    def get(self, request):
        search = request.query_params.get('search')
        data = get_comics(50, search)
        return DataResponse(data, HTTP_200_OK)


class ComicAPI(APIView):
    def get(self, request, id):
        obj = Comic.objects.filter(id=id, publish=True).first()
        if not obj:
            return ApiResponse.NOT_FOUND.run()

        comments = get_comments(obj)

        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'comment': [get_comment(comment) for comment in comments],
            'hashtag': [hashtag.jp_name for hashtag in obj.hashtag.all()],
            'like': obj.total_like(),
            'read': obj.read,
            'comment_count': obj.comment_count(),
            'publish': obj.publish,
            'created': obj.created,
            'updated': obj.updated,
            'author': get_author(obj.author),
        }
        return DataResponse(data, HTTP_200_OK)

    def post(self, request) -> Response:
        author = get_user(request)
        if not author:
            return ApiResponse.UNAUTHORIZED.run()

        data = request.data
        images = data.getlist('images[]')
        field = {
            'author': author,
            'title': data.get('title'),
            'content': data.get('content'),
            'image': data.get('image'),
        }
        obj = Comic.objects.create(**field)

        comic_pages = [ComicPage(comic=obj, image=image, sequence=sequence) for sequence, image in enumerate(images, start=1)]
        ComicPage.objects.bulk_create(comic_pages)

        data = {'id': obj.id}
        return DataResponse(data, HTTP_201_CREATED)


# Picture
class PictureListAPI(APIView):
    def get(self, request):
        search = request.query_params.get('search')
        data = get_pictures(50, search)
        return DataResponse(data, HTTP_200_OK)


class PictureAPI(APIView):
    def get(self, request, id):
        obj = Picture.objects.filter(id=id, publish=True).first()
        if not obj:
            return ApiResponse.NOT_FOUND.run()

        comments = get_comments(obj)

        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'image': f'{DOMAIN_URL}/{obj.image.url}',
            'comment': [get_comment(comment) for comment in comments],
            'hashtag': [hashtag.jp_name for hashtag in obj.hashtag.all()],
            'like': obj.total_like(),
            'read': obj.read,
            'comment_count': obj.comment_count(),
            'publish': obj.publish,
            'created': obj.created,
            'updated': obj.updated,
            'author': get_author(obj.author),
        }
        return DataResponse(data, HTTP_200_OK)

    def post(self, request):
        author = get_user(request)
        if not author:
            return ApiResponse.UNAUTHORIZED.run()

        data = request.data
        field = {
            'author': author,
            'title': data.get('title'),
            'content': data.get('content'),
            'image': data.get('image'),
        }
        obj = Picture.objects.create(**field)
        data = {'id': obj.id}
        return DataResponse(data, HTTP_201_CREATED)


# Blog
class BlogListAPI(APIView):
    def get(self, request):
        search = request.query_params.get('search')
        data = get_blogs(50, search)
        return DataResponse(data, HTTP_200_OK)


class BlogAPI(APIView):
    def get(self, request, id):
        obj = Blog.objects.filter(id=id, publish=True).first()
        if not obj:
            return ApiResponse.NOT_FOUND.run()

        search = request.query_params.get('search')
        user = get_user(request)
        comments = get_comments(obj)

        data = {
            'detail': {
                'id': obj.id,
                'title': obj.title,
                'content': obj.content,
                'richtext': obj.richtext,
                'image': obj.image.url,
                'comment': [get_comment(comment) for comment in comments],
                'hashtag': [hashtag.jp_name for hashtag in obj.hashtag.all()],
                'like': obj.total_like(),
                'read': obj.read,
                'comment_count': obj.comment_count(),
                'publish': obj.publish,
                'created': obj.created,
                'updated': obj.updated,
                'author': get_author(obj.author),
            },
            'list': get_blogs(50, search),
        }
        if user:
            data['detail']['user'] = get_media_user(user, obj)

        return DataResponse(data, HTTP_200_OK)

    def post(self, request) -> Response:
        author = get_user(request)
        if not author:
            return ApiResponse.UNAUTHORIZED.run()

        data = request.data
        field = {
            'author': author,
            'title': data.get('title'),
            'content': data.get('content'),
            'image': data.get('image'),
            'richtext': data.get('richtext'),
            'delta': self.get_delta(data.get('delta'), data.get('richtext')),
        }
        obj = Blog.objects.create(**field)
        data = {'id': obj.id}
        return DataResponse(data, HTTP_201_CREATED)

    @staticmethod
    def get_delta(delta, html):
        quill = json.dumps({'delta': delta, 'html': html})
        return quill


# Chat
class ChatListAPI(APIView):
    def get(self, request):
        search = request.query_params.get('search')
        data = get_chats(50, search)
        return DataResponse(data, HTTP_200_OK)


class ChatAPI(APIView):
    def get(self, request, id):
        obj = Chat.objects.filter(id=id, publish=True).first()
        if not obj:
            return ApiResponse.NOT_FOUND.run()

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
            'author': get_author(obj.author),
        }
        return DataResponse(data, HTTP_200_OK)

    def post(self, request) -> Response:
        author = get_user(request)
        if not author:
            return ApiResponse.UNAUTHORIZED.run()

        data = request.data
        field = {
            'author': author,
            'title': data.get('title'),
            'content': data.get('content'),
            'period': data.get('period'),
        }
        obj = Chat.objects.create(**field)
        data = {'id': obj.id}
        return DataResponse(data, HTTP_201_CREATED)

# Todo
class TodoListAPI(APIView):
    def get(self, request):
        author = get_user(request)
        if not author:
            return ApiResponse.UNAUTHORIZED.run()

        search = request.query_params.get('search')
        data = get_todos(50, author, search)
        return DataResponse(data, HTTP_200_OK)


class TodoAPI(APIView):
    def get(self, request, id):
        obj = Todo.objects.filter(id=id, publish=True).first()
        if not obj:
            return ApiResponse.NOT_FOUND.run()

        filter_kwargs = {'id': OuterRef('pk'), 'like': obj.author.id}
        subquery = obj.comment.filter(**filter_kwargs)
        comments = obj.comment.all().annotate(is_comment_like=Exists(subquery))

        data = {
            'id': obj.id,
            'title': obj.title,
            'content': obj.content,
            'priority': obj.priority,
            'progress': obj.progress,
            'comment': [get_comment(comment) for comment in comments],
            'hashtag': [hashtag.jp_name for hashtag in obj.hashtag.all()],
            'like': obj.total_like(),
            'read': obj.read,
            'comment_count': obj.comment_count(),
            'duete': obj.duedate,
            'created': obj.created,
            'updated': obj.updated,
            'author': get_author(obj.author),
        }
        return DataResponse(data, HTTP_200_OK)

    def post(self, request):
        author = get_user(request)
        if not author:
            return ApiResponse.UNAUTHORIZED.run()

        data = request.data
        field = {
            'author': author,
            'title': data.get('title'),
            'content': data.get('content'),
            'priority': data.get('priority'),
            'progress': data.get('progress'),
            'duedate': data.get('duedate'),
        }
        obj = Todo.objects.create(**field)
        data = {'id': obj.id}
        return DataResponse(data, HTTP_201_CREATED)
