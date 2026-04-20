from api.db.models.comment import Comment
from api.db.models.media import Video, Music, Blog, Comic, Picture, Chat
from api.db.models.message import Message
from api.db.models.users import Follow


type MediaModel = Video | Music | Blog | Comic | Picture | Chat


media_models: dict[str, type[MediaModel]] = {
    'Video': Video,
    'Music': Music,
    'Blog': Blog,
    'Comic': Comic,
    'Picture': Picture,
    'Chat': Chat,
}

model_list = [Video, Music, Blog, Comic, Picture, Chat]

model_dict = {
    Video  : "video",
    Music  : "music",
    Blog   : "blog",
    Comic  : "comic",
    Picture: "picture",
    Chat   : "chat",
}

model_pjax = {
    "media/video"  : Video,
    "media/music"  : Music,
    "media/blog"   : Blog,
    "media/comic"  : Comic,
    "media/picture": Picture,
    "media/chat"   : Chat,
}

model_create_pjax = (
    "media/video/create",
    "media/music/create",
    "media/blog/create",
    "media/comic/create",
    "media/picture/create",
    "media/chat/create",
)

model_like_dict = {
    "video/detail"  : Video,
    "music/detail"  : Music,
    "blog/detail"   : Blog,
    "comic/detail"  : Comic,
    "picture/detail": Picture,
    "chat/detail"   : Chat,
}

model_media_comment_dict = {
    "video"  : Video,
    "music"  : Music,
    "blog"   : Blog,
    "comic"  : Comic,
    "picture": Picture,
}

model_media_comment_no_dict = {
    "video"  : 1,
    "music"  : 2,
    "blog"   : 5,
    "comic"  : 3,
    "picture": 4,
}

model_comment_dict = {
    "video/detail"  : Video,
    "music/detail"  : Music,
    "blog/detail"   : Blog,
    "comic/detail"  : Comic,
    "picture/detail": Picture,
}

notification_type_no = {
    "is_video"  : 1,
    "is_music"  : 2,
    "is_blog"   : 5,
    "is_comic"  : 3,
    "is_picture": 4,
    "is_chat"   : 6,
    "is_follow" : 7,
    "is_like"   : 8,
    "is_reply"  : 9,
    "is_views"  : 10,
}

notification_type_model = {
    "video"  : Video,
    "music"  : Music,
    "blog"   : Blog,
    "comic"  : Comic,
    "picture": Picture,
    "chat"   : Chat,
    "follow" : Follow,
    "comment": Comment,
    "message": Message,
}
