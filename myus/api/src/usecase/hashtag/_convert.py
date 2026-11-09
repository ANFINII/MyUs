import re
from api.src.domain.interface.ng_word.interface import FilterOption, NgWordInterface, SortOption
from api.src.injectors.container import injector
from api.utils.common.result import FatalError, Result


HASHTAG_MAX_LENGTH = 30
ALLOWED_PATTERN = re.compile(r"^[ぁ-んァ-ヶー一-龯a-zA-Z]+$")


@Result.shield_exception()
def get_ng_words_data() -> Result[list[str], FatalError]:
    repo = injector.get(NgWordInterface)
    ids_ret = repo.get_ids(FilterOption(), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    ng_words_ret = repo.bulk_get(ids)
    if ng_words_ret.is_err:
        return Result.err(ng_words_ret.err_value)

    ng_words = ng_words_ret.ok_value
    return Result.ok([n.word for n in ng_words])


def normalize_name(name: str) -> str:
    return name.strip().lstrip("#").lower()


def validate_name(name: str, ng_words: list[str]) -> bool:
    if len(name) == 0:
        return False
    if len(name) > HASHTAG_MAX_LENGTH:
        return False
    if ALLOWED_PATTERN.match(name) is None:
        return False
    if any(ng in name for ng in ng_words):
        return False
    return True
