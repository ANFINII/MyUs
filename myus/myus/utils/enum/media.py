from enum import Enum


class MediaType(str, Enum):
    VIDEO = "Video"
    MUSIC = "Music"
    BLOG = "Blog"
    COMIC = "Comic"
    PICTURE = "Picture"
    CHAT = "Chat"


class HomeSort(str, Enum):
    RECOMMEND = "Recommend"
    TRENDING = "Trending"
    LATEST = "Latest"


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


class EncodeStatus(str, Enum):
    ENCODING = "Encoding"
    DONE = "Done"
    FAILED = "Failed"
