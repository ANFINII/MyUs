import re
from api.src.domain.interface.hashtag.data import HashtagData
from api.utils.common.result import Result, ValidationError


HASHTAG_MAX_LENGTH = 30
ALLOWED_PATTERN = re.compile(r"^[ぁ-んァ-ヶー一-龯a-zA-Z]+$")


def validate(obj: HashtagData) -> Result[None, ValidationError]:
    if len(obj.name) == 0 or len(obj.name) > HASHTAG_MAX_LENGTH:
        return Result.err(ValidationError("error.nameLength"))
    if ALLOWED_PATTERN.match(obj.name) is None:
        return Result.err(ValidationError("error.nameInvalid"))
    return Result.ok(None)
