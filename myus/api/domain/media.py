from dataclasses import dataclass
from enum import Enum, auto
from django.db.models import Count, F, Q
from django.utils import timezone
from api.types.union.media import MediaModelType
from api.utils.functions.search import search_q_list


class SortType(Enum):
    ID = auto()
    CREATED = auto()
    SCORE = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    publish: bool = True
    category_id: int = 0
    search: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.ID


@dataclass(frozen=True, slots=True)
class ExcludeOption:
    id: int = 0


class MediaDomain:
    @classmethod
    def get(cls, model: MediaModelType, ulid: str, publish: bool) -> MediaModelType | None:
        qs = model.objects.filter(ulid=ulid, publish=publish).first()
        return qs

    @classmethod
    def bulk_get(cls, model: MediaModelType, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, limit: int | None) -> MediaModelType:
        q_list: list[Q] = []
        e_list: list[Q] = []
        if filter.publish:
            q_list.append(Q(publish=filter.publish))
        if filter.category_id:
            q_list.append(Q(category_id=filter.category_id))
        if filter.search:
            q_list.append(search_q_list(filter.search))
        if exclude.id:
            e_list.append(Q(id=exclude.id))

        qs = model.objects.filter(*q_list).exclude(*e_list)

        if filter.search:
            sort = SortOption(is_asc=sort.is_asc, sort_type=SortType.SCORE)
            score = F('read') + Count('like')*10 + F('read')*Count('like')/(F('read')+1)*20
            qs = qs.annotate(score=score)

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f'-{field_name}'
        qs = qs.order_by(order_by_key)

        if limit:
            qs = qs[:limit]

        return qs

    @classmethod
    def create(cls, model: MediaModelType, **kwargs) -> MediaModelType:
        return model.objects.create(**kwargs)

    @classmethod
    def update(cls, model: MediaModelType, **kwargs) -> None:
        if not kwargs:
            return

        kwargs["updated"] = timezone.now()
        [setattr(model, key, value) for key, value in kwargs.items()]
        model.save(update_fields=list(kwargs.keys()))
