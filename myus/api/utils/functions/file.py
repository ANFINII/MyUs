from typing import Any
from api.utils.enum.index import ImageType, VideoType
from api.utils.functions.index import new_ulid


def avatar_path(type: ImageType, ulid: str, filename: str) -> str:
    return f"images/{type}/{ulid}/{new_ulid()}_{filename}"


def image_path(type: ImageType, ulid: str, filename: str) -> str:
    return f"images/{type}/channel_{ulid}/{new_ulid()}_{filename}"


def video_path(type: VideoType, ulid: str, filename: str) -> str:
    return f"videos/{type}/channel_{ulid}/{new_ulid()}_{filename}"


def musics_path(ulid: str, filename: str) -> str:
    return f"musics/channel_{ulid}/{new_ulid()}_{filename}"


def comic_path(ulid: str, filename: str) -> str:
    return f"comics/channel_{ulid}/{new_ulid()}_{filename}"


def avatar_upload(obj: Any, filename: str) -> str:
    type_map: dict[str, ImageType] = {
        "User": ImageType.USER,
        "MyPage": ImageType.USER,
        "Channel": ImageType.CHANNEL,
    }
    image_type = type_map[type(obj).__name__]
    ulid = str(obj.ulid) if hasattr(obj, "ulid") else str(obj.user.ulid)
    return avatar_path(image_type, ulid, filename)


def image_upload(obj: Any, filename: str) -> str:
    type_map: dict[str, ImageType] = {
        "Video": ImageType.VIDEO,
        "Comic": ImageType.COMIC,
        "Picture": ImageType.PICTURE,
        "Blog": ImageType.BLOG,
    }
    image_type = type_map[type(obj).__name__]
    return image_path(image_type, str(obj.channel.ulid), filename)


def video_upload(obj: Any, filename: str) -> str:
    return video_path(VideoType.VIDEO, str(obj.channel.ulid), filename)


def music_upload(obj: Any, filename: str) -> str:
    return musics_path(str(obj.channel.ulid), filename)


def comic_upload(obj: Any, filename: str) -> str:
    return comic_path(str(obj.channel.ulid), filename)
