from django.db.models import Q
from myus.db.models.payment import PaymentSeller
from myus.domain.payment.seller.data import PaymentSellerData
from myus.domain.payment.seller.interface import FilterOption, PageOption, SortOption, PaymentSellerInterface
from myus.domain.payment.seller.validation import validate
from myus.utils.common.result import FatalError, Result
from ._convert import convert_data, marshal_data
from ...common import get_save_new_ids, page_queryset, sort_ids


PAYMENT_SELLER_FIELDS = ["user_id", "provider", "external_id", "is_enabled"]


class PaymentSellerRepository(PaymentSellerInterface):
    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.user_id != 0:
            q_list.append(Q(user_id=filter.user_id))
        if len(filter.provider) > 0:
            q_list.append(Q(provider=filter.provider))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = PaymentSeller.objects.filter(*q_list).order_by(order_by_key)
        qs = page_queryset(qs, page)

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[PaymentSellerData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(PaymentSeller.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[PaymentSellerData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, PAYMENT_SELLER_FIELDS)

        return Result.ok(new_ids)
