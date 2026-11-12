from myus.src.domain.interface.category.data import CategoryData
from myus.src.domain.interface.category.interface import CategoryInterface, FilterOption, SortOption
from myus.src.injectors.container import injector
from myus.utils.common.result import FatalError, Result


@Result.shield_exception()
def get_category_data(ulid: str) -> Result[CategoryData, FatalError]:
    repo = injector.get(CategoryInterface)
    ids_ret = repo.get_ids(FilterOption(ulids=[ulid]), SortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        return Result.err(FatalError(f"Category not found ulid={ulid}"))

    categories_ret = repo.bulk_get(ids)
    if categories_ret.is_err:
        return Result.err(categories_ret.err_value)

    categories = categories_ret.ok_value
    data = categories[0]
    return Result.ok(data)
