from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.users import SearchTag
from api.src.domain.entity.search_tag._convert import convert_data, marshal_data
from api.src.domain.entity.index import sort_ids
from api.src.domain.interface.search_tag.data import SearchTagData
from api.src.domain.interface.search_tag.interface import FilterOption, SearchTagInterface, SortOption


SEARCH_TAG_FIELDS = ["author_id", "sequence", "name"]


class SearchTagRepository(SearchTagInterface):
    def queryset(self) -> QuerySet[SearchTag]:
        return SearchTag.objects.select_related("author")

    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = 20) -> list[int]:
        q_list: list[Q] = []
        if filter.author_id:
            q_list.append(Q(author_id=filter.author_id))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = SearchTag.objects.filter(*q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[SearchTagData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[SearchTagData]) -> None:
        if len(objs) == 0:
            return

        SearchTag.objects.bulk_create(
            [marshal_data(o) for o in objs],
            update_conflicts=True,
            update_fields=SEARCH_TAG_FIELDS,
        )
