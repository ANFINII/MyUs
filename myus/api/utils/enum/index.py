from enum import Enum


class GenderType(str, Enum):
    MALE = "male"
    FEMALE = "female"
    SECRET = "secret"


class NotificationType(str, Enum):
    VIDEO = "video"
    MUSIC = "music"
    COMIC = "comic"
    PICTURE = "picture"
    BLOG = "blog"
    CHAT = "chat"
