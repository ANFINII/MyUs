from api.src.domain.interface.category.interface import CategoryInterface, FilterOption, SortOption, SortType
from api.src.injectors.container import injector
from api.src.types.dto.category import CategoryDTO


def get_categories() -> list[CategoryDTO]:
    repo = injector.get(CategoryInterface)
    ids = repo.get_ids(FilterOption(), SortOption(is_asc=True, sort_type=SortType.ID))
    return [CategoryDTO(ulid=c.ulid, jp_name=c.jp_name, en_name=c.en_name) for c in repo.bulk_get(ids)]
