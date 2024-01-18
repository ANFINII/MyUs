from apps.myus.models import Video, Music, Comic, Picture, Blog, Chat, Todo


def get_video_list(count):
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

def get_music_list(count):
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

def get_comic_list(count):
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

def get_picture_list(count):
    objs = Picture.objects.filter(publish=True).order_by('-created')[:count]
    data = [{
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'image': obj.image.url,
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

def get_blog_list(count):
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

def get_chat_list(count):
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


def get_todo_list(count):
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
