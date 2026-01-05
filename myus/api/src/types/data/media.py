from datetime import datetime
from dataclasses import dataclass
from api.src.types.data.comment import CommentData
from api.src.types.data.message import MessageData
from api.src.types.data.user import AuthorData, MediaUserData


@dataclass(frozen=True, slots=True)
class HashtagData:
    jp_name: str


@dataclass(frozen=True, slots=True)
class MediaCreateData:
    ulid: str


@dataclass(frozen=True, slots=True)
class MediaData:
    ulid: str
    title: str
    content: str
    read: int
    like_count: int
    publish: bool
    created: datetime
    updated: datetime
    author: AuthorData


@dataclass(frozen=True, slots=True)
class MediaDetailData:
    id: int
    ulid: str
    title: str
    content: str
    read: int
    like_count: int
    publish: bool
    created: datetime
    updated: datetime
    author: AuthorData
    mediaUser: MediaUserData
    hashtags: list[HashtagData]


@dataclass(frozen=True, slots=True)
class VideoData(MediaData):
    image: str
    video: str
    convert: str
    comment_count: int


@dataclass(frozen=True, slots=True)
class VideoDetailData(MediaDetailData):
    image: str
    video: str
    convert: str
    comments: list[CommentData]


@dataclass(frozen=True, slots=True)
class MusicData(MediaData):
    lyric: str
    music: str
    download: bool
    comment_count: int


@dataclass(frozen=True, slots=True)
class MusicDetailData(MediaDetailData):
    lyric: str
    music: str
    download: bool
    comments: list[CommentData]


@dataclass(frozen=True, slots=True)
class ComicData(MediaData):
    image: str
    comment_count: int


@dataclass(frozen=True, slots=True)
class ComicDetailData(MediaDetailData):
    image: str
    comments: list[CommentData]


@dataclass(frozen=True, slots=True)
class PictureData(MediaData):
    image: str
    comment_count: int


@dataclass(frozen=True, slots=True)
class PictureDetailData(MediaDetailData):
    image: str
    comments: list[CommentData]


@dataclass(frozen=True, slots=True)
class BlogData(MediaData):
    image: str
    comment_count: int


@dataclass(frozen=True, slots=True)
class BlogDetailData(MediaDetailData):
    richtext: str
    image: str
    comments: list[CommentData]


@dataclass(frozen=True, slots=True)
class ChatData(MediaData):
    thread: int
    joined: int
    period: datetime


@dataclass(frozen=True, slots=True)
class ChatDetailData(MediaDetailData):
    thread: int
    joined: int
    period: datetime
    messages: list[MessageData]


@dataclass(frozen=True, slots=True)
class HomeData():
    videos: list[VideoData]
    musics: list[MusicData]
    comics: list[ComicData]
    pictures: list[PictureData]
    blogs: list[BlogData]
    chats: list[ChatData]
