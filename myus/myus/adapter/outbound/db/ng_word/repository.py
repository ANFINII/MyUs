from django.db.models import Q
from django.db.models.query import QuerySet
from myus.db.models.master import NgWord
from myus.domain.ng_word.data import NgWordData
from myus.domain.ng_word.interface import FilterOption, NgWordInterface, SortOption
from myus.utils.common.result import FatalError, Result
from ..base import sort_ids
from ._convert import convert_data


class NgWordRepository(NgWordInterface):
    def queryset(self) -> QuerySet[NgWord]:
        return NgWord.objects.all()

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.search:
            q_list.append(Q(word__icontains=filter.search))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = NgWord.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[NgWordData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])
