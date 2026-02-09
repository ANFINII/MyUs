from dataclasses import dataclass
from enum import Enum
from django.db.models import Q
from api.db.models.users import SearchTag
from api.src.domain.index import sort_ids


class SortType(Enum):
    SEQUENCE = "sequence"


@dataclass(frozen=True, slots=True)
class FilterOption:
    author_id: int = 0


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.SEQUENCE


SEARCH_TAG_FIELDS = ["author_id", "sequence", "name"]


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
    def bulk_save(cls, objs: list[SearchTag]) -> list[SearchTag]:
        if len(objs) == 0:
            return []

        SearchTag.objects.bulk_create(
            objs,
            update_conflicts=True,
            update_fields=SEARCH_TAG_FIELDS,
        )

        return cls.bulk_get([o.id for o in objs])
