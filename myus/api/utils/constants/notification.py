from api.db.models.comment import Comment
from api.db.models.media import Video, Music, Blog, Comic, Picture, Chat
from api.db.models.message import Message
from api.db.models.users import Follow


notification_type_no = {
    "is_video"  : 1,
    "is_music"  : 2,
    "is_blog"   : 3,
    "is_comic"  : 4,
    "is_picture": 5,
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
