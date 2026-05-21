from django.db.models import Q
from api.db.models.payment import Subscription
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.entity.payment.subscription._convert import convert_data, marshal_data
from api.src.domain.interface.payment.subscription.data import SubscriptionData
from api.src.domain.interface.payment.subscription.interface import FilterOption, SortOption, SubscriptionInterface


SUBSCRIPTION_FIELDS = ["customer_id", "seller_id", "provider", "external_id", "product_code", "price_amount", "price_currency", "status", "started_at", "current_period_end", "canceled_at"]


class SubscriptionRepository(SubscriptionInterface):
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> list[int]:
        q_list: list[Q] = []
        if filter.customer_user_id != 0:
            q_list.append(Q(customer_id=filter.customer_user_id))
        if len(filter.provider) > 0:
            q_list.append(Q(provider=filter.provider))
        if len(filter.external_id) > 0:
            q_list.append(Q(external_id=filter.external_id))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Subscription.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[SubscriptionData]:
        if len(ids) == 0:
            return []

        objs = list(Subscription.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[SubscriptionData]) -> list[int]:
        if len(objs) == 0:
            return []

        models = [marshal_data(o) for o in objs]
        new_ids = get_new_ids(models, Subscription)

        Subscription.objects.bulk_create(
            models,
            update_conflicts=True,
            update_fields=SUBSCRIPTION_FIELDS,
        )

        return new_ids
