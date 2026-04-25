from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.master import NgWord
from api.src.domain.entity.index import sort_ids
from api.src.domain.entity.ng_word._convert import convert_data
from api.src.domain.interface.ng_word.data import NgWordData
from api.src.domain.interface.ng_word.interface import FilterOption, NgWordInterface, SortOption


class NgWordRepository(NgWordInterface):
    def queryset(self) -> QuerySet[NgWord]:
        return NgWord.objects.all()

    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.search:
            q_list.append(Q(word__icontains=filter.search))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = NgWord.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[NgWordData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]
