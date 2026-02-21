from typing import assert_never
from api.src.domain.interface.media.blog.interface import BlogInterface
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.domain.interface.media.comic.interface import ComicInterface
from api.src.domain.interface.media.music.interface import MusicInterface
from api.src.domain.interface.media.picture.interface import PictureInterface
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.injectors.container import injector
from api.utils.enum.index import MediaType


type MediaInterfaceType = VideoInterface | MusicInterface | ComicInterface | PictureInterface | BlogInterface | ChatInterface


def get_media_repository(media_type: MediaType) -> MediaInterfaceType:
    match media_type:
        case MediaType.VIDEO:
            return injector.get(VideoInterface)
        case MediaType.MUSIC:
            return injector.get(MusicInterface)
        case MediaType.COMIC:
            return injector.get(ComicInterface)
        case MediaType.PICTURE:
            return injector.get(PictureInterface)
        case MediaType.BLOG:
            return injector.get(BlogInterface)
        case MediaType.CHAT:
            return injector.get(ChatInterface)
        case _:
            assert_never(media_type)
