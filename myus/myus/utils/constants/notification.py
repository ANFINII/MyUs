from myus.db.models.comment import Comment
from myus.db.models.media import Video, Audio, Blog, Comic, Picture, Chat
from myus.db.models.message import Message
from myus.db.models.users import Follow


notification_type_model = {
    "video"  : Video,
    "audio"  : Audio,
    "blog"   : Blog,
    "comic"  : Comic,
    "picture": Picture,
    "chat"   : Chat,
    "follow" : Follow,
    "comment": Comment,
    "message": Message,
}
