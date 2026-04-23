from django.db.models.query import QuerySet
from api.db.models.media import Chat
from api.src.domain.entity.media.chat._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.entity.media.index import filter_q_list, sort_queryset
from api.src.domain.interface.media.chat.data import ChatData
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption


CHAT_FIELDS = ["channel_id", "title", "content", "read", "period", "publish"]


class ChatRepository(ChatInterface):
    def queryset(self) -> QuerySet[Chat]:
        return Chat.objects.select_related("channel", "channel__owner").prefetch_related("like", "hashtag")

    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, page: PageOption, user_id: int | None = None) -> list[int]:
        qs = Chat.objects.filter(*filter_q_list(filter, exclude)).distinct()
        qs, order_by_key = sort_queryset(qs, sort, filter.is_recommend, user_id)
        qs = qs.order_by(order_by_key)
        qs = qs[page.offset:page.offset + page.limit]
        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[ChatData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[ChatData]) -> list[int]:
        if len(objs) == 0:
            return []

        models = [marshal_data(o) for o in objs]
        new_ids = get_new_ids(models, Chat)

        Chat.objects.bulk_create(
            models,
            update_conflicts=True,
            update_fields=CHAT_FIELDS,
        )

        return new_ids

    def bulk_delete(self, ids: list[int]) -> None:
        Chat.objects.filter(id__in=ids).delete()

    def count(self, filter: FilterOption) -> int:
        return Chat.objects.filter(*filter_q_list(filter)).distinct().count()

    def is_liked(self, media_id: int, user_id: int) -> bool:
        return Chat.objects.filter(id=media_id, like__id=user_id).exists()
