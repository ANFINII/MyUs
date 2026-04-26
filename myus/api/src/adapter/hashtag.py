from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.types.schema.common import ErrorOut
from api.src.types.schema.hashtag import MediaHashtagsUpdateIn
from api.src.usecase.auth import auth_check
from api.src.usecase.hashtag import HashtagInput, update_media_hashtags


class MediaHashtagAPI:
    """MediaHashtagAPI"""

    router = Router()

    @staticmethod
    @router.put("", response={204: ErrorOut, 400: ErrorOut, 401: ErrorOut})
    def put(request: HttpRequest, input: MediaHashtagsUpdateIn):
        log.info("MediaHashtagAPI put", media_type=input.media_type.value, media_ulid=input.media_ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        hashtags = [HashtagInput(ulid=h.ulid, name=h.name) for h in input.hashtags]
        if not update_media_hashtags(user_id, input.media_type, input.media_ulid, hashtags):
            return 400, ErrorOut(message="保存に失敗しました!")

        return 204, ErrorOut(message="保存しました!")
