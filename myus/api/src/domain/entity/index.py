from typing import TypeVar
from django.db import connection
from django.db.models import Model


T = TypeVar("T", bound=Model)


def sort_ids(objs: list[T], ids: list[int]) -> list[T]:
    obj_map = {obj.pk: obj for obj in objs}
    return [obj_map[id] for id in ids]


def allocate_ids(model: type[Model], num: int) -> list[int]:
    table = model._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT AUTO_INCREMENT FROM information_schema.TABLES "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s",
            [table],
        )
        row = cursor.fetchone()
        assert row is not None
        first_id: int = row[0]
        cursor.execute(f"ALTER TABLE `{table}` AUTO_INCREMENT = %s", [first_id + num])
        return list(range(first_id, first_id + num))


def get_new_ids(objs: list[T], model: type[Model]) -> list[int]:
    new_objs = [o for o in objs if o.pk == 0]
    if len(new_objs) == 0:
        return []

    ids = allocate_ids(model, len(new_objs))
    for o, new_id in zip(new_objs, ids):
        o.pk = new_id
    return ids
