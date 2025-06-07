from enum import Enum


class GenderType(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    SECRET = "Secret"


class NotificationType(str, Enum):
    VIDEO = "Video"
    MUSIC = "Music"
    COMIC = "Comic"
    PICTURE = "Picture"
    BLOG = "Blog"
    CHAT = "Chat"
    FOLLOW = "Follow"
    LIKE = "Like"
    REPLY = "Reply"
    VIEWS = "Views"


class NotificationTypeNo(int, Enum):
    VIDEO = 1
    MUSIC = 2
    COMIC = 3
    PICTURE = 4
    BLOG = 5
    CHAT = 6
    FOLLOW = 7
    LIKE = 8
    REPLY = 9
    VIEWS = 10


class CommentType(str, Enum):
    VIDEO = "Video"
    MUSIC = "Music"
    COMIC = "Comic"
    PICTURE = "Picture"
    BLOG = "Blog"


class CommentTypeNo(int, Enum):
    VIDEO = 1
    MUSIC = 2
    COMIC = 3
    PICTURE = 4
    BLOG = 5
