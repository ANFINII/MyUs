from django.db import transaction
from api.src.domain.interface.search_tag.data import SearchTagData
from api.src.domain.interface.search_tag.interface import FilterOption, SearchTagInterface, SortOption
from api.src.injectors.container import injector
from api.src.types.schema.user import SearchTagIn
from api.utils.common.result import FatalError, Result


@Result.shield_exception()
def get_search_tag_data(author_id: int) -> Result[list[SearchTagData], FatalError]:
    repository = injector.get(SearchTagInterface)
    ids_ret = repository.get_ids(FilterOption(author_id=author_id), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    tags_ret = repository.bulk_get(ids_ret.ok_value)
    if tags_ret.is_err:
        return Result.err(tags_ret.err_value)

    return Result.ok(tags_ret.ok_value)


@Result.shield_exception()
def save_search_tag_data(delete_ids: list[int], save_objs: list[SearchTagData]) -> Result[None, FatalError]:
    repository = injector.get(SearchTagInterface)
    with transaction.atomic():
        delete_ret = repository.bulk_delete(delete_ids)
        if delete_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(delete_ret.err_value)

        save_ret = repository.bulk_save(save_objs)
        if save_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def update_search_tags(author_id: int, tags: list[SearchTagIn]) -> Result[None, FatalError]:
    objs_ret = get_search_tag_data(author_id)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
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

    save_ret = save_search_tag_data(delete_ids, save_objs)
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)
