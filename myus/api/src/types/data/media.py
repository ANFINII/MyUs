from dataclasses import dataclass
from datetime import date, datetime
from api.src.domain.interface.media.data import HashtagData
from api.src.types.data.comment import CommentGetData
from api.src.types.data.message import MessageData
from api.src.domain.interface.channel.data import ChannelData
from api.src.types.data.user import MediaUserData


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
    channel: ChannelData
    mediaUser: MediaUserData
    hashtags: list[HashtagData]


@dataclass(frozen=True, slots=True)
class VideoDetailData(MediaDetailData):
    image: str
    video: str
    convert: str
    comments: list[CommentGetData]


@dataclass(frozen=True, slots=True)
class MusicDetailData(MediaDetailData):
    lyric: str
    music: str
    download: bool
    comments: list[CommentGetData]


@dataclass(frozen=True, slots=True)
class ComicDetailData(MediaDetailData):
    image: str
    comments: list[CommentGetData]


@dataclass(frozen=True, slots=True)
class PictureDetailData(MediaDetailData):
    image: str
    comments: list[CommentGetData]


@dataclass(frozen=True, slots=True)
class BlogDetailData(MediaDetailData):
    richtext: str
    image: str
    comments: list[CommentGetData]


@dataclass(frozen=True, slots=True)
class ChatDetailData(MediaDetailData):
    thread: int
    joined: int
    period: date
    messages: list[MessageData]
