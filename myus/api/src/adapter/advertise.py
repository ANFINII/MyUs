from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.domain.interface.advertise.data import AdvertiseData
from api.src.types.schema.advertise import AdvertiseListOut, AdvertiseOut, AdvertiseReadOut
from api.src.types.schema.common import ErrorOut
from api.src.usecase.advertise import get_user_advertises, increment_advertise_read
from api.utils.common.result import FatalError


class AdvertiseAPI:
    """AdvertiseAPI"""

    router = Router()

    @staticmethod
    @router.get("/user/{user_ulid}", response={200: AdvertiseListOut, 500: ErrorOut})
    def list_by_user(request: HttpRequest, user_ulid: str):
        log.info("AdvertiseAPI list_by_user", user_ulid=user_ulid)

        ret = get_user_advertises(user_ulid)
        if ret.is_err:
            return 500, ErrorOut(message="サーバーエラーが発生しました")

        objs = ret.ok_value
        return 200, AdvertiseListOut(items=convert_advertises(objs), total=len(objs))

    @staticmethod
    @router.post("/{ulid}/read", response={200: AdvertiseReadOut, 404: ErrorOut, 500: ErrorOut})
    def post_read(request: HttpRequest, ulid: str):
        log.info("AdvertiseAPI post_read", ulid=ulid)

        ret = increment_advertise_read(ulid)
        if ret.is_err:
            if isinstance(ret.err_value, FatalError):
                return 500, ErrorOut(message="サーバーエラーが発生しました")
            return 404, ErrorOut(message=ret.err_value.error_message)

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
