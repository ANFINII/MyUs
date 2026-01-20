from dataclasses import dataclass
from enum import Enum
from django.db.models import Q
from api.db.models.users import SearchTag
from api.src.domain.index import sort_ids
from api.utils.functions.index import set_attr


class SortType(Enum):
    SEQUENCE = "sequence"


@dataclass(frozen=True, slots=True)
class FilterOption:
    author_id: int = 0


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.SEQUENCE


class SearchTagDomain:
    @classmethod
    def get_ids(cls, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> list[int]:
        q_list: list[Q] = []
        if filter.author_id:
            q_list.append(Q(author_id=filter.author_id))

        field_name = sort.sort_type.value
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = SearchTag.objects.filter(*q_list).order_by(order_by_key)

        if limit:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    @classmethod
    def bulk_get(cls, ids: list[int]) -> list[SearchTag]:
        if len(ids) == 0:
            return []

        objs = list(SearchTag.objects.filter(id__in=ids))
        return sort_ids(objs, ids)

    @classmethod
    def create(cls, **kwargs) -> SearchTag:
        return SearchTag.objects.create(**kwargs)

    @classmethod
    def update(cls, obj: SearchTag, **kwargs) -> None:
        if not kwargs:
            return

        [set_attr(obj, key, value) for key, value in kwargs.items()]
        obj.save(update_fields=list(kwargs.keys()))
