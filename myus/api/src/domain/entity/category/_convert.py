from typing import assert_never
from api.db.models.master import Category
from api.db.models.media import Blog, Chat, Comic, Music, Picture, Video
from api.src.domain.interface.category.data import CategoryData
from api.utils.enum.index import MediaType


def convert_data(obj: Category) -> CategoryData:
    return CategoryData(
        id=obj.id,
        ulid=obj.ulid,
        jp_name=obj.jp_name,
        en_name=obj.en_name,
    )


def get_media_model(media_type: MediaType) -> type[Video] | type[Music] | type[Blog] | type[Comic] | type[Picture] | type[Chat]:
    match media_type:
        case MediaType.VIDEO:
            return Video
        case MediaType.MUSIC:
            return Music
        case MediaType.BLOG:
            return Blog
        case MediaType.COMIC:
            return Comic
        case MediaType.PICTURE:
            return Picture
        case MediaType.CHAT:
            return Chat
        case _:
            assert_never(media_type)
