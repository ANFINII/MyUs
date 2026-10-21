from django.db.models import Q
from api.db.models.payment import WebhookInbox
from api.src.domain.entity.index import save_models, sort_ids
from api.src.domain.entity.webhook.inbox._convert import convert_data, marshal_data
from api.src.domain.interface.webhook.inbox.data import WebhookInboxData
from api.src.domain.interface.webhook.inbox.interface import FilterOption, SortOption, WebhookInboxInterface
from api.utils.common.result import FatalError, Result


WEBHOOK_INBOX_FIELDS = ["provider", "event_id", "event_type", "external_id", "occurred_at"]


class WebhookInboxRepository(WebhookInboxInterface):
    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if len(filter.provider) > 0:
            q_list.append(Q(provider=filter.provider))
        if len(filter.event_id) > 0:
            q_list.append(Q(event_id=filter.event_id))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = WebhookInbox.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[WebhookInboxData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(WebhookInbox.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[WebhookInboxData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        models = [marshal_data(o) for o in objs]
        new_ids = save_models(models, WEBHOOK_INBOX_FIELDS)

        return Result.ok(new_ids)
