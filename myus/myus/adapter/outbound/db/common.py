from typing import Protocol, TypeVar
from django.db import transaction
from django.db.models import Model
from django.db.models.query import QuerySet


T = TypeVar("T", bound=Model)


class PageOption(Protocol):
    @property
    def limit(self) -> int: ...

    @property
    def offset(self) -> int: ...


def sort_ids(objs: list[T], ids: list[int]) -> list[T]:
    obj_map = {obj.pk: obj for obj in objs}
    return [obj_map[id] for id in ids if id in obj_map]


def page_queryset(qs: QuerySet[T], page: PageOption) -> QuerySet[T]:
    if page.limit == 0:
        return qs[page.offset:]
    return qs[page.offset:page.offset + page.limit]


def get_save_new_ids(models: list[T], update_fields: list[str]) -> list[int]:
    new_models = [m for m in models if m.pk is None]
    existing_models = [m for m in models if m.pk is not None]

    with transaction.atomic():
        for m in new_models:
            m.save(force_insert=True)

        if len(existing_models) > 0:
            type(existing_models[0])._default_manager.bulk_create(existing_models, update_conflicts=True, update_fields=update_fields)

    return [m.pk for m in new_models]
