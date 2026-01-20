from django.db.models import Count, F, Q
from django.utils import timezone
from api.db.models.media import Music
from api.src.domain.index import sort_ids
from api.src.domain.media.index import FilterOption, SortOption, ExcludeOption, SortType
from api.utils.functions.search import search_q_list
from api.utils.functions.index import set_attr


class MusicDomain:
    @classmethod
    def queryset(cls):
        return Music.objects.select_related("channel", "channel__owner").prefetch_related("like")

    @classmethod
    def get_ids(cls, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        e_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.publish:
            q_list.append(Q(publish=filter.publish))
        if filter.category_id:
            q_list.append(Q(category_id=filter.category_id))
        if filter.search:
            q_list.append(search_q_list(filter.search))
        if exclude.id:
            e_list.append(Q(id=exclude.id))

        qs = Music.objects.filter(*q_list).exclude(*e_list)

        if filter.search:
            sort = SortOption(is_asc=sort.is_asc, sort_type=SortType.SCORE)
            score = F("read") + Count("like") * 10 + F("read") * Count("like") / (F("read") + 1) * 20
            qs = qs.annotate(score=score)

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = qs.order_by(order_by_key)

        if limit:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    @classmethod
    def bulk_get(cls, ids: list[int]) -> list[Music]:
        if len(ids) == 0:
            return []

        objs = cls.queryset().filter(id__in=ids)
        return sort_ids(objs, ids)

    @classmethod
    def create(cls, **kwargs) -> Music:
        return Music.objects.create(**kwargs)

    @classmethod
    def update(cls, obj: Music, **kwargs) -> None:
        if not kwargs:
            return

        kwargs["updated"] = timezone.now()
        [set_attr(obj, key, value) for key, value in kwargs.items()]
        obj.save(update_fields=list(kwargs.keys()))
        return
