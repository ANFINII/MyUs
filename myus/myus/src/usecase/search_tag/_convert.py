from myus.src.domain.interface.search_tag.data import SearchTagData
from myus.src.domain.interface.search_tag.interface import SearchTagInterface
from myus.src.injectors.container import injector
from myus.utils.common.result import FatalError, Result


@Result.shield_exception()
def save_search_tag_data(delete_ids: list[int], save_objs: list[SearchTagData]) -> Result[None, FatalError]:
    repo = injector.get(SearchTagInterface)
    delete_ret = repo.bulk_delete(delete_ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    save_ret = repo.bulk_save(save_objs)
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)
