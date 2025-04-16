from enum import Enum
from api.models import Video, Music, Comic, Picture, Blog, Chat


MediaModelType = Video | Music | Comic | Picture | Blog | Chat


class NotificationType(str, Enum):
    VIDEO = "video"
    MUSIC = "music"
    COMIC = "comic"
    PICTURE = "picture"
    BLOG = "blog"
    CHAT = "chat"
