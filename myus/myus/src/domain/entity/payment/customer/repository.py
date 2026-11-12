from django.db.models import Q
from myus.db.models.payment import PaymentCustomer
from myus.src.domain.entity.index import get_save_new_ids, sort_ids
from myus.src.domain.entity.payment.customer._convert import convert_data, marshal_data
from myus.src.domain.interface.payment.customer.data import PaymentCustomerData
from myus.src.domain.interface.payment.customer.interface import FilterOption, SortOption, PaymentCustomerInterface
from myus.src.domain.interface.payment.customer.validation import validate
from myus.utils.common.result import FatalError, Result


PAYMENT_CUSTOMER_FIELDS = ["user_id", "provider", "external_id"]


class PaymentCustomerRepository(PaymentCustomerInterface):
    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.user_id != 0:
            q_list.append(Q(user_id=filter.user_id))
        if len(filter.provider) > 0:
            q_list.append(Q(provider=filter.provider))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = PaymentCustomer.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[PaymentCustomerData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(PaymentCustomer.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[PaymentCustomerData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, PAYMENT_CUSTOMER_FIELDS)

        return Result.ok(new_ids)
