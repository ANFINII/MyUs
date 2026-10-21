from typing import assert_never
from django.http import HttpRequest
from ninja import File, Form, Router, UploadedFile
from api.modules.logger import log
from api.src.adapter._auth import auth_check
from api.src.types.schema.channel import ChannelCreateOut, ChannelIn, ChannelOut
from api.src.types.schema.common import ErrorOut, ErrorType, SuccessOut
from api.src.types.schema.subscribe import SubscribeIn, SubscribeOut
from api.src.usecase.channel import create_user_channel, get_user_channels, update_user_channel
from api.src.usecase.subscribe import get_subscribe_channels, upsert_subscribe
from api.utils.common.result import FatalError, ForbiddenError, NotFoundError, ValidationError
from api.utils.functions.index import create_url


class ChannelAPI:
    """チャンネルAPI"""

    router = Router()

    @staticmethod
    @router.get("/user", response={200: list[ChannelOut], 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest):
        log.info("ChannelAPI get")

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        channels_ret = get_user_channels(user_id)
        if channels_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        channels = channels_ret.ok_value
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
    @router.get("/subscribe", response={200: list[ChannelOut], 400: ErrorOut, 500: ErrorOut})
    def get_subscribe(request: HttpRequest):
        log.info("ChannelAPI get_subscribe")

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        channels_ret = get_subscribe_channels(user_id)
        if channels_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        channels = channels_ret.ok_value
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
    @router.post("/subscribe", response={200: SubscribeOut, 400: ErrorOut, 500: ErrorOut})
    def post_subscribe(request: HttpRequest, input: SubscribeIn):
        log.info("ChannelAPI post_subscribe", input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        subscribe_ret = upsert_subscribe(user_id, input.channel_ulid, input.is_subscribe)
        if subscribe_ret.is_err:
            message = subscribe_ret.err_value.message
            match subscribe_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(subscribe_ret.err_value)

        subscribe = subscribe_ret.ok_value
        data = SubscribeOut(is_subscribe=subscribe.is_subscribe, count=subscribe.count)
        return 200, data

    @staticmethod
    @router.post("", response={200: ChannelCreateOut, 400: ErrorOut, 500: ErrorOut})
    def post(request: HttpRequest, input: ChannelIn = Form(...), avatar_file: UploadedFile = File(None)):
        log.info("ChannelAPI post", input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        create_ret = create_user_channel(user_id, input, avatar_file)
        if create_ret.is_err:
            message = create_ret.err_value.message
            match create_ret.err_value:
                case ValidationError():
                    return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(create_ret.err_value)

        ulid = create_ret.ok_value
        return 200, ChannelCreateOut(ulid=ulid)

    @staticmethod
    @router.put("/{ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, ulid: str, input: ChannelIn = Form(...), avatar_file: UploadedFile = File(None)):
        log.info("ChannelAPI put", ulid=ulid, input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        update_ret = update_user_channel(user_id, ulid, input, avatar_file)
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
