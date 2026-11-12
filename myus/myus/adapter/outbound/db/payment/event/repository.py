from django.db.models import Q
from myus.db.models.payment import DATETIME_MIN, PaymentEvent
from myus.adapter.outbound.db.index import get_save_new_ids, sort_ids
from myus.adapter.outbound.db.payment.event._convert import convert_data, marshal_data
from myus.domain.interface.payment.event.data import PaymentEventData
from myus.domain.interface.payment.event.interface import FilterOption, SortOption, PaymentEventInterface
from myus.domain.interface.payment.event.validation import validate
from myus.utils.common.result import FatalError, Result


PAYMENT_EVENT_FIELDS = ["provider", "event_id", "event_type", "external_id", "payload", "content", "occurred_at", "processed_at", "attempts", "last_error"]


class PaymentEventRepository(PaymentEventInterface):
    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if len(filter.provider) > 0:
            q_list.append(Q(provider=filter.provider))
        if len(filter.event_id) > 0:
            q_list.append(Q(event_id=filter.event_id))
        if filter.is_processed is not None:
            q_list.append(~Q(processed_at=DATETIME_MIN) if filter.is_processed else Q(processed_at=DATETIME_MIN))
        if filter.max_attempts > 0:
            q_list.append(Q(attempts__lt=filter.max_attempts))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = PaymentEvent.objects.filter(*q_list).order_by(order_by_key, "id" if sort.is_asc else "-id")

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[PaymentEventData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(PaymentEvent.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[PaymentEventData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, PAYMENT_EVENT_FIELDS)

        return Result.ok(new_ids)
