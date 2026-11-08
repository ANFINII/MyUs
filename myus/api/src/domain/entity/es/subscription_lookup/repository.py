from django.db.models import Q
from api.db.models.es import EsSubscriptionLookup
from api.src.domain.entity.es.subscription_lookup._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_save_new_ids, sort_ids
from api.src.domain.interface.es.subscription_lookup.data import SubscriptionLookupData
from api.src.domain.interface.es.subscription_lookup.interface import FilterOption, SortOption, SubscriptionLookupInterface
from api.utils.common.result import FatalError, Result


SUBSCRIPTION_LOOKUP_FIELDS = ["aggregate_id", "provider", "external_id"]


class SubscriptionLookupRepository(SubscriptionLookupInterface):
    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if len(filter.provider) > 0:
            q_list.append(Q(provider=filter.provider))
        if len(filter.external_id) > 0:
            q_list.append(Q(external_id=filter.external_id))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = EsSubscriptionLookup.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[SubscriptionLookupData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(EsSubscriptionLookup.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[SubscriptionLookupData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, SUBSCRIPTION_LOOKUP_FIELDS)

        return Result.ok(new_ids)
