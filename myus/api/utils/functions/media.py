from typing import Type, assert_never
from api.db.models import Video, Music, Comic, Picture, Blog, Chat
from api.src.domain.media.blog import BlogDomain
from api.src.domain.media.chat import ChatDomain
from api.src.domain.media.comic import ComicDomain
from api.src.domain.media.music import MusicDomain
from api.src.domain.media.picture import PictureDomain
from api.src.domain.media.video import VideoDomain
from api.utils.enum.index import MediaType


type MediaModel = Video | Music | Comic | Picture | Blog | Chat
type MediaDomainType = Type[VideoDomain] | Type[MusicDomain] | Type[ComicDomain] | Type[PictureDomain] | Type[BlogDomain] | Type[ChatDomain]

DOMAIN_MAP: dict[type[MediaModel], MediaDomainType] = {
    Video: VideoDomain,
    Music: MusicDomain,
    Comic: ComicDomain,
    Picture: PictureDomain,
    Blog: BlogDomain,
    Chat: ChatDomain,
}


def get_media_domain(model: type[MediaModel]) -> MediaDomainType:
    domain = DOMAIN_MAP.get(model)
    if domain is None:
        raise ValueError(f"Unknown media model: {model}")
    return domain


def get_media_domain_type(media_type: MediaType) -> MediaDomainType:
    match media_type:
        case MediaType.VIDEO:
            return VideoDomain
        case MediaType.MUSIC:
            return MusicDomain
        case MediaType.COMIC:
            return ComicDomain
        case MediaType.PICTURE:
            return PictureDomain
        case MediaType.BLOG:
            return BlogDomain
        case MediaType.CHAT:
            return ChatDomain
        case _:
            assert_never(media_type)
