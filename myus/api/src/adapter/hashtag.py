from typing import assert_never
from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.adapter._auth import auth_check
from api.src.types.dto.hashtag import HashtagDTO
from api.src.types.schema.common import ErrorOut, ErrorType, SuccessOut
from api.src.types.schema.hashtag import HashtagOut, MediaHashtagsUpdateIn
from api.src.usecase.hashtag import get_master_hashtags, update_media_hashtags
from api.utils.common.result import FatalError, ForbiddenError, NotFoundError


class MediaHashtagAPI:
    """MediaHashtagAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: list[HashtagOut], 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest):
        log.info("MediaHashtagAPI get")

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        hashtags_ret = get_master_hashtags()
        if hashtags_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        hashtags = hashtags_ret.ok_value
        return 200, [HashtagOut(ulid=h.ulid, name=h.name) for h in hashtags]

    @staticmethod
    @router.put("", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, input: MediaHashtagsUpdateIn):
        log.info("MediaHashtagAPI put", media_type=input.media_type.value, media_ulid=input.media_ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        hashtags = [HashtagDTO(ulid=h.ulid, name=h.name) for h in input.hashtags]
        update_ret = update_media_hashtags(user_id, input.media_type, input.media_ulid, hashtags)
        if update_ret.is_err:
            message = update_ret.err_value.message
            match update_ret.err_value:
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(update_ret.err_value)

        return 200, SuccessOut(message="保存しました!")
