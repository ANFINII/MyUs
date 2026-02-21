from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.message import Message
from api.src.domain.entity.index import sort_ids
from api.src.domain.entity.message._convert import convert_data, marshal_data
from api.src.domain.interface.message.data import MessageData
from api.src.domain.interface.message.interface import FilterOption, MessageInterface, SortOption


MESSAGE_FIELDS = ["author_id", "chat_id", "parent_id", "text"]


class MessageRepository(MessageInterface):
    def queryset(self) -> QuerySet[Message]:
        return Message.objects.select_related("author", "chat", "parent")

    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.chat_id:
            q_list.append(Q(chat_id=filter.chat_id))
        if filter.is_parent:
            q_list.append(Q(parent__isnull=True))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Message.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[MessageData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[MessageData]) -> None:
        if len(objs) == 0:
            return

        Message.objects.bulk_create(
            [marshal_data(o) for o in objs],
            update_conflicts=True,
            update_fields=MESSAGE_FIELDS,
        )
