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

notification_type_dict = {
    'video'  : [1 , 'is_video'],
    'live'   : [2 , 'is_live'],
    'music'  : [3 , 'is_music'],
    'picture': [4 , 'is_picture'],
    'blog'   : [5 , 'is_blog'],
    'chat'   : [6 , 'is_chat'],
    'collabo': [7 , 'is_collabo'],
    'follow' : [8 , 'is_follow'],
    'like'   : [9 , 'is_like'],
    'reply'  : [10, 'is_reply'],
    'views'  : [11, 'is_views'],
}
