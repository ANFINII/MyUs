from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.master import Category
from api.src.domain.entity.category._convert import convert_data, get_media_model
from api.src.domain.entity.index import sort_ids
from api.src.domain.interface.category.data import CategoryData
from api.src.domain.interface.category.interface import CategoryInterface, FilterOption, SortOption
from api.utils.common.result import FatalError, Result
from api.utils.enum.media import MediaType


class CategoryRepository(CategoryInterface):
    def queryset(self) -> QuerySet[Category]:
        return Category.objects.all()

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if len(filter.ulids) > 0:
            q_list.append(Q(ulid__in=filter.ulids))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Category.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[CategoryData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, media_type: MediaType, media_id: int, objs: list[CategoryData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            category_ids: list[int] = []
        else:
            ulids = [o.ulid for o in objs if o.ulid]
            existing_map = {c.ulid: c.id for c in Category.objects.filter(ulid__in=ulids)}
            category_ids = [existing_map[o.ulid] for o in objs if o.ulid in existing_map]

        model_class = get_media_model(media_type)
        obj = model_class.objects.get(id=media_id)
        obj.category.set(category_ids)

        return Result.ok(category_ids)
