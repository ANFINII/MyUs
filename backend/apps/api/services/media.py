from apps.myus.models import Video, Music, Comic, Picture, Blog, Chat, Todo
from config.settings.base import DOMAIN_URL


def get_home(count: int):
    data = {
        'videos': get_videos(count),
        'musics': get_musics(count),
        'pictures': get_pictures(count),
        'blogs': get_blogs(count),
        'chats': get_chats(count),
    }
    return data


def get_recommend(count: int):
    data = {
        'videos': get_videos(count),
        'musics': get_musics(count),
        'pictures': get_pictures(count),
        'blogs': get_blogs(count),
        'chats': get_chats(count),
    }
    return data


def get_videos(count: int):
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
        'author': {
            'id': obj.author.id,
            'nickname': obj.author.nickname,
            'image': obj.author.image(),
        }
    } for obj in objs]
    return data


def get_musics(count: int):
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
        'author': {
            'id': obj.author.id,
            'nickname': obj.author.nickname,
            'image': obj.author.image(),
        }
    } for obj in objs]
    return data


def get_comics(count: int):
    objs = Comic.objects.filter(publish=True).order_by('-created')[:count]
    data = [{
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'like': obj.total_like(),
        'read': obj.read,
        'publish': obj.publish,
        'created': obj.created,
        'updated': obj.updated,
        'author': {
            'id': obj.author.id,
            'nickname': obj.author.nickname,
            'image': obj.author.image(),
        }
    } for obj in objs]
    return data


def get_pictures(count: int):
    objs = Picture.objects.filter(publish=True).order_by('-created')[:count]
    data = [{
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'image': f'{DOMAIN_URL}{obj.image.url}',
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
    } for obj in objs]
    return data


def get_blogs(count: int):
    objs = Blog.objects.filter(publish=True).order_by('-created')[:count]
    data = [{
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'richtext': obj.richtext,
        # 'delta': obj.delta,
        'image': obj.image.url,
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
    } for obj in objs]
    return data


def get_chats(count: int):
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
        'author': {
            'id': obj.author.id,
            'nickname': obj.author.nickname,
            'image': obj.author.image(),
        }
    } for obj in objs]
    return data


def get_todos(count: int):
    objs = Todo.objects.all().order_by('-created')[:count]
    data = [{
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'like': obj.total_like(),
        'read': obj.read,
        'period': obj.period,
        'publish': obj.publish,
        'created': obj.created,
        'updated': obj.updated,
        'author': {
            'id': obj.author.id,
            'nickname': obj.author.nickname,
            'image': obj.author.image(),
        }
    } for obj in objs]
    return data
