from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.channel import Channel
from api.src.domain.entity.channel._convert import convert_data, marshal_data
from api.src.domain.entity.index import save_models, sort_ids
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.channel.interface import ChannelInterface, FilterOption, SortOption
from api.utils.common.result import FatalError, Result


CHANNEL_FIELDS = ["owner_id", "avatar", "name", "description", "is_default", "count"]


class ChannelRepository(ChannelInterface):
    def queryset(self) -> QuerySet[Channel]:
        return Channel.objects.select_related("owner")

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.owner_id:
            q_list.append(Q(owner_id=filter.owner_id))
        if filter.is_default is not None:
            q_list.append(Q(is_default=filter.is_default))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Channel.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[ChannelData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[ChannelData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        models = [marshal_data(o) for o in objs]
        new_ids = save_models(models, CHANNEL_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def delete(self, id: int) -> Result[None, FatalError]:
        Channel.objects.filter(id=id).delete()
        return Result.ok(None)
