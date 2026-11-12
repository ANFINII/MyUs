from typing import assert_never
from django.db.models import Model
from django_ulid.models import ulid
from myus.db.models.hashtag import HashTag, VideoHashtag, MusicHashtag, BlogHashtag, ComicHashtag, PictureHashtag, ChatHashtag
from myus.domain.hashtag.data import HashtagData
from myus.utils.enum.media import MediaType


def convert_data(obj: HashTag) -> HashtagData:
    return HashtagData(
        id=obj.id,
        ulid=obj.ulid,
        name=obj.name,
    )


def marshal_data(data: HashtagData) -> HashTag:
    return HashTag(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid if data.ulid else ulid.new(),
        name=data.name,
    )


def marshal_through(media_type: MediaType, media_id: int, hashtag_id: int, sequence: int) -> Model:
    model_class, fk_name = get_through_model(media_type)
    return model_class(**{fk_name: media_id}, hashtag_id=hashtag_id, sequence=sequence)


def get_through_model(media_type: MediaType) -> tuple[type[Model], str]:
    match media_type:
        case MediaType.VIDEO:
            return (VideoHashtag, "video_id")
        case MediaType.MUSIC:
            return (MusicHashtag, "music_id")
        case MediaType.BLOG:
            return (BlogHashtag, "blog_id")
        case MediaType.COMIC:
            return (ComicHashtag, "comic_id")
        case MediaType.PICTURE:
            return (PictureHashtag, "picture_id")
        case MediaType.CHAT:
            return (ChatHashtag, "chat_id")
        case _:
            assert_never(media_type)
