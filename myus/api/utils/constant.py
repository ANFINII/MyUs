from api.db.models import Video, Music, Comic, Picture, Blog, Chat
from api.db.models.comment import Comment
from api.db.models.message import Message
from api.db.models.users import Follow
from api.utils.functions.media import MediaModel


media_models: dict[str, type[MediaModel]] = {
    'Video': Video,
    'Music': Music,
    'Comic': Comic,
    'Picture': Picture,
    'Blog': Blog,
    'Chat': Chat,
}

model_list = [Video, Music, Comic, Picture, Blog, Chat]

model_dict = {
    Video  : "video",
    Music  : "music",
    Comic  : "comic",
    Picture: "picture",
    Blog   : "blog",
    Chat   : "chat",
}

model_pjax = {
    "media/video"  : Video,
    "media/music"  : Music,
    "media/comic"  : Comic,
    "media/picture": Picture,
    "media/blog"   : Blog,
    "media/chat"   : Chat,
}

model_create_pjax = (
    "media/video/create",
    "media/music/create",
    "media/comic/create",
    "media/picture/create",
    "media/blog/create",
    "media/chat/create",
)

model_like_dict = {
    "video/detail"  : Video,
    "music/detail"  : Music,
    "comic/detail"  : Comic,
    "picture/detail": Picture,
    "blog/detail"   : Blog,
    "chat/detail"   : Chat,
}

model_media_comment_dict = {
    "video"  : Video,
    "music"  : Music,
    "comic"  : Comic,
    "picture": Picture,
    "blog"   : Blog,
}

model_media_comment_no_dict = {
    "video"  : 1,
    "music"  : 2,
    "comic"  : 3,
    "picture": 4,
    "blog"   : 5,
}

model_comment_dict = {
    "video/detail"  : Video,
    "music/detail"  : Music,
    "comic/detail"  : Comic,
    "picture/detail": Picture,
    "blog/detail"   : Blog,
}

notification_type_no = {
    "is_video"  : 1,
    "is_music"  : 2,
    "is_comic"  : 3,
    "is_picture": 4,
    "is_blog"   : 5,
    "is_chat"   : 6,
    "is_follow" : 7,
    "is_like"   : 8,
    "is_reply"  : 9,
    "is_views"  : 10,
}

notification_type_model = {
    "video"  : Video,
    "music"  : Music,
    "comic"  : Comic,
    "picture": Picture,
    "blog"   : Blog,
    "chat"   : Chat,
    "follow" : Follow,
    "comment": Comment,
    "message": Message,
}
