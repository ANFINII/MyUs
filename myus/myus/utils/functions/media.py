import json
import os
import shutil
import subprocess
import tempfile
from typing import assert_never
from PIL import Image, UnidentifiedImageError
from ninja import UploadedFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import TemporaryUploadedFile
from .convert.audio_converter import is_conversion, save_converted_mp3
from .file import advertise_image_path, advertise_video_path, avatar_path, comic_path, file_extension, image_path, musics_path, video_path
from ..common.logger import log
from ..common.result import Result, ValidationError
from ..constants.upload import IMAGE_EXTENSIONS, IMAGE_FORMATS, IMAGE_MAX_SIZE, MUSIC_EXTENSIONS, MUSIC_FORMATS, MUSIC_MAX_SIZE, VIDEO_EXTENSIONS, VIDEO_FORMATS, VIDEO_MAX_SIZE, UploadRuleData
from ..enum.upload import ImageUpload, MediaUpload


type UploadType = ImageUpload | MediaUpload

PROBE_TIMEOUT = 60


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
            return Result.err(ValidationError("error.fileTypeInvalid"))

        if file.size is None or file.size > rule.max_size:
            log.warning("Upload rejected: too large", upload_type=upload_type.value, size=file.size)
            return Result.err(ValidationError("error.fileTooLarge"))

        if isinstance(upload_type, ImageUpload) and not is_image(file):
            log.warning("Upload rejected: not an image", upload_type=upload_type.value, extension=extension, content_type=content_type)
            return Result.err(ValidationError("error.fileTypeInvalid"))

        if isinstance(upload_type, MediaUpload) and not is_media(file, upload_type):
            log.warning("Upload rejected: unsupported format", upload_type=upload_type.value, extension=extension, content_type=content_type)
            return Result.err(ValidationError("error.fileTypeInvalid"))

    return Result.ok(None)


def is_image(file: UploadedFile) -> bool:
    try:
        with Image.open(file) as image:
            image_format = image.format
            image.verify()
    except (UnidentifiedImageError, Image.DecompressionBombError, OSError, SyntaxError, ValueError):
        return False
    finally:
        file.seek(0)
    return image_format in IMAGE_FORMATS


def media_formats(upload_type: MediaUpload) -> set[str]:
    match upload_type:
        case MediaUpload.VIDEO | MediaUpload.ADVERTISE:
            return VIDEO_FORMATS
        case MediaUpload.MUSIC:
            return MUSIC_FORMATS
        case _:
            assert_never(upload_type)


def is_media(file: UploadedFile, upload_type: MediaUpload) -> bool:
    if isinstance(file, TemporaryUploadedFile):
        formats = probe_formats(file.temporary_file_path())
    else:
        with tempfile.NamedTemporaryFile() as tmp:
            for chunk in file.chunks():
                tmp.write(chunk)
            tmp.flush()
            formats = probe_formats(tmp.name)
    file.seek(0)
    return len(formats) > 0 and formats <= media_formats(upload_type)


def probe_formats(path: str) -> set[str]:
    ffprobe_path = shutil.which("ffprobe") or "ffprobe"
    cmd = [ffprobe_path, "-v", "error", "-protocol_whitelist", "file", "-show_entries", "format=format_name", "-of", "json", path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=PROBE_TIMEOUT)
    except (OSError, subprocess.TimeoutExpired) as e:
        log.error("ffprobe failed", exc=e, path=path)
        return set()

    if result.returncode != 0:
        log.warning("ffprobe rejected", path=path, stderr=result.stderr)
        return set()

    try:
        format_name: str = json.loads(result.stdout)["format"]["format_name"]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        log.warning("ffprobe output invalid", exc=e, path=path)
        return set()
    return set(format_name.split(","))


def save_upload(file: UploadedFile, upload_type: UploadType, ulid: str) -> str:
    filename = file.name or "upload"
    extension = file_extension(filename)
    match upload_type:
        case ImageUpload():
            path = image_upload_path(upload_type, ulid, extension)
        case MediaUpload.VIDEO:
            path = video_path(upload_type, ulid, extension)
        case MediaUpload.ADVERTISE:
            path = advertise_video_path(ulid, extension)
        case MediaUpload.MUSIC:
            path = musics_path(ulid, extension)
            if is_conversion(filename):
                return save_converted_mp3(file, path)
        case _:
            assert_never(upload_type)
    return default_storage.save(path, file)


def image_upload_path(upload_type: ImageUpload, ulid: str, extension: str) -> str:
    match upload_type:
        case ImageUpload.USER | ImageUpload.CHANNEL:
            return avatar_path(upload_type, ulid, extension)
        case ImageUpload.VIDEO | ImageUpload.BLOG | ImageUpload.COMIC | ImageUpload.PICTURE:
            return image_path(upload_type, ulid, extension)
        case ImageUpload.COMIC_PAGE:
            return comic_path(ulid, extension)
        case ImageUpload.ADVERTISE:
            return advertise_image_path(ulid, extension)
        case _:
            assert False, f"未対応のUploadType: {upload_type}"
