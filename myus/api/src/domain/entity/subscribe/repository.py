from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.subscribe import Subscribe
from api.src.domain.entity.subscribe._convert import convert_data, marshal_data
from api.src.domain.entity.index import insert_new_models, sort_ids
from api.src.domain.interface.subscribe.data import SubscribeData
from api.src.domain.interface.subscribe.interface import FilterOption, SubscribeInterface, SortOption
from api.utils.common.result import FatalError, Result


SUBSCRIBE_FIELDS = ["user_id", "channel_id", "is_subscribe"]


class SubscribeRepository(SubscribeInterface):
    def queryset(self) -> QuerySet[Subscribe]:
        return Subscribe.objects.select_related("user", "channel")

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
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

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[SubscribeData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[SubscribeData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        models = [marshal_data(o) for o in objs]
        new_ids = insert_new_models(models)

        Subscribe.objects.bulk_create(
            models,
            update_conflicts=True,
            update_fields=SUBSCRIBE_FIELDS,
        )

        return Result.ok(new_ids)

    @Result.shield_exception()
    def count(self, filter: FilterOption) -> Result[int, FatalError]:
        q_list: list[Q] = []
        if filter.user_id:
            q_list.append(Q(user_id=filter.user_id))
        if filter.channel_id:
            q_list.append(Q(channel_id=filter.channel_id))
        if filter.is_subscribe is not None:
            q_list.append(Q(is_subscribe=filter.is_subscribe))

        return Result.ok(Subscribe.objects.filter(*q_list).count())
