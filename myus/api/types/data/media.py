from datetime import datetime
from dataclasses import dataclass
from api.types.data.comment import CommentData
from api.types.dto.user import AuthorData


@dataclass(frozen=True, slots=True)
class HashtagData:
    jp_name: str


@dataclass(frozen=True, slots=True)
class MediaData:
    id: int
    title: str
    content: str
    like: int
    read: int
    publish: bool
    created: datetime
    updated: datetime
    author: AuthorData


@dataclass(frozen=True, slots=True)
class MediaDetailData:
    id: int
    title: str
    content: str
    like: int
    read: int
    publish: bool
    created: datetime
    updated: datetime
    author: AuthorData
    comment_count: int
    comments: list[CommentData]
    hashtags: list[HashtagData]


@dataclass(frozen=True, slots=True)
class VideoData(MediaData):
    image: str
    video: str
    convert: str


@dataclass(frozen=True, slots=True)
class VideoDetailData(MediaDetailData):
    image: str
    video: str
    convert: str

@dataclass(frozen=True, slots=True)
class MusicData(MediaData):
    lyric: str
    music: str
    download: bool


@dataclass(frozen=True, slots=True)
class MusicDetailData(MediaDetailData):
    lyric: str
    music: str
    download: bool


@dataclass(frozen=True, slots=True)
class ComicsData(MediaData):
    image: str


@dataclass(frozen=True, slots=True)
class ComicsDetailData(MediaDetailData):
    image: str


@dataclass(frozen=True, slots=True)
class PictureData(MediaData):
    image: str


@dataclass(frozen=True, slots=True)
class PictureDetailData(MediaDetailData):
    image: str


@dataclass(frozen=True, slots=True)
class BlogData(MediaData):
    image: str

@dataclass(frozen=True, slots=True)
class BlogDetailData(MediaDetailData):
    image: str
    richtext: str


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
