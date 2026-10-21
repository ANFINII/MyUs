from django.db.models import Count, Q
from django.db.models.query import QuerySet
from api.db.models.message import Message
from api.src.domain.entity.index import get_save_new_ids, sort_ids
from api.src.domain.entity.message._convert import convert_data, marshal_data
from api.src.domain.interface.message.data import MessageData
from api.src.domain.interface.message.interface import FilterOption, MessageInterface, SortOption
from api.utils.common.result import FatalError, Result


MESSAGE_FIELDS = ["author_id", "chat_id", "parent_id", "text", "updated"]


class MessageRepository(MessageInterface):
    def queryset(self) -> QuerySet[Message]:
        qs: QuerySet[Message] = Message.objects.select_related("author", "chat", "parent").annotate(reply_count=Count("reply"))
        return qs

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.chat_id:
            q_list.append(Q(chat_id=filter.chat_id))
        if len(filter.chat_ids) > 0:
            q_list.append(Q(chat_id__in=filter.chat_ids))
        if filter.message_ulid:
            q_list.append(Q(ulid=filter.message_ulid))
        if filter.parent_ulid:
            q_list.append(Q(parent__ulid=filter.parent_ulid))
        if filter.is_parent is True:
            q_list.append(Q(parent__isnull=True))
        elif filter.is_parent is False:
            q_list.append(Q(parent__isnull=False))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Message.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[MessageData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[MessageData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, MESSAGE_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        Message.objects.filter(id__in=ids).delete()
        return Result.ok(None)
