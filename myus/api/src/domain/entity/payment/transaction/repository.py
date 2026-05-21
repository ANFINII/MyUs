from django.db.models import Q
from api.db.models.payment import PaymentTransaction
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.entity.payment.transaction._convert import convert_data, marshal_data
from api.src.domain.interface.payment.transaction.data import TransactionData
from api.src.domain.interface.payment.transaction.interface import FilterOption, SortOption, TransactionInterface


TRANSACTION_FIELDS = ["subscription_id", "customer_id", "provider", "external_id", "price_amount", "price_currency", "status", "paid_at"]


class TransactionRepository(TransactionInterface):
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> list[int]:
        q_list: list[Q] = []
        if filter.customer_user_id != 0:
            q_list.append(Q(customer_id=filter.customer_user_id))
        if filter.subscription_id != 0:
            q_list.append(Q(subscription_id=filter.subscription_id))
        if len(filter.provider) > 0:
            q_list.append(Q(provider=filter.provider))
        if len(filter.external_id) > 0:
            q_list.append(Q(external_id=filter.external_id))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = PaymentTransaction.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[TransactionData]:
        if len(ids) == 0:
            return []

        objs = list(PaymentTransaction.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[TransactionData]) -> list[int]:
        if len(objs) == 0:
            return []

        models = [marshal_data(o) for o in objs]
        new_ids = get_new_ids(models, PaymentTransaction)

        PaymentTransaction.objects.bulk_create(
            models,
            update_conflicts=True,
            update_fields=TRANSACTION_FIELDS,
        )

        return new_ids
