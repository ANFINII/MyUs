from dataclasses import dataclass
from datetime import date, datetime
from api.src.domain.interface.media.data import HashtagData
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.music.data import MusicData
from api.src.domain.interface.media.comic.data import ComicData
from api.src.domain.interface.media.picture.data import PictureData
from api.src.domain.interface.media.blog.data import BlogData
from api.src.domain.interface.media.chat.data import ChatData
from api.src.types.dto.comment import CommentDTO
from api.src.types.dto.message import MessageDTO
from api.src.domain.interface.channel.data import ChannelData
from api.src.types.dto.user import MediaUserDTO


@dataclass(frozen=True, slots=True)
class HomeDTO:
    videos: list[VideoData]
    musics: list[MusicData]
    comics: list[ComicData]
    pictures: list[PictureData]
    blogs: list[BlogData]
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
class ComicDetailDTO(MediaDetailDTO):
    image: str
    pages: list[str]
    comments: list[CommentDTO]


@dataclass(frozen=True, slots=True)
class PictureDetailDTO(MediaDetailDTO):
    image: str
    comments: list[CommentDTO]


@dataclass(frozen=True, slots=True)
class BlogDetailDTO(MediaDetailDTO):
    richtext: str
    image: str
    comments: list[CommentDTO]


@dataclass(frozen=True, slots=True)
class ChatDetailDTO(MediaDetailDTO):
    thread: int
    joined: int
    period: date
    messages: list[MessageDTO]
