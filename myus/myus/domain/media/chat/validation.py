from myus.domain.media.chat.data import ChatData
from myus.utils.common.result import Result, ValidationError


CHAT_TITLE_MAX_LENGTH = 100


def validate(obj: ChatData) -> Result[None, ValidationError]:
    if len(obj.title) > CHAT_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))

    return Result.ok(None)
