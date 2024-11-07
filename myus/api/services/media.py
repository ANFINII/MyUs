from api.models import User
from api.models import Video, Music, Comic, Picture, Blog, Chat, Todo
from api.utils.functions.index import create_url
from api.utils.functions.search import search_media, search_todo
from api.utils.functions.user import get_author


def get_home(count: int, search: str | None):
    data = {
        'videos': get_videos(count, search),
        'musics': get_musics(count, search),
        'pictures': get_pictures(count, search),
        'blogs': get_blogs(count, search),
        'chats': get_chats(count, search),
    }
    return data


def get_recommend(count: int, search: str | None):
    data = {
        'videos': get_videos(count, search),
        'musics': get_musics(count, search),
        'pictures': get_pictures(count, search),
        'blogs': get_blogs(count, search),
        'chats': get_chats(count, search),
    }
    return data


def get_videos(count: int, search: str | None):
    objs = Video.objects.none
    if search:
        objs = search_media(Video, search)
    else:
        objs = Video.objects.filter(publish=True).order_by('-created')[:count]

    data = [{
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'image': obj.image.url,
        'video': obj.video.url,
        'convert': obj.convert.url,
        'like': obj.total_like(),
        'read': obj.read,
        'comment_count': obj.comment_count(),
        'publish': obj.publish,
        'created': obj.created,
        'updated': obj.updated,
        'author': get_author(obj.author)
    } for obj in objs]
    return data


def get_musics(count: int, search: str | None):
    objs = Music.objects.none
    if search:
        objs = search_media(Music, search)
    else:
        objs = Music.objects.filter(publish=True).order_by('-created')[:count]

    data = [{
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'lyric': obj.lyric,
        'music': obj.music.url,
        'like': obj.total_like(),
        'read': obj.read,
        'comment_count': obj.comment_count(),
        'dowoad': obj.download,
        'publish': obj.publish,
        'created': obj.created,
        'updated': obj.updated,
        'author': get_author(obj.author)
    } for obj in objs]
    return data


def get_comics(count: int, search: str | None):
    objs = Comic.objects.none
    if search:
        objs = search_media(Comic, search)
    else:
        objs = Comic.objects.filter(publish=True).order_by('-created')[:count]

    data = [{
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'image': create_url(obj.image.url),
        'like': obj.total_like(),
        'read': obj.read,
        'publish': obj.publish,
        'created': obj.created,
        'updated': obj.updated,
        'author': get_author(obj.author)
    } for obj in objs]
    return data


def get_pictures(count: int, search: str | None):
    objs = Picture.objects.none
    if search:
        objs = search_media(Picture, search)
    else:
        objs = Picture.objects.filter(publish=True).order_by('-created')[:count]

    data = [{
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'image': create_url(obj.image.url),
        'like': obj.total_like(),
        'read': obj.read,
        'comment_count': obj.comment_count(),
        'publish': obj.publish,
        'created': obj.created,
        'updated': obj.updated,
        'author': get_author(obj.author)
    } for obj in objs]
    return data


def get_blogs(count: int, search: str | None):
    objs = Blog.objects.none
    if search:
        objs = search_media(Blog, search)
    else:
        objs = Blog.objects.filter(publish=True).order_by('-created')[:count]

    data = [{
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'richtext': obj.richtext,
        'image': create_url(obj.image.url),
        'like': obj.total_like(),
        'read': obj.read,
        'comment_count': obj.comment_count(),
        'publish': obj.publish,
        'created': obj.created,
        'updated': obj.updated,
        'author': get_author(obj.author)
    } for obj in objs]
    return data


def get_chats(count: int, search: str | None):
    objs = Chat.objects.none
    if search:
        objs = search_media(Chat, search)
    else:
        objs = Chat.objects.filter(publish=True).order_by('-created')[:count]

    data = [{
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'like': obj.total_like(),
        'read': obj.read,
        'thread': obj.thread_count(),
        'joined': obj.joined_count(),
        'period': obj.period,
        'publish': obj.publish,
        'created': obj.created,
        'updated': obj.updated,
        'author': get_author(obj.author)
    } for obj in objs]
    return data


def get_todos(count: int, user: User, search: str | None):
    objs = Todo.objects.none
    if search:
        objs = search_todo(Todo, user, search)
    else:
        objs = Todo.objects.filter(author=user.id).order_by('-created')[:count]

    data = [{
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'priority': obj.priority,
        'progress': obj.progress,
        'duedate': obj.duedate,
        'created': obj.created,
        'updated': obj.updated,
        'author': get_author(obj.author)
    } for obj in objs]
    return data
