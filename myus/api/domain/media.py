from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce
from operator import and_

from api.types.union.media import MediaModelType
from api.utils.functions.search import search_q_list
from django.db.models import Count, F, Q


class SortType(Enum):
    ID = auto()
    CREATED = auto()
    SCORE = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    publish: bool | None = True
    category_id: int | None = None
    search: str | None = None


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.ID


class MediaDomain:
    @classmethod
    def get(cls, model: MediaModelType, id: int, publish: bool) -> MediaModelType | None:
        qs = model.objects.filter(id=id, publish=publish).first()
        return qs

    @classmethod
    def bulk_get(cls, model: MediaModelType, option: FilterOption, sort_options: SortOption, limit: int | None) -> MediaModelType:
        q_list: list[Q] = []
        if option.publish:
            q_list.append(Q(publish=option.publish))
        if option.category_id:
            q_list.append(Q(category_id=option.category_id))
        if option.search:
            q_list.append(search_q_list(option.search))

        q = reduce(and_, q_list)
        qs = model.objects.filter(q)

        if option.search:
            sort_options = SortOption(is_asc=sort_options.is_asc,sort_type=SortType.SCORE)
            score = F('read') + Count('like')*10 + F('read')*Count('like')/(F('read')+1)*20
            qs = qs.annotate(score=score)

        field_name = sort_options.sort_type.name.lower()
        order_by_key = field_name if sort_options.is_asc else f'-{field_name}'
        qs = qs.order_by(order_by_key)

        if limit:
            qs = qs[:limit]

        return qs
