from typing import assert_never
from django.core.files.storage import default_storage
from ninja import UploadedFile
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.domain.interface.media.music.interface import MusicInterface
from api.src.domain.interface.media.blog.interface import BlogInterface
from api.src.domain.interface.media.comic.interface import ComicInterface
from api.src.domain.interface.media.picture.interface import PictureInterface
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.injectors.container import injector
from api.utils.enum.index import MediaType, ImageUpload, MediaUpload
from api.utils.functions.convert.audio_converter import is_conversion, save_converted_mp3
from api.utils.functions.file import advertise_image_path, advertise_video_path, avatar_path, comic_path, image_path, musics_path, video_path


type MediaInterfaceType = VideoInterface | MusicInterface | BlogInterface | ComicInterface | PictureInterface | ChatInterface
type UploadType = ImageUpload | MediaUpload


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
        case ImageUpload.USER | ImageUpload.CHANNEL:
            path = avatar_path(upload_type, ulid, filename)
        case ImageUpload.VIDEO | ImageUpload.BLOG | ImageUpload.COMIC | ImageUpload.PICTURE:
            path = image_path(upload_type, ulid, filename)
        case ImageUpload.COMIC_PAGE:
            path = comic_path(ulid, filename)
        case ImageUpload.ADVERTISE:
            path = advertise_image_path(ulid, filename)
        case MediaUpload.VIDEO:
            path = video_path(upload_type, ulid, filename)
        case MediaUpload.ADVERTISE:
            path = advertise_video_path(ulid, filename)
        case MediaUpload.MUSIC:
            path = musics_path(ulid, filename)
            if is_conversion(filename):
                return save_converted_mp3(file, path)
        case _:
            assert False, f"未対応のUploadType: {upload_type}"
    return default_storage.save(path, file)
