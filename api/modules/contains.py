from api.models import Video, Live, Music, Picture, Blog, Chat, Collabo, Todo


models_dict = {
    Video  : 'video',
    Live   : 'live',
    Music  : 'music',
    Picture: 'picture',
    Blog   : 'blog',
    Chat   : 'chat',
    Collabo: 'collabo',
}

models_like_dict = {
    'video/detail'  : Video,
    'live/detail'   : Live,
    'music/detail'  : Music,
    'picture/detail': Picture,
    'blog/detail'   : Blog,
    'chat/detail'   : Chat,
    'collabo/detail': Collabo,
}

models_comment_dict = {
    'video/detail'  : Video,
    'live/detail'   : Live,
    'music/detail'  : Music,
    'picture/detail': Picture,
    'blog/detail'   : Blog,
    'collabo/detail': Collabo,
    'todo/detail'   : Todo,
}

models_pjax = {
    'video'  : Video,
    'live'   : Live,
    'music'  : Music,
    'picture': Picture,
    'blog'   : Blog,
    'chat'   : Chat,
    'collabo': Collabo,
}

models_create_pjax = (
    'video/create',
    'live/create',
    'music/create',
    'picture/create',
    'blog/create',
    'chat/create',
    'collabo/create',
    'todo/create',
)

notification_type_dict = {
    'video'  : 'is_video',
    'live'   : 'is_live',
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
    live    = 2
    music   = 3
    picture = 4
    blog    = 5
    chat    = 6
    collabo = 7
    follow  = 8
    like    = 9
    reply   = 10
    views   = 11

class PlanType:
    free     = '0'
    basic    = '1'
    standard = '2'
    premium  = '3'
