from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.subscribe import Subscribe
from api.src.domain.entity.subscribe._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.interface.subscribe.data import SubscribeData
from api.src.domain.interface.subscribe.interface import FilterOption, SubscribeInterface, SortOption


SUBSCRIBE_FIELDS = ["user_id", "channel_id", "is_subscribe"]


class SubscribeRepository(SubscribeInterface):
    def queryset(self) -> QuerySet[Subscribe]:
        return Subscribe.objects.select_related("user", "channel")

    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.user_id:
            q_list.append(Q(user_id=filter.user_id))
        if filter.channel_id:
            q_list.append(Q(channel_id=filter.channel_id))
        if filter.is_subscribe is not None:
            q_list.append(Q(is_subscribe=filter.is_subscribe))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Subscribe.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[SubscribeData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[SubscribeData]) -> list[int]:
        if len(objs) == 0:
            return []

        models = [marshal_data(o) for o in objs]
        new_ids = get_new_ids(models, Subscribe)

        Subscribe.objects.bulk_create(
            models,
            update_conflicts=True,
            update_fields=SUBSCRIBE_FIELDS,
        )

        return new_ids

    def count(self, filter: FilterOption) -> int:
        q_list: list[Q] = []
        if filter.user_id:
            q_list.append(Q(user_id=filter.user_id))
        if filter.channel_id:
            q_list.append(Q(channel_id=filter.channel_id))
        if filter.is_subscribe is not None:
            q_list.append(Q(is_subscribe=filter.is_subscribe))

        return Subscribe.objects.filter(*q_list).count()
