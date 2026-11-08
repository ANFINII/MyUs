from api.src.domain.interface.category.interface import CategoryInterface, FilterOption, SortOption, SortType
from api.src.injectors.container import injector
from api.src.types.dto.category import CategoryDTO
from api.utils.common.result import FatalError, Result


@Result.shield_exception()
def get_categories() -> Result[list[CategoryDTO], FatalError]:
    repo = injector.get(CategoryInterface)
    ids_ret = repo.get_ids(FilterOption(), SortOption(is_asc=True, sort_type=SortType.ID))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    categories_ret = repo.bulk_get(ids)
    if categories_ret.is_err:
        return Result.err(categories_ret.err_value)

    categories = categories_ret.ok_value
    return Result.ok([CategoryDTO(ulid=c.ulid, jp_name=c.jp_name, en_name=c.en_name) for c in categories])
