from enum import Enum


class ImageUpload(str, Enum):
    USER = "user"
    MYPAGE = "mypage"
    CHANNEL = "channel"
    VIDEO = "video"
    BLOG = "blog"
    COMIC = "comic"
    COMIC_PAGE = "comic_page"
    PICTURE = "picture"
    ADVERTISE = "advertise"


class MediaUpload(str, Enum):
    VIDEO = "video"
    MUSIC = "music"
    ADVERTISE = "advertise"
