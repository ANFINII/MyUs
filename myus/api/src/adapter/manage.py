from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.adapter.media import convert_comics, convert_musics, convert_videos
from api.src.types.schema.common import ErrorOut
from api.src.types.schema.media.input import BulkDeleteIn, ComicUpdateIn, MusicUpdateIn, VideoUpdateIn
from api.src.types.schema.media.output import ComicOut, MusicOut, VideoOut
from api.src.usecase.auth import auth_check
from api.src.usecase.manage.media import delete_manage_comic, delete_manage_music, delete_manage_video, get_manage_comic, get_manage_comics, get_manage_music, get_manage_musics, get_manage_video, get_manage_videos, update_manage_comic, update_manage_music, update_manage_video


class ManageVideoAPI:
    """ManageVideoAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: list[VideoOut], 401: ErrorOut})
    def list(request: HttpRequest, search: str = ""):
        log.info("ManageVideoAPI list", search=search)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        objs = get_manage_videos(user_id, search)
        return 200, convert_videos(objs)

    @staticmethod
    @router.get("/{ulid}", response={200: VideoOut, 401: ErrorOut, 404: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageVideoAPI get", ulid=ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        obj = get_manage_video(user_id, ulid)
        if obj is None:
            return 404, ErrorOut(message="Video not found")

        return 200, convert_videos([obj])[0]

    @staticmethod
    @router.put("/{ulid}", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: VideoUpdateIn):
        log.info("ManageVideoAPI put", ulid=ulid, input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not update_manage_video(user_id, ulid, input):
            return 400, ErrorOut(message="保存に失敗しました!")

        return 204, ErrorOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageVideoAPI delete", ulids=input.ulids)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not delete_manage_video(user_id, input.ulids):
            return 400, ErrorOut(message="削除に失敗しました!")

        return 204, ErrorOut(message="削除しました!")


class ManageMusicAPI:
    """ManageMusicAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: list[MusicOut], 401: ErrorOut})
    def list(request: HttpRequest, search: str = ""):
        log.info("ManageMusicAPI list", search=search)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        objs = get_manage_musics(user_id, search)
        return 200, convert_musics(objs)

    @staticmethod
    @router.get("/{ulid}", response={200: MusicOut, 401: ErrorOut, 404: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageMusicAPI get", ulid=ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        obj = get_manage_music(user_id, ulid)
        if obj is None:
            return 404, ErrorOut(message="Music not found")

        return 200, convert_musics([obj])[0]

    @staticmethod
    @router.put("/{ulid}", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: MusicUpdateIn):
        log.info("ManageMusicAPI put", ulid=ulid, input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not update_manage_music(user_id, ulid, input):
            return 400, ErrorOut(message="保存に失敗しました!")

        return 204, ErrorOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageMusicAPI delete", ulids=input.ulids)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not delete_manage_music(user_id, input.ulids):
            return 400, ErrorOut(message="削除に失敗しました!")

        return 204, ErrorOut(message="削除しました!")


class ManageComicAPI:
    """ManageComicAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: list[ComicOut], 401: ErrorOut})
    def list(request: HttpRequest, search: str = ""):
        log.info("ManageComicAPI list", search=search)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        objs = get_manage_comics(user_id, search)
        return 200, convert_comics(objs)

    @staticmethod
    @router.get("/{ulid}", response={200: ComicOut, 401: ErrorOut, 404: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("ManageComicAPI get", ulid=ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        obj = get_manage_comic(user_id, ulid)
        if obj is None:
            return 404, ErrorOut(message="Comic not found")

        return 200, convert_comics([obj])[0]

    @staticmethod
    @router.put("/{ulid}", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: ComicUpdateIn):
        log.info("ManageComicAPI put", ulid=ulid, input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not update_manage_comic(user_id, ulid, input):
            return 400, ErrorOut(message="保存に失敗しました!")

        return 204, ErrorOut(message="保存しました!")

    @staticmethod
    @router.delete("", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def delete(request: HttpRequest, input: BulkDeleteIn):
        log.info("ManageComicAPI delete", ulids=input.ulids)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not delete_manage_comic(user_id, input.ulids):
            return 400, ErrorOut(message="削除に失敗しました!")

        return 204, ErrorOut(message="削除しました!")
