from enum import Enum


class GenderType(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    SECRET = "Secret"


class MediaType(str, Enum):
    VIDEO = "Video"
    MUSIC = "Music"
    BLOG = "Blog"
    COMIC = "Comic"
    PICTURE = "Picture"
    CHAT = "Chat"


class NotificationType(str, Enum):
    VIDEO = "Video"
    MUSIC = "Music"
    BLOG = "Blog"
    COMIC = "Comic"
    PICTURE = "Picture"
    CHAT = "Chat"
    FOLLOW = "Follow"
    LIKE = "Like"
    REPLY = "Reply"
    VIEWS = "Views"


class NotificationTypeNo(int, Enum):
    VIDEO = 1
    MUSIC = 2
    BLOG = 3
    COMIC = 4
    PICTURE = 5
    CHAT = 6
    FOLLOW = 7
    LIKE = 8
    REPLY = 9
    VIEWS = 10


class NotificationObjectType(str, Enum):
    VIDEO = "Video"
    MUSIC = "Music"
    BLOG = "Blog"
    COMIC = "Comic"
    PICTURE = "Picture"
    CHAT = "Chat"
    FOLLOW = "Follow"
    COMMENT = "Comment"
    MESSAGE = "Message"


class CommentTypeNo(int, Enum):
    VIDEO = 1
    MUSIC = 2
    BLOG = 3
    COMIC = 4
    PICTURE = 5


class CommentType(str, Enum):
    VIDEO = "Video"
    MUSIC = "Music"
    BLOG = "Blog"
    COMIC = "Comic"
    PICTURE = "Picture"


class ImageUpload(str, Enum):
    USER = "user"
    MYPAGE = "mypage"
    CHANNEL = "channel"
    VIDEO = "video"
    BLOG = "blog"
    COMIC = "comic"
    COMIC_PAGE = "comic_page"
    PICTURE = "picture"


class MediaUpload(str, Enum):
    VIDEO = "video"
    MUSIC = "music"
    ADVERTISE = "advertise"
