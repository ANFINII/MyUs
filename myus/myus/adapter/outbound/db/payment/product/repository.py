from django.db.models import Q
from myus.db.models.payment import Product
from myus.domain.payment.product.data import ProductData
from myus.domain.payment.product.interface import FilterOption, PageOption, SortOption, ProductInterface
from myus.domain.payment.product.validation import validate
from myus.utils.common.result import FatalError, Result
from ._convert import convert_data, marshal_data
from ...common import get_save_new_ids, page_queryset, sort_ids


PRODUCT_FIELDS = ["seller_id", "product_type", "object_id", "price", "currency"]


class ProductRepository(ProductInterface):
    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.ulid != "":
            q_list.append(Q(ulid=filter.ulid))
        if filter.seller_id != 0:
            q_list.append(Q(seller_id=filter.seller_id))
        if filter.product_type is not None:
            q_list.append(Q(product_type=filter.product_type))
        if len(filter.object_ids) > 0:
            q_list.append(Q(object_id__in=filter.object_ids))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Product.objects.filter(*q_list).order_by(order_by_key)
        qs = page_queryset(qs, page)

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[ProductData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(Product.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[ProductData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, PRODUCT_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        if len(ids) == 0:
            return Result.ok(None)
        Product.objects.filter(id__in=ids).delete()
        return Result.ok(None)
