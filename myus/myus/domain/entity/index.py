from typing import TypeVar
from django.db import transaction
from django.db.models import Model


T = TypeVar("T", bound=Model)


def sort_ids(objs: list[T], ids: list[int]) -> list[T]:
    obj_map = {obj.pk: obj for obj in objs}
    return [obj_map[id] for id in ids if id in obj_map]


def get_save_new_ids(models: list[T], update_fields: list[str]) -> list[int]:
    new_models = [m for m in models if m.pk is None]
    existing_models = [m for m in models if m.pk is not None]

    with transaction.atomic():
        for m in new_models:
            m.save(force_insert=True)

        if len(existing_models) > 0:
            type(existing_models[0])._default_manager.bulk_create(existing_models, update_conflicts=True, update_fields=update_fields)

    return [m.pk for m in new_models]
