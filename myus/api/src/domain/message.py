from dataclasses import dataclass
from enum import Enum
from django.utils import timezone
from api.db.models.message import Message
from api.src.domain.index import sort_ids
from api.utils.functions.index import set_attr


class SortType(Enum):
    CREATED = "created"


@dataclass(frozen=True, slots=True)
class FilterOption:
    chat_id: int = 0
    is_parent: bool = True


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class MessageDomain:
    @classmethod
    def queryset(cls):
        return Message.objects.select_related("author")

    @classmethod
    def get_ids(cls, filter: FilterOption, sort: SortOption = SortOption(), limit: int | None = None) -> list[int]:
        field_name = sort.sort_type.value
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Message.objects.filter(chat_id=filter.chat_id, parent__isnull=filter.is_parent)
        qs = qs.order_by(order_by_key)

        if limit:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    @classmethod
    def bulk_get(cls, ids: list[int]) -> list[Message]:
        if not ids:
            return []

        objs = cls.queryset().filter(id__in=ids)
        return sort_ids(objs, ids)

    @classmethod
    def create(cls, **kwargs) -> Message:
        return Message.objects.create(**kwargs)

    @classmethod
    def update(cls, obj: Message, **kwargs) -> None:
        if not kwargs:
            return

        kwargs["updated"] = timezone.now
        [set_attr(obj, key, value) for key, value in kwargs.items()]
        obj.save(update_fields=list(kwargs.keys()))
        return
