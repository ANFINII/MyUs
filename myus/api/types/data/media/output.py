from dataclasses import dataclass
from api.types.data.media.index import VideoData, VideoDetailData
from api.types.data.media.index import MusicData, MusicDetailData
from api.types.data.media.index import ComicData, ComicDetailData
from api.types.data.media.index import PictureData, PictureDetailData
from api.types.data.media.index import BlogData, BlogDetailData
from api.types.data.media.index import ChatData, ChatDetailData


@dataclass(frozen=True, slots=True)
class VideoDetailOutData():
    detail: VideoDetailData
    list: list[VideoData]


@dataclass(frozen=True, slots=True)
class MusicDetailOutData():
    detail: MusicDetailData
    list: list[MusicData]


@dataclass(frozen=True, slots=True)
class ComicDetailOutData():
    detail: ComicDetailData
    list: list[ComicData]


@dataclass(frozen=True, slots=True)
class PictureDetailOutData():
    detail: PictureDetailData
    list: list[PictureData]


@dataclass(frozen=True, slots=True)
class BlogDetailOutData():
    detail: BlogDetailData
    list: list[BlogData]


@dataclass(frozen=True, slots=True)
class ChatDetailOutData():
    detail: ChatDetailData
    list: list[ChatData]
