from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.master import Category
from api.src.domain.entity.category._convert import convert_data
from api.src.domain.entity.index import sort_ids
from api.src.domain.interface.category.data import CategoryData
from api.src.domain.interface.category.interface import CategoryInterface, FilterOption, SortOption


class CategoryRepository(CategoryInterface):
    def queryset(self) -> QuerySet[Category]:
        return Category.objects.all()

    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if len(filter.ulids) > 0:
            q_list.append(Q(ulid__in=filter.ulids))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Category.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[CategoryData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]
