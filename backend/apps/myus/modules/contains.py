from apps.myus.models import Video, Music, Comic, Picture, Blog, Chat, Todo


model_list = [Video, Music, Comic, Picture, Blog, Chat]

model_dict = {
    Video  : 'video',
    Music  : 'music',
    Comic  : 'comic',
    Picture: 'picture',
    Blog   : 'blog',
    Chat   : 'chat',
}

model_like_dict = {
    'video/detail'  : Video,
    'music/detail'  : Music,
    'comic/detail'  : Comic,
    'picture/detail': Picture,
    'blog/detail'   : Blog,
    'chat/detail'   : Chat,
}

model_comment_dict = {
    'video/detail'  : Video,
    'music/detail'  : Music,
    'comic/detail'  : Comic,
    'picture/detail': Picture,
    'blog/detail'   : Blog,
    'todo/detail'   : Todo,
}

model_pjax = {
    'video'  : Video,
    'music'  : Music,
    'comic'  : Comic,
    'picture': Picture,
    'blog'   : Blog,
    'chat'   : Chat,
}

model_create_pjax = (
    'video/create',
    'music/create',
    'comic/create',
    'picture/create',
    'blog/create',
    'chat/create',
    'todo/create',
)

notification_type_no = {
    'is_video'  : 1,
    'is_music'  : 2,
    'is_comic'  : 3,
    'is_picture': 4,
    'is_blog'   : 5,
    'is_chat'   : 6,
    'is_follow' : 7,
    'is_like'   : 8,
    'is_reply'  : 9,
    'is_views'  : 10,
}

class NotificationTypeNo:
    video   = 1
    music   = 2
    comic   = 3
    picture = 4
    blog    = 5
    chat    = 6
    follow  = 7
    like    = 8
    reply   = 9
    views   = 10
