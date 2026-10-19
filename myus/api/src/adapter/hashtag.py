from typing import assert_never
from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.types.dto.hashtag import HashtagDTO
from api.src.types.schema.common import ErrorOut
from api.src.types.schema.hashtag import HashtagOut, MediaHashtagsUpdateIn
from api.src.usecase.auth import auth_check
from api.src.usecase.hashtag import get_master_hashtags, update_media_hashtags
from api.utils.common.result import FatalError, NotFoundError


class MediaHashtagAPI:
    """MediaHashtagAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: list[HashtagOut], 401: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest):
        log.info("MediaHashtagAPI get")

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        hashtags_ret = get_master_hashtags()
        if hashtags_ret.is_err:
            return 500, ErrorOut(message="Internal Server Error")

        hashtags = hashtags_ret.ok_value
        return 200, [HashtagOut(ulid=h.ulid, name=h.name) for h in hashtags]

    @staticmethod
    @router.put("", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, input: MediaHashtagsUpdateIn):
        log.info("MediaHashtagAPI put", media_type=input.media_type.value, media_ulid=input.media_ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        hashtags = [HashtagDTO(ulid=h.ulid, name=h.name) for h in input.hashtags]
        update_ret = update_media_hashtags(user_id, input.media_type, input.media_ulid, hashtags)
        if update_ret.is_err:
            match update_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(message=update_ret.err_value.error_message)
                case FatalError():
                    return 500, ErrorOut(message="Internal Server Error")
                case _:
                    assert_never(update_ret.err_value)

        return 204, ErrorOut(message="保存しました!")
