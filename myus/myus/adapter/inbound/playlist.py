from typing import assert_never
from ninja import Router
from django.http import HttpRequest
from myus.usecase.dto.playlist import PlaylistCreateDTO, PlaylistDetailDTO, PlaylistDTO, PlaylistUpdateDTO
from myus.usecase.playlist.core import add_playlist_music, create_playlist, delete_playlist, get_my_playlists, get_playlist, get_user_playlists, update_playlist
from myus.utils.common.logger import log
from myus.utils.common.result import FatalError, ForbiddenError, NotFoundError
from .auth import auth_check
from .media import convert_musics
from .schema.common import ErrorOut, ErrorType, SuccessOut
from .schema.playlist import PlaylistCreateOut, PlaylistDetailOut, PlaylistIn, PlaylistListOut, PlaylistMusicIn, PlaylistOut, PlaylistUpdateIn


class PlaylistAPI:
    """PlaylistAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: PlaylistListOut, 500: ErrorOut})
    def list(request: HttpRequest):
        log.info("request")

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 200, PlaylistListOut(items=[])

        ret = get_my_playlists(user_id)
        if ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        return 200, PlaylistListOut(items=convert_playlists(ret.ok_value))

    @staticmethod
    @router.post("", response={200: PlaylistCreateOut, 400: ErrorOut, 500: ErrorOut})
    def create(request: HttpRequest, input: PlaylistIn):
        log.info("request", input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        ret = create_playlist(user_id, PlaylistCreateDTO(**input.model_dump()))
        if ret.is_err:
            message = ret.err_value.message
            match ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(ret.err_value)

        return 200, PlaylistCreateOut(ulid=ret.ok_value)

    @staticmethod
    @router.get("/user/{user_ulid}", response={200: PlaylistListOut, 400: ErrorOut, 500: ErrorOut})
    def list_user(request: HttpRequest, user_ulid: str):
        log.info("request", user_ulid=user_ulid)

        ret = get_user_playlists(user_ulid)
        if ret.is_err:
            message = ret.err_value.message
            match ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(ret.err_value)

        return 200, PlaylistListOut(items=convert_playlists(ret.ok_value))

    @staticmethod
    @router.get("/{ulid}", response={200: PlaylistDetailOut, 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("request", ulid=ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        ret = get_playlist(user_id_ret.ok_value, ulid)
        if ret.is_err:
            message = ret.err_value.message
            match ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(ret.err_value)

        return 200, convert_playlist_detail(ret.ok_value)

    @staticmethod
    @router.put("/{ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def update(request: HttpRequest, ulid: str, input: PlaylistUpdateIn):
        log.info("request", ulid=ulid, input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        ret = update_playlist(user_id, ulid, PlaylistUpdateDTO(**input.model_dump()))
        if ret.is_err:
            message = ret.err_value.message
            match ret.err_value:
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(ret.err_value)

        return 200, SuccessOut(message="OK")

    @staticmethod
    @router.delete("/{ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def delete(request: HttpRequest, ulid: str):
        log.info("request", ulid=ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        ret = delete_playlist(user_id, ulid)
        if ret.is_err:
            message = ret.err_value.message
            match ret.err_value:
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(ret.err_value)

        return 200, SuccessOut(message="OK")

    @staticmethod
    @router.post("/{ulid}/music", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def add_music(request: HttpRequest, ulid: str, input: PlaylistMusicIn):
        log.info("request", ulid=ulid, input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        ret = add_playlist_music(user_id, ulid, input.music_ulid)
        if ret.is_err:
            message = ret.err_value.message
            match ret.err_value:
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(ret.err_value)

        return 200, SuccessOut(message="OK")


def convert_playlists(objs: list[PlaylistDTO]) -> list[PlaylistOut]:
    data = [
        PlaylistOut(
            ulid=x.ulid,
            title=x.title,
            publish=x.publish,
            count=x.count,
            image=x.image,
            updated=x.updated,
        ) for x in objs
    ]
    return data


def convert_playlist_detail(obj: PlaylistDetailDTO) -> PlaylistDetailOut:
    data = PlaylistDetailOut(
        ulid=obj.ulid,
        title=obj.title,
        publish=obj.publish,
        is_owner=obj.is_owner,
        author_ulid=obj.author_ulid,
        author_nickname=obj.author_nickname,
        musics=convert_musics(obj.musics),
        updated=obj.updated,
    )
    return data
