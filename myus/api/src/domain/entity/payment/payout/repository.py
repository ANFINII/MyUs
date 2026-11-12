from django.db.models import Q
from api.db.models.payment import PaymentPayout
from api.src.domain.entity.index import get_save_new_ids, sort_ids
from api.src.domain.entity.payment.payout._convert import convert_data, marshal_data
from api.src.domain.interface.payment.payout.data import PayoutData
from api.src.domain.interface.payment.payout.interface import FilterOption, SortOption, PayoutInterface
from api.src.domain.interface.payment.payout.validation import validate
from api.utils.common.result import FatalError, Result


PAYOUT_FIELDS = ["provider", "external_id", "amount", "currency", "status", "arrival_at", "last_event_at"]


class PayoutRepository(PayoutInterface):
    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if len(filter.provider) > 0:
            q_list.append(Q(provider=filter.provider))
        if len(filter.external_id) > 0:
            q_list.append(Q(external_id=filter.external_id))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = PaymentPayout.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[PayoutData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(PaymentPayout.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[PayoutData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, PAYOUT_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        if len(ids) == 0:
            return Result.ok(None)
        PaymentPayout.objects.filter(id__in=ids).delete()
        return Result.ok(None)
