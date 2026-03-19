from django.db import transaction
from api.modules.logger import log
from api.src.domain.interface.search_tag.data import SearchTagData
from api.src.domain.interface.search_tag.interface import FilterOption, SearchTagInterface, SortOption
from api.src.injectors.container import injector
from api.src.types.schema.user import SearchTagIn


def get_search_tag_data(author_id: int) -> list[SearchTagData]:
    repository = injector.get(SearchTagInterface)
    ids = repository.get_ids(FilterOption(author_id=author_id), SortOption())
    return repository.bulk_get(ids)


def save_search_tag_data(delete_ids: list[int], save_objs: list[SearchTagData]) -> bool:
    repository = injector.get(SearchTagInterface)
    try:
        with transaction.atomic():
            repository.bulk_delete(delete_ids)
            repository.bulk_save(save_objs)
        return True
    except Exception as e:
        log.error("save_search_tag_data error", exc=e)
        return False


def update_search_tags(author_id: int, tags: list[SearchTagIn]) -> bool:
    objs = get_search_tag_data(author_id)
    existing_ids = [obj.id for obj in objs]
    name_map: dict[str, int] = {obj.name: obj.id for obj in objs}

    save_objs: list[SearchTagData] = []
    keep_ids: set[int] = set()
    for tag in tags:
        existing_id = name_map.get(tag.name, 0)
        if existing_id != 0:
            keep_ids.add(existing_id)
        save_objs.append(SearchTagData(id=existing_id, author_id=author_id, sequence=tag.sequence, name=tag.name))

    delete_ids = [id for id in existing_ids if id not in keep_ids]

    return save_search_tag_data(delete_ids, save_objs)
