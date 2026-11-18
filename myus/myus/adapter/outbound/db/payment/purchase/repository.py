from django.db.models import Q
from myus.db.models.payment import BlogPurchase
from myus.domain.payment.purchase.data import BlogPurchaseData
from myus.domain.payment.purchase.interface import FilterOption, PageOption, SortOption, BlogPurchaseInterface
from myus.domain.payment.purchase.validation import validate
from myus.utils.common.result import FatalError, Result
from ._convert import convert_data, marshal_data
from ...common import get_save_new_ids, page_queryset, sort_ids


BLOG_PURCHASE_FIELDS = ["user_id", "blog_id", "transaction_id"]


class BlogPurchaseRepository(BlogPurchaseInterface):
    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.user_id != 0:
            q_list.append(Q(user_id=filter.user_id))
        if filter.blog_id != 0:
            q_list.append(Q(blog_id=filter.blog_id))
        if filter.transaction_id != 0:
            q_list.append(Q(transaction_id=filter.transaction_id))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = BlogPurchase.objects.filter(*q_list).order_by(order_by_key)
        qs = page_queryset(qs, page)

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[BlogPurchaseData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(BlogPurchase.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[BlogPurchaseData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, BLOG_PURCHASE_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        if len(ids) == 0:
            return Result.ok(None)
        BlogPurchase.objects.filter(id__in=ids).delete()
        return Result.ok(None)
