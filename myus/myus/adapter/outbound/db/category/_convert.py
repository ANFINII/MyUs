from typing import assert_never
from myus.db.models.master import Category
from myus.db.models.media import Audio, Blog, Chat, Comic, Picture, Video
from myus.domain.category.data import CategoryData
from myus.utils.enum.media import MediaType


def convert_data(obj: Category) -> CategoryData:
    return CategoryData(
        id=obj.id,
        ulid=obj.ulid,
        jp_name=obj.jp_name,
        en_name=obj.en_name,
    )


def get_media_model(media_type: MediaType) -> type[Video] | type[Audio] | type[Blog] | type[Comic] | type[Picture] | type[Chat]:
    match media_type:
        case MediaType.VIDEO:
            return Video
        case MediaType.AUDIO:
            return Audio
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
