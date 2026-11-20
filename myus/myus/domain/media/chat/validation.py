from myus.utils.common.result import Result, ValidationError
from .data import ChatData
from ..common import MEDIA_TITLE_MAX


def validate(obj: ChatData) -> Result[None, ValidationError]:
    if len(obj.title) > MEDIA_TITLE_MAX:
        return Result.err(ValidationError("error.titleLength"))

    return Result.ok(None)
