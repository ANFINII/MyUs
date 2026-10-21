from typing import assert_never
from django.http import HttpRequest
from ninja import File, Form, Router, UploadedFile
from api.modules.logger import log
from api.src.adapter._auth import auth_check
from api.src.adapter.advertise import convert_advertises
from api.src.adapter.media import convert_videos, convert_musics, convert_blogs, convert_comics, convert_pictures, convert_chats
from api.src.types.schema.advertise import AdvertiseIn, AdvertiseListOut, AdvertiseOut, AdvertiseUpdateIn
from api.src.types.schema.common import ErrorOut, ErrorType, Limit, Offset, SuccessOut
from api.src.types.schema.media.input import BulkDeleteIn, VideoUpdateIn, MusicUpdateIn, BlogUpdateIn, ComicUpdateIn, PictureUpdateIn, ChatUpdateIn
from api.src.types.schema.media.output import MediaCreateOut, VideoOut, MusicOut, BlogOut, ComicOut, PictureOut, ChatOut
from api.src.types.schema.media.output import VideoListOut, MusicListOut, BlogListOut, ComicListOut, PictureListOut, ChatListOut
from api.src.domain.interface.media.index import PAGE_SIZE
from api.src.usecase.manage.advertise import get_manage_advertises, get_manage_advertise, create_manage_advertise, update_manage_advertise, delete_manage_advertise
from api.src.usecase.manage.media import (
    get_manage_videos, get_manage_video, update_manage_video, delete_manage_video,
    get_manage_musics, get_manage_music, update_manage_music, delete_manage_music,
    get_manage_blogs, get_manage_blog, update_manage_blog, delete_manage_blog,
    get_manage_comics, get_manage_comic, update_manage_comic, delete_manage_comic,
    get_manage_pictures, get_manage_picture, update_manage_picture, delete_manage_picture,
    get_manage_chats, get_manage_chat, update_manage_chat, delete_manage_chat,
)
from api.utils.common.result import FatalError, ForbiddenError, NotFoundError, ValidationError


