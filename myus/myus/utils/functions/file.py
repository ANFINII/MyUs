from pathlib import Path
from typing import Any
from django.core.files.storage import Storage, storages
from .common import new_ulid
from ..enum.upload import ImageUpload, MediaUpload


def file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def avatar_path(type: ImageUpload, ulid: str, extension: str) -> str:
    return f"images/{type.value}/{ulid}/{new_ulid()}{extension}"


def image_path(type: ImageUpload, ulid: str, extension: str) -> str:
    return f"images/{type.value}/channel_{ulid}/{new_ulid()}{extension}"


def video_path(type: MediaUpload, ulid: str, extension: str) -> str:
    return f"videos/{type.value}/channel_{ulid}/{new_ulid()}{extension}"


def audios_path(ulid: str) -> str:
    return f"audios/channel_{ulid}/{new_ulid()}.mp3"


def hires_path(ulid: str) -> str:
    return f"hires/channel_{ulid}/{new_ulid()}.flac"


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


def audio_upload(obj: Any, filename: str) -> str:
    return audios_path(str(obj.channel.ulid))


def hires_upload(obj: Any, filename: str) -> str:
    return hires_path(str(obj.audio.channel.ulid))


def comic_upload(obj: Any, filename: str) -> str:
    return comic_path(str(obj.channel.ulid), file_extension(filename))


def advertise_image_upload(obj: Any, filename: str) -> str:
    return advertise_image_path(str(obj.author.ulid), file_extension(filename))


def advertise_video_upload(obj: Any, filename: str) -> str:
    return advertise_video_path(str(obj.author.ulid), file_extension(filename))


def private_storage() -> Storage:
    return storages["private"]
