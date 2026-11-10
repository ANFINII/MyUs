import re
from api.utils.common.result import Result, ValidationError


HASHTAG_MAX_LENGTH = 30
ALLOWED_PATTERN = re.compile(r"^[ぁ-んァ-ヶー一-龯a-zA-Z]+$")


def validate_name_data(name: str, ng_words: list[str]) -> Result[None, ValidationError]:
    if len(name) == 0:
        return Result.err(ValidationError("error.hashtagInvalid"))
    if len(name) > HASHTAG_MAX_LENGTH:
        return Result.err(ValidationError("error.hashtagInvalid"))
    if ALLOWED_PATTERN.match(name) is None:
        return Result.err(ValidationError("error.hashtagInvalid"))
    if any(ng in name for ng in ng_words):
        return Result.err(ValidationError("error.hashtagInvalid"))

    return Result.ok(None)
