from api.models import Video, Live, Music, Picture, Blog, Chat, Collabo, Todo

models_dict = {
    Video: 'video',
    Live: 'live',
    Music: 'music',
    Picture: 'picture',
    Blog: 'blog',
    Chat: 'chat',
    Collabo: 'collabo',
}

models_like_dict = {
    'video/detail': Video,
    'live/detail': Live,
    'music/detail': Music,
    'picture/detail': Picture,
    'blog/detail': Blog,
    'chat/detail': Chat,
    'collabo/detail': Collabo,
}

models_comment_dict = {
    'video/detail': Video,
    'live/detail': Live,
    'music/detail': Music,
    'picture/detail': Picture,
    'blog/detail': Blog,
    'collabo/detail': Collabo,
    'todo/detail': Todo,
}

notification_type_no = {
    'video'  : 1,
    'live'   : 2,
    'music'  : 3,
    'picture': 4,
    'blog'   : 5,
    'chat'   : 6,
    'collabo': 7,
    'follow' : 8,
    'like'   : 9,
    'reply'  : 10,
    'views'  : 11,
}
