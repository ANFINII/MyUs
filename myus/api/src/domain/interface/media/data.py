from dataclasses import dataclass
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.music.data import MusicData
from api.src.domain.interface.media.comic.data import ComicData
from api.src.domain.interface.media.picture.data import PictureData
from api.src.domain.interface.media.blog.data import BlogData
from api.src.domain.interface.media.chat.data import ChatData

@dataclass(frozen=True, slots=True)
class MediaCreateData:
    ulid: str


@dataclass(frozen=True, slots=True)
class HashtagData:
    jp_name: str


@dataclass(frozen=True, slots=True)
class HomeData:
    videos: list[VideoData]
    musics: list[MusicData]
    comics: list[ComicData]
    pictures: list[PictureData]
    blogs: list[BlogData]
    chats: list[ChatData]
