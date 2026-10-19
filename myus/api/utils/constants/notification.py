from api.db.models.comment import Comment
from api.db.models.media import Video, Music, Blog, Comic, Picture, Chat
from api.db.models.message import Message
from api.db.models.users import Follow


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
