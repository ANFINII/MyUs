import os
from typing import assert_never
from django.core.files.storage import default_storage
from ninja import UploadedFile
from api.modules.logger import log
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.domain.interface.media.music.interface import MusicInterface
from api.src.domain.interface.media.blog.interface import BlogInterface
from api.src.domain.interface.media.comic.interface import ComicInterface
from api.src.domain.interface.media.picture.interface import PictureInterface
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.injectors.container import injector
from api.utils.common.result import Result, ValidationError
from api.utils.constants.upload import IMAGE_EXTENSIONS, IMAGE_MAX_SIZE, MUSIC_EXTENSIONS, MUSIC_MAX_SIZE, VIDEO_EXTENSIONS, VIDEO_MAX_SIZE, UploadRuleData
from api.utils.enum.media import MediaType
from api.utils.enum.upload import ImageUpload, MediaUpload
from api.utils.functions.convert.audio_converter import is_conversion, save_converted_mp3
from api.utils.functions.file import advertise_image_path, advertise_video_path, avatar_path, comic_path, image_path, musics_path, video_path


type MediaInterfaceType = VideoInterface | MusicInterface | BlogInterface | ComicInterface | PictureInterface | ChatInterface
type UploadType = ImageUpload | MediaUpload


def upload_rule(upload_type: UploadType) -> UploadRuleData:
    match upload_type:
        case ImageUpload():
            return UploadRuleData(extensions=IMAGE_EXTENSIONS, content_type_prefix="image/", max_size=IMAGE_MAX_SIZE)
        case MediaUpload.VIDEO | MediaUpload.ADVERTISE:
            return UploadRuleData(extensions=VIDEO_EXTENSIONS, content_type_prefix="video/", max_size=VIDEO_MAX_SIZE)
        case MediaUpload.MUSIC:
            return UploadRuleData(extensions=MUSIC_EXTENSIONS, content_type_prefix="audio/", max_size=MUSIC_MAX_SIZE)
        case _:
            assert_never(upload_type)


def validate_uploads(files: list[tuple[UploadedFile | None, UploadType]]) -> Result[None, ValidationError]:
    for file, upload_type in files:
        if file is None:
            continue

        rule = upload_rule(upload_type)
        extension = os.path.splitext(file.name or "")[1].lower()
        content_type = file.content_type or ""
        if extension not in rule.extensions or not content_type.startswith(rule.content_type_prefix):
            log.warning("Upload rejected: unsupported type", upload_type=upload_type.value, extension=extension, content_type=content_type)
            return Result.err(ValidationError("対応していないファイル形式です"))

        if file.size is None or file.size > rule.max_size:
            log.warning("Upload rejected: too large", upload_type=upload_type.value, size=file.size)
            return Result.err(ValidationError("ファイルサイズが大きすぎます"))

    return Result.ok(None)


def get_media_repository(media_type: MediaType) -> MediaInterfaceType:
    match media_type:
        case MediaType.VIDEO:
            return injector.get(VideoInterface)
        case MediaType.MUSIC:
            return injector.get(MusicInterface)
        case MediaType.BLOG:
            return injector.get(BlogInterface)
        case MediaType.COMIC:
            return injector.get(ComicInterface)
        case MediaType.PICTURE:
            return injector.get(PictureInterface)
        case MediaType.CHAT:
            return injector.get(ChatInterface)
        case _:
            assert_never(media_type)


def save_upload(file: UploadedFile, upload_type: UploadType, ulid: str) -> str:
    filename = file.name or "upload"
    match upload_type:
        case ImageUpload():
            path = image_upload_path(upload_type, ulid, filename)
        case MediaUpload.VIDEO:
            path = video_path(upload_type, ulid, filename)
        case MediaUpload.ADVERTISE:
            path = advertise_video_path(ulid, filename)
        case MediaUpload.MUSIC:
            path = musics_path(ulid, filename)
            if is_conversion(filename):
                return save_converted_mp3(file, path)
        case _:
            assert_never(upload_type)
    return default_storage.save(path, file)


def image_upload_path(upload_type: ImageUpload, ulid: str, filename: str) -> str:
    match upload_type:
        case ImageUpload.USER | ImageUpload.CHANNEL:
            return avatar_path(upload_type, ulid, filename)
        case ImageUpload.VIDEO | ImageUpload.BLOG | ImageUpload.COMIC | ImageUpload.PICTURE:
            return image_path(upload_type, ulid, filename)
        case ImageUpload.COMIC_PAGE:
            return comic_path(ulid, filename)
        case ImageUpload.ADVERTISE:
            return advertise_image_path(ulid, filename)
        case _:
            assert False, f"未対応のUploadType: {upload_type}"
