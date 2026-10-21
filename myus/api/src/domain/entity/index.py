from typing import TypeVar
from django.db import transaction
from django.db.models import Count, IntegerField, Model, OuterRef, Subquery
from django.db.models.functions import Coalesce
from api.db.models.subscribe import Subscribe
from api.db.models.users import Follow


T = TypeVar("T", bound=Model)


def sort_ids(objs: list[T], ids: list[int]) -> list[T]:
    obj_map = {obj.pk: obj for obj in objs}
    return [obj_map[id] for id in ids]


def get_save_new_ids(models: list[T], update_fields: list[str]) -> list[int]:
    new_models = [m for m in models if m.pk is None]
    existing_models = [m for m in models if m.pk is not None]

    with transaction.atomic():
        for m in new_models:
            m.save(force_insert=True)

        if len(existing_models) > 0:
            type(existing_models[0])._default_manager.bulk_create(existing_models, update_conflicts=True, update_fields=update_fields)

    return [m.pk for m in new_models]


def subscribe_count(channel_ref: str) -> Coalesce:
    qs = Subscribe.objects.filter(channel_id=OuterRef(channel_ref), is_subscribe=True).order_by().values("channel_id").annotate(count=Count("id")).values("count")
    return Coalesce(Subquery(qs), 0, output_field=IntegerField())


def follower_count(user_ref: str) -> Coalesce:
    qs = Follow.objects.filter(following_id=OuterRef(user_ref), is_follow=True).order_by().values("following_id").annotate(count=Count("id")).values("count")
    return Coalesce(Subquery(qs), 0, output_field=IntegerField())


def following_count(user_ref: str) -> Coalesce:
    qs = Follow.objects.filter(follower_id=OuterRef(user_ref), is_follow=True).order_by().values("follower_id").annotate(count=Count("id")).values("count")
    return Coalesce(Subquery(qs), 0, output_field=IntegerField())
