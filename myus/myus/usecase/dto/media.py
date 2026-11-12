from dataclasses import dataclass
from datetime import date, datetime
from myus.domain.channel.data import ChannelData
from myus.domain.hashtag.data import HashtagData
from myus.domain.media.blog.data import BlogData
from myus.domain.media.chat.data import ChatData
from myus.domain.media.comic.data import ComicData
from myus.domain.media.music.data import MusicData
from myus.domain.media.picture.data import PictureData
from myus.domain.media.video.data import VideoData
from .comment import CommentDTO
from .message import MessageDTO
from .user import MediaUserDTO


@dataclass(frozen=True, slots=True)
class HomeDTO:
    videos: list[VideoData]
    musics: list[MusicData]
    blogs: list[BlogData]
    comics: list[ComicData]
    pictures: list[PictureData]
    chats: list[ChatData]


@dataclass(frozen=True, slots=True)
class MediaCreateDTO:
    ulid: str


@dataclass(frozen=True, slots=True)
class MediaDetailDTO:
    id: int
    ulid: str
    title: str
    content: str
    read: int
    like: int
    publish: bool
    created: datetime
    updated: datetime
    channel: ChannelData
    mediaUser: MediaUserDTO
    hashtags: list[HashtagData]


@dataclass(frozen=True, slots=True)
class VideoDetailDTO(MediaDetailDTO):
    image: str
    video: str
    convert: str
    comments: list[CommentDTO]


@dataclass(frozen=True, slots=True)
class MusicDetailDTO(MediaDetailDTO):
    lyric: str
    music: str
    download: bool
    comments: list[CommentDTO]


@dataclass(frozen=True, slots=True)
class BlogDetailDTO(MediaDetailDTO):
    richtext: str
    is_promotion: bool
    image: str
    comments: list[CommentDTO]


@dataclass(frozen=True, slots=True)
class ComicDetailDTO(MediaDetailDTO):
    image: str
    pages: list[str]
    comments: list[CommentDTO]


@dataclass(frozen=True, slots=True)
class PictureDetailDTO(MediaDetailDTO):
    image: str
    comments: list[CommentDTO]


@dataclass(frozen=True, slots=True)
class ChatDetailDTO(MediaDetailDTO):
    thread: int
    joined: int
    period: date
    messages: list[MessageDTO]


@dataclass(frozen=True, slots=True)
class VideoCreateDTO:
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str


@dataclass(frozen=True, slots=True)
class MusicCreateDTO:
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str
    lyric: str
    download: bool


@dataclass(frozen=True, slots=True)
class BlogCreateDTO:
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str
    richtext: str
    is_promotion: bool


@dataclass(frozen=True, slots=True)
class ComicCreateDTO:
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str


@dataclass(frozen=True, slots=True)
class PictureCreateDTO:
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str


@dataclass(frozen=True, slots=True)
class ChatCreateDTO:
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str
    period: date


@dataclass(frozen=True, slots=True)
class VideoUpdateDTO:
    category_ulid: str
    title: str
    content: str
    publish: bool
    publish_at: datetime


@dataclass(frozen=True, slots=True)
class MusicUpdateDTO:
    category_ulid: str
    title: str
    content: str
    lyric: str
    download: bool
    publish: bool
    publish_at: datetime


@dataclass(frozen=True, slots=True)
class BlogUpdateDTO:
    category_ulid: str
    title: str
    content: str
    richtext: str
    is_promotion: bool
    publish: bool
    publish_at: datetime


@dataclass(frozen=True, slots=True)
class ComicUpdateDTO:
    category_ulid: str
    title: str
    content: str
    publish: bool
    publish_at: datetime


@dataclass(frozen=True, slots=True)
class PictureUpdateDTO:
    category_ulid: str
    title: str
    content: str
    publish: bool
    publish_at: datetime


@dataclass(frozen=True, slots=True)
class ChatUpdateDTO:
    category_ulid: str
    title: str
    content: str
    period: date
    publish: bool
    publish_at: datetime
