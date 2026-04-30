from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.domain.interface.advertise.data import AdvertiseData
from api.src.types.schema.advertise import AdvertiseListOut, AdvertiseOut, AdvertiseReadOut
from api.src.types.schema.common import ErrorOut
from api.src.usecase.advertise import get_user_advertises, increment_advertise_read


class AdvertiseAPI:
    """AdvertiseAPI"""

    router = Router()

    @staticmethod
    @router.get("/user/{user_ulid}", response={200: AdvertiseListOut})
    def list_by_user(request: HttpRequest, user_ulid: str):
        log.info("AdvertiseAPI list_by_user", user_ulid=user_ulid)

        objs = get_user_advertises(user_ulid)
        return 200, AdvertiseListOut(datas=convert_advertises(objs), total=len(objs))

    @staticmethod
    @router.post("/{ulid}/read", response={200: AdvertiseReadOut, 404: ErrorOut})
    def post_read(request: HttpRequest, ulid: str):
        log.info("AdvertiseAPI post_read", ulid=ulid)

        new_count = increment_advertise_read(ulid)
        if new_count is None:
            return 404, ErrorOut(message="Advertise not found")

        return 200, AdvertiseReadOut(read=new_count)


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
