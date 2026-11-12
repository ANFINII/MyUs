from django.db.models import Q
from myus.db.models.payment import PaymentLedgerEntry
from myus.src.domain.entity.index import get_save_new_ids, sort_ids
from myus.src.domain.entity.payment.ledger._convert import convert_data, marshal_data
from myus.src.domain.interface.payment.ledger.data import LedgerEntryData
from myus.src.domain.interface.payment.ledger.interface import FilterOption, SortOption, LedgerEntryInterface
from myus.src.domain.interface.payment.ledger.validation import validate
from myus.utils.common.result import FatalError, Result


LEDGER_ENTRY_FIELDS = ["payout_id"]


class LedgerEntryRepository(LedgerEntryInterface):
    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.transaction_id != 0:
            q_list.append(Q(transaction_id=filter.transaction_id))
        if len(filter.external_ids) > 0:
            q_list.append(Q(external_id__in=filter.external_ids))
        if filter.occurred_from is not None:
            q_list.append(Q(occurred_at__gte=filter.occurred_from))
        if filter.occurred_to is not None:
            q_list.append(Q(occurred_at__lt=filter.occurred_to))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = PaymentLedgerEntry.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[LedgerEntryData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(PaymentLedgerEntry.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[LedgerEntryData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, LEDGER_ENTRY_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        if len(ids) == 0:
            return Result.ok(None)
        PaymentLedgerEntry.objects.filter(id__in=ids).delete()
        return Result.ok(None)
