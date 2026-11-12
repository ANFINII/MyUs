from dataclasses import dataclass
from datetime import date, datetime
from myus.domain.interface.hashtag.data import HashtagData
from myus.domain.interface.media.video.data import VideoData
from myus.domain.interface.media.music.data import MusicData
from myus.domain.interface.media.blog.data import BlogData
from myus.domain.interface.media.comic.data import ComicData
from myus.domain.interface.media.picture.data import PictureData
from myus.domain.interface.media.chat.data import ChatData
from myus.types.dto.comment import CommentDTO
from myus.types.dto.message import MessageDTO
from myus.domain.interface.channel.data import ChannelData
from myus.types.dto.user import MediaUserDTO


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
