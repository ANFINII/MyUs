from typing import assert_never
from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.domain.interface.advertise.data import AdvertiseData
from api.src.types.schema.advertise import AdvertiseListOut, AdvertiseOut, AdvertiseReadOut
from api.src.types.schema.common import ErrorOut, ErrorType
from api.src.usecase.advertise import get_global_advertises, get_user_advertises, increment_advertise_read
from api.utils.common.result import FatalError, NotFoundError
from api.utils.functions.index import get_client_ip


class AdvertiseAPI:
    """AdvertiseAPI"""

    router = Router()

    @staticmethod
    @router.get("/global", response={200: AdvertiseListOut, 500: ErrorOut})
    def list_global(request: HttpRequest):
        log.info("AdvertiseAPI list_global")

        ret = get_global_advertises()
        if ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs = ret.ok_value
        return 200, AdvertiseListOut(items=convert_advertises(objs), total=len(objs))

    @staticmethod
    @router.get("/user/{user_ulid}", response={200: AdvertiseListOut, 500: ErrorOut})
    def list_by_user(request: HttpRequest, user_ulid: str):
        log.info("AdvertiseAPI list_by_user", user_ulid=user_ulid)

        ret = get_user_advertises(user_ulid)
        if ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        objs = ret.ok_value
        return 200, AdvertiseListOut(items=convert_advertises(objs), total=len(objs))

    @staticmethod
    @router.post("/{ulid}/read", response={200: AdvertiseReadOut, 400: ErrorOut, 500: ErrorOut})
    def post_read(request: HttpRequest, ulid: str):
        log.info("AdvertiseAPI post_read", ulid=ulid)

        ret = increment_advertise_read(ulid, get_client_ip(request))
        if ret.is_err:
            message = ret.err_value.message
            match ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(ret.err_value)

        read = ret.ok_value
        return 200, AdvertiseReadOut(read=read)


def convert_advertises(objs: list[AdvertiseData]) -> list[AdvertiseOut]:
    return [
        AdvertiseOut(
            ulid=o.ulid,
            title=o.title,
            url=o.url,
            content=o.content,
            image=o.image,
            video=o.video,
            read=o.read,
            type=o.type,
            period=o.period,
            publish=o.publish,
            created=o.created,
            updated=o.updated,
        )
        for o in objs
    ]
