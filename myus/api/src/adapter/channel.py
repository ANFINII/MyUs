from django.http import HttpRequest
from ninja import File, Form, Router, UploadedFile
from api.modules.logger import log
from api.src.types.schema.channel import ChannelIn, ChannelOut
from api.src.types.schema.common import ErrorOut
from api.src.usecase.auth import auth_check
from api.src.usecase.channel import get_user_channels, update_user_channel
from api.utils.functions.index import create_url


class ChannelAPI:
    """チャンネルAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: list[ChannelOut], 401: ErrorOut})
    def get(request: HttpRequest):
        log.info("ChannelAPI get")

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        channels = get_user_channels(user_id)
        data = [
            ChannelOut(
                ulid=str(c.ulid),
                owner_ulid=c.owner_ulid,
                avatar=create_url(c.avatar),
                name=c.name,
                description=c.description,
                is_default=c.is_default,
                count=c.count,
            )
            for c in channels
        ]

        return 200, data

    @staticmethod
    @router.put("/{ulid}", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: ChannelIn = Form(...), avatar_file: UploadedFile = File(None)):
        log.info("ChannelAPI put", ulid=ulid, input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        if not update_user_channel(user_id, ulid, input, avatar_file):
            return 400, ErrorOut(message="保存に失敗しました!")

        return 204, ErrorOut(message="保存しました!")
