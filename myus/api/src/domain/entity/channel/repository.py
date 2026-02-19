from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.channel import Channel
from api.src.domain.entity.channel._convert import convert_data, marshal_channel
from api.src.domain.entity.index import sort_ids
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.channel.interface import ChannelInterface, FilterOption, SortOption


CHANNEL_FIELDS = ["owner_id", "avatar", "name", "description", "is_default", "count"]


class ChannelRepository(ChannelInterface):
    def queryset(self) -> QuerySet[Channel]:
        return Channel.objects.select_related("owner")

    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
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

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[ChannelData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[ChannelData]) -> list[int]:
        if len(objs) == 0:
            return []

        save_objs = Channel.objects.bulk_create(
            [marshal_channel(o) for o in objs],
            update_conflicts=True,
            update_fields=CHANNEL_FIELDS,
        )

        return [o.id for o in save_objs]

    def delete(self, id: int) -> None:
        Channel.objects.filter(id=id).delete()
