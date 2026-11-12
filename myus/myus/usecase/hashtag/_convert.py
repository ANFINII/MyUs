from myus.domain.interface.ng_word.interface import FilterOption, NgWordInterface, SortOption
from myus.injectors.container import injector
from myus.utils.common.result import FatalError, Result


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


def has_ng_word(name: str, ng_words: list[str]) -> bool:
    return any(ng in name for ng in ng_words)
