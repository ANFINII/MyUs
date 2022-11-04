from apps.myus.models import Video, Music, Picture, Blog, Chat, Collabo, Todo


model_list = [Video, Music, Picture, Blog, Chat]

model_dict = {
    Video  : 'video',
    Music  : 'music',
    Picture: 'picture',
    Blog   : 'blog',
    Chat   : 'chat',
}

model_dict_type = {
    Video  : 'video',
    Music  : 'music',
    Picture: 'picture',
    Blog   : 'blog',
    Chat   : 'chat',
    Collabo: 'collabo',
}

model_like_dict = {
    'video/detail'  : Video,
    'music/detail'  : Music,
    'picture/detail': Picture,
    'blog/detail'   : Blog,
    'chat/detail'   : Chat,
    'collabo/detail': Collabo,
}

model_comment_dict = {
    'video/detail'  : Video,
    'music/detail'  : Music,
    'picture/detail': Picture,
    'blog/detail'   : Blog,
    'collabo/detail': Collabo,
    'todo/detail'   : Todo,
}

model_pjax = {
    'video'  : Video,
    'music'  : Music,
    'picture': Picture,
    'blog'   : Blog,
    'chat'   : Chat,
    'collabo': Collabo,
}

model_create_pjax = (
    'video/create',
    'music/create',
    'picture/create',
    'blog/create',
    'chat/create',
    'collabo/create',
    'todo/create',
)

notification_type_dict = {
    'video'  : 'is_video',
    'music'  : 'is_music',
    'picture': 'is_picture',
    'blog'   : 'is_blog',
    'chat'   : 'is_chat',
    'collabo': 'is_collabo',
    'follow' : 'is_follow',
    'like'   : 'is_like',
    'reply'  : 'is_reply',
    'views'  : 'is_views',
}

class NotificationTypeNo:
    video   = 1
    music   = 2
    picture = 3
    blog    = 4
    chat    = 5
    collabo = 6
    follow  = 7
    like    = 8
    reply   = 9
    views   = 10
