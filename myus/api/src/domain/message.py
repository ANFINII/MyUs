from dataclasses import dataclass
from enum import Enum
from django.db.models import Q
from api.db.models.message import Message
from api.src.domain.index import sort_ids


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


MESSAGE_FIELDS = ["author_id", "chat_id", "parent_id", "text"]


class MessageDomain:
    @classmethod
    def queryset(cls):
        return Message.objects.select_related("author")

    @classmethod
    def get_ids(cls, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.chat_id:
            q_list.append(Q(chat_id=filter.chat_id))
        if filter.is_parent:
            q_list.append(Q(parent__isnull=filter.is_parent))

        field_name = sort.sort_type.value
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Message.objects.filter(*q_list).order_by(order_by_key)

        if limit:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    @classmethod
    def bulk_get(cls, ids: list[int]) -> list[Message]:
        if len(ids) == 0:
            return []

        objs = cls.queryset().filter(id__in=ids)
        return sort_ids(objs, ids)

    @classmethod
    def bulk_save(cls, objs: list[Message]) -> list[Message]:
        if len(objs) == 0:
            return []

        Message.objects.bulk_create(
            objs,
            update_conflicts=True,
            update_fields=MESSAGE_FIELDS,
        )

        return cls.bulk_get([o.id for o in objs])
