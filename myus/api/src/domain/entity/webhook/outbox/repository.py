from django.db.models import Q
from api.db.models.payment import WebhookOutbox
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.entity.webhook.outbox._convert import convert_data, marshal_data
from api.src.domain.interface.webhook.outbox.data import WebhookOutboxData
from api.src.domain.interface.webhook.outbox.interface import FilterOption, SortOption, WebhookOutboxInterface


WEBHOOK_OUTBOX_FIELDS = ["provider", "event_type", "external_id", "payload", "status", "occurred_at", "delivered_at"]


class WebhookOutboxRepository(WebhookOutboxInterface):
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> list[int]:
        q_list: list[Q] = []
        if len(filter.provider) > 0:
            q_list.append(Q(provider=filter.provider))
        if len(filter.external_id) > 0:
            q_list.append(Q(external_id=filter.external_id))
        if len(filter.status) > 0:
            q_list.append(Q(status=filter.status))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = WebhookOutbox.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[WebhookOutboxData]:
        if len(ids) == 0:
            return []

        objs = list(WebhookOutbox.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[WebhookOutboxData]) -> list[int]:
        if len(objs) == 0:
            return []

        models = [marshal_data(o) for o in objs]
        new_ids = get_new_ids(models, WebhookOutbox)

        WebhookOutbox.objects.bulk_create(
            models,
            update_conflicts=True,
            update_fields=WEBHOOK_OUTBOX_FIELDS,
        )

        return new_ids
