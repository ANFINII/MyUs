from pathlib import Path
from typing import Any
from myus.utils.enum.upload import ImageUpload, MediaUpload
from myus.utils.functions.convert.audio_converter import CONVERTIBLE_EXTENSIONS
from myus.utils.functions.index import new_ulid


def file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def avatar_path(type: ImageUpload, ulid: str, extension: str) -> str:
    return f"images/{type.value}/{ulid}/{new_ulid()}{extension}"


def image_path(type: ImageUpload, ulid: str, extension: str) -> str:
    return f"images/{type.value}/channel_{ulid}/{new_ulid()}{extension}"


def video_path(type: MediaUpload, ulid: str, extension: str) -> str:
    return f"videos/{type.value}/channel_{ulid}/{new_ulid()}{extension}"


def musics_path(ulid: str, extension: str) -> str:
    if extension in CONVERTIBLE_EXTENSIONS:
        extension = ".mp3"
    return f"musics/channel_{ulid}/{new_ulid()}{extension}"


def comic_path(ulid: str, extension: str) -> str:
    return f"comics/channel_{ulid}/{new_ulid()}{extension}"


def advertise_image_path(ulid: str, extension: str) -> str:
    return f"images/advertise/user_{ulid}/{new_ulid()}{extension}"


def advertise_video_path(ulid: str, extension: str) -> str:
    return f"videos/advertise/user_{ulid}/{new_ulid()}{extension}"


def avatar_upload(obj: Any, filename: str) -> str:
    type_map: dict[str, ImageUpload] = {
        "User": ImageUpload.USER,
        "MyPage": ImageUpload.USER,
        "Channel": ImageUpload.CHANNEL,
    }
    upload_type = type_map[type(obj).__name__]
    ulid = str(obj.ulid) if hasattr(obj, "ulid") else str(obj.user.ulid)
    return avatar_path(upload_type, ulid, file_extension(filename))


def image_upload(obj: Any, filename: str) -> str:
    type_map: dict[str, ImageUpload] = {
        "Video": ImageUpload.VIDEO,
        "Blog": ImageUpload.BLOG,
        "Comic": ImageUpload.COMIC,
        "Picture": ImageUpload.PICTURE,
    }
    upload_type = type_map[type(obj).__name__]
    return image_path(upload_type, str(obj.channel.ulid), file_extension(filename))


def video_upload(obj: Any, filename: str) -> str:
    return video_path(MediaUpload.VIDEO, str(obj.channel.ulid), file_extension(filename))


def music_upload(obj: Any, filename: str) -> str:
    return musics_path(str(obj.channel.ulid), file_extension(filename))


def comic_upload(obj: Any, filename: str) -> str:
    return comic_path(str(obj.channel.ulid), file_extension(filename))


def advertise_image_upload(obj: Any, filename: str) -> str:
    return advertise_image_path(str(obj.author.ulid), file_extension(filename))


def advertise_video_upload(obj: Any, filename: str) -> str:
    return advertise_video_path(str(obj.author.ulid), file_extension(filename))
