from typing import TypeVar
from django.db.models import Model


T = TypeVar("T", bound=Model)


def sort_ids(objs: list[T], ids: list[int]) -> list[T]:
    obj_map = {obj.pk: obj for obj in objs}
    return [obj_map[id] for id in ids]


def get_new_ids(models: list[T]) -> list[int]:
    new_models = [m for m in models if m.pk is None]
    for m in new_models:
        m.save(force_insert=True)

    return [m.pk for m in new_models]
