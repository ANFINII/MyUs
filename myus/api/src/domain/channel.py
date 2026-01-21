from dataclasses import dataclass
from enum import Enum
from django.db.models import Q
from django.utils import timezone
from api.db.models.channel import Channel
from api.src.domain.index import sort_ids
from api.utils.functions.index import set_attr


class SortType(Enum):
    CREATED = "created"
    UPDATED = "updated"


@dataclass(frozen=True, slots=True)
class FilterOption:
    ulid: str = ""
    owner_id: int = 0
    is_default: bool | None = None


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class ChannelDomain:
    @classmethod
    def queryset(cls):
        return Channel.objects.select_related("owner")

    @classmethod
    def get_ids(cls, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.owner_id:
            q_list.append(Q(owner_id=filter.owner_id))
        if filter.is_default is not None:
            q_list.append(Q(is_default=filter.is_default))

        field_name = sort.sort_type.value
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Channel.objects.filter(*q_list).order_by(order_by_key)

        if limit:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    @classmethod
    def bulk_get(cls, ids: list[int]) -> list[Channel]:
        if len(ids) == 0:
            return []

        objs = cls.queryset().filter(id__in=ids)
        return sort_ids(objs, ids)

    @classmethod
    def create(cls, **kwargs) -> Channel:
        return Channel.objects.create(**kwargs)

    @classmethod
    def update(cls, obj: Channel, **kwargs) -> None:
        if not kwargs:
            return

        kwargs["updated"] = timezone.now()
        [set_attr(obj, key, value) for key, value in kwargs.items()]
        obj.save(update_fields=list(kwargs.keys()))
        return

    @classmethod
    def delete(cls, obj: Channel) -> None:
        obj.delete()
        return
