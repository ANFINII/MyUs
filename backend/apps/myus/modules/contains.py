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

notification_type_no = {
    'is_video'  : 1,
    'is_music'  : 2,
    'is_picture': 3,
    'is_blog'   : 4,
    'is_chat'   : 5,
    'is_collabo': 6,
    'is_follow' : 7,
    'is_like'   : 8,
    'is_reply'  : 9,
    'is_views'  : 10,
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
