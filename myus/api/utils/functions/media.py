from typing import assert_never
from api.db.models import Video, Music, Comic, Picture, Blog, Chat
from api.src.domain.entity.media.blog.repository import BlogRepository
from api.src.domain.entity.media.chat.repository import ChatRepository
from api.src.domain.entity.media.comic.repository import ComicRepository
from api.src.domain.entity.media.music.repository import MusicRepository
from api.src.domain.entity.media.picture.repository import PictureRepository
from api.src.domain.entity.media.video.repository import VideoRepository
from api.src.domain.interface.media.blog.interface import BlogInterface
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.domain.interface.media.comic.interface import ComicInterface
from api.src.domain.interface.media.music.interface import MusicInterface
from api.src.domain.interface.media.picture.interface import PictureInterface
from api.src.domain.interface.media.video.interface import VideoInterface
from api.utils.enum.index import MediaType


type MediaModel = Video | Music | Comic | Picture | Blog | Chat
type MediaInterfaceType = VideoInterface | MusicInterface | ComicInterface | PictureInterface | BlogInterface | ChatInterface


def get_media_repository(media_type: MediaType) -> MediaInterfaceType:
    match media_type:
        case MediaType.VIDEO:
            return VideoRepository()
        case MediaType.MUSIC:
            return MusicRepository()
        case MediaType.COMIC:
            return ComicRepository()
        case MediaType.PICTURE:
            return PictureRepository()
        case MediaType.BLOG:
            return BlogRepository()
        case MediaType.CHAT:
            return ChatRepository()
        case _:
            assert_never(media_type)