class ManageVideoAPI:
    """ManageVideoAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: VideoListOut, 400: ErrorOut, 500: ErrorOut})
    def list(request: HttpRequest, search: str = "", channel: str = "", limit: Limit = PAGE_SIZE, offset: Offset = 0):
        log.info("ManageVideoAPI list", search=search, channel=channel, limit=limit, offset=offset)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        videos_ret = get_manage_videos(user_id, search, channel, limit, offset)
        if videos_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, total = videos_ret.ok_value
        return 200, VideoListOut(items=convert_videos(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: VideoOut, 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageVideoAPI get", ulid=ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        video_ret = get_manage_video(user_id, ulid)
        if video_ret.is_err:
            message = video_ret.err_value.message
            match video_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(video_ret.err_value)

        video = video_ret.ok_value
        return 200, convert_videos([video])[0]

    @staticmethod
    @router.put("/{ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: VideoUpdateIn = Form(...), image: UploadedFile | None = File(None)):
        log.info("ManageVideoAPI put", ulid=ulid, input=input, image=image)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        update_ret = update_manage_video(user_id, ulid, input, image)
        if update_ret.is_err:
            message = update_ret.err_value.message
            match update_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(update_ret.err_value)

        return 200, SuccessOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageVideoAPI delete", ulids=input.ulids)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        delete_ret = delete_manage_video(user_id, input.ulids)
        if delete_ret.is_err:
            message = delete_ret.err_value.message
            match delete_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(delete_ret.err_value)

        return 200, SuccessOut(message="削除しました!")


class ManageMusicAPI:
    """ManageMusicAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: MusicListOut, 400: ErrorOut, 500: ErrorOut})
    def list(request: HttpRequest, search: str = "", channel: str = "", limit: Limit = PAGE_SIZE, offset: Offset = 0):
        log.info("ManageMusicAPI list", search=search, channel=channel, limit=limit, offset=offset)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        musics_ret = get_manage_musics(user_id, search, channel, limit, offset)
        if musics_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, total = musics_ret.ok_value
        return 200, MusicListOut(items=convert_musics(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: MusicOut, 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageMusicAPI get", ulid=ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        music_ret = get_manage_music(user_id, ulid)
        if music_ret.is_err:
            message = music_ret.err_value.message
            match music_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(music_ret.err_value)

        music = music_ret.ok_value
        return 200, convert_musics([music])[0]

    @staticmethod
    @router.put("/{ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: MusicUpdateIn):
        log.info("ManageMusicAPI put", ulid=ulid, input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        update_ret = update_manage_music(user_id, ulid, input)
        if update_ret.is_err:
            message = update_ret.err_value.message
            match update_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(update_ret.err_value)

        return 200, SuccessOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageMusicAPI delete", ulids=input.ulids)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        delete_ret = delete_manage_music(user_id, input.ulids)
        if delete_ret.is_err:
            message = delete_ret.err_value.message
            match delete_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(delete_ret.err_value)

        return 200, SuccessOut(message="削除しました!")


class ManageBlogAPI:
    """ManageBlogAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: BlogListOut, 400: ErrorOut, 500: ErrorOut})
    def list(request: HttpRequest, search: str = "", channel: str = "", limit: Limit = PAGE_SIZE, offset: Offset = 0):
        log.info("ManageBlogAPI list", search=search, channel=channel, limit=limit, offset=offset)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        blogs_ret = get_manage_blogs(user_id, search, channel, limit, offset)
        if blogs_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, total = blogs_ret.ok_value
        return 200, BlogListOut(items=convert_blogs(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: BlogOut, 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageBlogAPI get", ulid=ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        blog_ret = get_manage_blog(user_id, ulid)
        if blog_ret.is_err:
            message = blog_ret.err_value.message
            match blog_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(blog_ret.err_value)

        blog = blog_ret.ok_value
        return 200, convert_blogs([blog])[0]

    @staticmethod
    @router.put("/{ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: BlogUpdateIn = Form(...), image: UploadedFile | None = File(None)):
        log.info("ManageBlogAPI put", ulid=ulid, input=input, image=image)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        update_ret = update_manage_blog(user_id, ulid, input, image)
        if update_ret.is_err:
            message = update_ret.err_value.message
            match update_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(update_ret.err_value)

        return 200, SuccessOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageBlogAPI delete", ulids=input.ulids)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        delete_ret = delete_manage_blog(user_id, input.ulids)
        if delete_ret.is_err:
            message = delete_ret.err_value.message
            match delete_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(delete_ret.err_value)

        return 200, SuccessOut(message="削除しました!")


class ManageComicAPI:
    """ManageComicAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: ComicListOut, 400: ErrorOut, 500: ErrorOut})
    def list(request: HttpRequest, search: str = "", channel: str = "", limit: Limit = PAGE_SIZE, offset: Offset = 0):
        log.info("ManageComicAPI list", search=search, channel=channel, limit=limit, offset=offset)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        comics_ret = get_manage_comics(user_id, search, channel, limit, offset)
        if comics_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, total = comics_ret.ok_value
        return 200, ComicListOut(items=convert_comics(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: ComicOut, 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageComicAPI get", ulid=ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        comic_ret = get_manage_comic(user_id, ulid)
        if comic_ret.is_err:
            message = comic_ret.err_value.message
            match comic_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(comic_ret.err_value)

        comic = comic_ret.ok_value
        return 200, convert_comics([comic])[0]

    @staticmethod
    @router.put("/{ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: ComicUpdateIn = Form(...), image: UploadedFile | None = File(None)):
        log.info("ManageComicAPI put", ulid=ulid, input=input, image=image)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        update_ret = update_manage_comic(user_id, ulid, input, image)
        if update_ret.is_err:
            message = update_ret.err_value.message
            match update_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(update_ret.err_value)

        return 200, SuccessOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageComicAPI delete", ulids=input.ulids)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        delete_ret = delete_manage_comic(user_id, input.ulids)
        if delete_ret.is_err:
            message = delete_ret.err_value.message
            match delete_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(delete_ret.err_value)

        return 200, SuccessOut(message="削除しました!")


class ManagePictureAPI:
    """ManagePictureAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: PictureListOut, 400: ErrorOut, 500: ErrorOut})
    def list(request: HttpRequest, search: str = "", channel: str = "", limit: Limit = PAGE_SIZE, offset: Offset = 0):
        log.info("ManagePictureAPI list", search=search, channel=channel, limit=limit, offset=offset)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        pictures_ret = get_manage_pictures(user_id, search, channel, limit, offset)
        if pictures_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, total = pictures_ret.ok_value
        return 200, PictureListOut(items=convert_pictures(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: PictureOut, 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManagePictureAPI get", ulid=ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        picture_ret = get_manage_picture(user_id, ulid)
        if picture_ret.is_err:
            message = picture_ret.err_value.message
            match picture_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(picture_ret.err_value)

        picture = picture_ret.ok_value
        return 200, convert_pictures([picture])[0]

    @staticmethod
    @router.put("/{ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: PictureUpdateIn = Form(...), image: UploadedFile | None = File(None)):
        log.info("ManagePictureAPI put", ulid=ulid, input=input, image=image)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        update_ret = update_manage_picture(user_id, ulid, input, image)
        if update_ret.is_err:
            message = update_ret.err_value.message
            match update_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(update_ret.err_value)

        return 200, SuccessOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManagePictureAPI delete", ulids=input.ulids)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        delete_ret = delete_manage_picture(user_id, input.ulids)
        if delete_ret.is_err:
            message = delete_ret.err_value.message
            match delete_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(delete_ret.err_value)

        return 200, SuccessOut(message="削除しました!")


class ManageChatAPI:
    """ManageChatAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: ChatListOut, 400: ErrorOut, 500: ErrorOut})
    def list(request: HttpRequest, search: str = "", channel: str = "", limit: Limit = PAGE_SIZE, offset: Offset = 0):
        log.info("ManageChatAPI list", search=search, channel=channel, limit=limit, offset=offset)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        chats_ret = get_manage_chats(user_id, search, channel, limit, offset)
        if chats_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, total = chats_ret.ok_value
        return 200, ChatListOut(items=convert_chats(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: ChatOut, 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageChatAPI get", ulid=ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        chat_ret = get_manage_chat(user_id, ulid)
        if chat_ret.is_err:
            message = chat_ret.err_value.message
            match chat_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(chat_ret.err_value)

        chat = chat_ret.ok_value
        return 200, convert_chats([chat])[0]

    @staticmethod
    @router.put("/{ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: ChatUpdateIn):
        log.info("ManageChatAPI put", ulid=ulid, input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        update_ret = update_manage_chat(user_id, ulid, input)
        if update_ret.is_err:
            message = update_ret.err_value.message
            match update_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(update_ret.err_value)

        return 200, SuccessOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageChatAPI delete", ulids=input.ulids)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        delete_ret = delete_manage_chat(user_id, input.ulids)
        if delete_ret.is_err:
            message = delete_ret.err_value.message
            match delete_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(delete_ret.err_value)

        return 200, SuccessOut(message="削除しました!")


class ManageAdvertiseAPI:
    """ManageAdvertiseAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: AdvertiseListOut, 400: ErrorOut, 500: ErrorOut})
    def list(request: HttpRequest, search: str = "", limit: Limit = PAGE_SIZE, offset: Offset = 0):
        log.info("ManageAdvertiseAPI list", search=search, limit=limit, offset=offset)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        advertises_ret = get_manage_advertises(user_id, search, limit, offset)
        if advertises_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs, total = advertises_ret.ok_value
        return 200, AdvertiseListOut(items=convert_advertises(objs), total=total)

    @staticmethod
    @router.get("/{ulid}", response={200: AdvertiseOut, 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageAdvertiseAPI get", ulid=ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        advertise_ret = get_manage_advertise(user_id, ulid)
        if advertise_ret.is_err:
            message = advertise_ret.err_value.message
            match advertise_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(advertise_ret.err_value)

        advertise = advertise_ret.ok_value
        return 200, convert_advertises([advertise])[0]

    @staticmethod
    @router.post("", response={200: MediaCreateOut, 400: ErrorOut, 500: ErrorOut})
    def post(request: HttpRequest, input: AdvertiseIn = Form(...), image: UploadedFile = File(...), video: UploadedFile | None = File(None)):
        log.info("ManageAdvertiseAPI post", input=input, image=image, video=video)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        create_ret = create_manage_advertise(user_id, input, image, video)
        if create_ret.is_err:
            message = create_ret.err_value.message
            match create_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(create_ret.err_value)

        advertise = create_ret.ok_value
        return 200, MediaCreateOut(ulid=advertise.ulid)

    @staticmethod
    @router.put("/{ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: AdvertiseUpdateIn = Form(...), image: UploadedFile | None = File(None), video: UploadedFile | None = File(None)):
        log.info("ManageAdvertiseAPI put", ulid=ulid, input=input, image=image, video=video)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        update_ret = update_manage_advertise(user_id, ulid, input, image, video)
        if update_ret.is_err:
            message = update_ret.err_value.message
            match update_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(update_ret.err_value)

        return 200, SuccessOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageAdvertiseAPI delete", ulids=input.ulids)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        delete_ret = delete_manage_advertise(user_id, input.ulids)
        if delete_ret.is_err:
            message = delete_ret.err_value.message
            match delete_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(delete_ret.err_value)

        return 200, SuccessOut(message="削除しました!")
