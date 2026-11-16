from typing import assert_never
from ninja import Router
from django.http import HttpRequest
from myus.usecase.dto.series import SeriesCreateDTO, SeriesDetailDTO, SeriesItemDTO, SeriesUpdateDTO
from myus.usecase.series.core import create_manage_series, get_channel_series, delete_manage_series, get_manage_series, get_manage_series_list, update_manage_series
from myus.utils.common.logger import log
from myus.utils.common.result import FatalError, ForbiddenError, NotFoundError
from .auth import auth_check
from .schema.common import ErrorOut, ErrorType, SuccessOut
from .schema.series import ChannelSeriesListOut, ChannelSeriesOut, SeriesCreateOut, SeriesDetailOut, SeriesIn, SeriesItemOut, SeriesListOut, SeriesOut, SeriesUpdateIn


class SeriesAPI:
    """SeriesAPI"""

    router = Router()

    @staticmethod
    @router.get("/channel/{channel_ulid}", response={200: ChannelSeriesListOut, 400: ErrorOut, 500: ErrorOut})
    def list_channel(request: HttpRequest, channel_ulid: str):
        log.info("request", channel_ulid=channel_ulid)

        ret = get_channel_series(channel_ulid)
        if ret.is_err:
            message = ret.err_value.message
            match ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(ret.err_value)

        objs = ret.ok_value
        return 200, ChannelSeriesListOut(items=[ChannelSeriesOut(ulid=o.ulid, title=o.title, media_type=o.media_type, count=o.count, media_ulid=o.media_ulid, image=o.image) for o in objs])


class ManageSeriesAPI:
    """ManageSeriesAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: SeriesListOut, 400: ErrorOut, 500: ErrorOut})
    def list(request: HttpRequest, channel_ulid: str):
        log.info("request", channel_ulid=channel_ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        ret = get_manage_series_list(user_id, channel_ulid)
        if ret.is_err:
            message = ret.err_value.message
            match ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(ret.err_value)

        objs = ret.ok_value
        return 200, SeriesListOut(items=[SeriesOut(ulid=o.ulid, title=o.title, media_type=o.media_type, count=o.count) for o in objs])

    @staticmethod
    @router.post("", response={200: SeriesCreateOut, 400: ErrorOut, 500: ErrorOut})
    def create(request: HttpRequest, input: SeriesIn):
        log.info("request", input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        ret = create_manage_series(user_id, SeriesCreateDTO(**input.model_dump()))
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

        new_ulid = ret.ok_value
        return 200, SeriesCreateOut(ulid=new_ulid)

    @staticmethod
    @router.get("/{ulid}", response={200: SeriesDetailOut, 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest, ulid: str):
        log.info("request", ulid=ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        ret = get_manage_series(user_id, ulid)
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

        obj = ret.ok_value
        return 200, convert_series_detail(obj)

    @staticmethod
    @router.put("/{ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def update(request: HttpRequest, ulid: str, input: SeriesUpdateIn):
        log.info("request", ulid=ulid, input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        ret = update_manage_series(user_id, ulid, SeriesUpdateDTO(**input.model_dump()))
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

        ret = delete_manage_series(user_id, ulid)
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


def convert_series_items(objs: list[SeriesItemDTO]) -> list[SeriesItemOut]:
    data = [SeriesItemOut(ulid=x.ulid, title=x.title, publish=x.publish) for x in objs]
    return data


def convert_series_detail(obj: SeriesDetailDTO) -> SeriesDetailOut:
    data = SeriesDetailOut(
        ulid=obj.ulid,
        title=obj.title,
        media_type=obj.media_type,
        channel_ulid=obj.channel_ulid,
        items=convert_series_items(obj.items),
        candidates=convert_series_items(obj.candidates),
    )
    return data
