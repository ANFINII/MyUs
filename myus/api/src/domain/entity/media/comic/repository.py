from django.db import transaction
from django.db.models import Prefetch, Q
from django.db.models.query import QuerySet
from api.db.models.media import Comic, ComicPage
from api.src.domain.entity.media.comic._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.entity.media.index import filter_recommend, filter_search, sort_queryset
from api.src.domain.interface.media.comic.data import ComicData
from api.src.domain.interface.media.comic.interface import ComicInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, SortOption


COMIC_FIELDS = ["channel_id", "title", "content", "image", "read", "publish"]


class ComicRepository(ComicInterface):
    def queryset(self) -> QuerySet[Comic]:
        pages_prefetch = Prefetch("comic", queryset=ComicPage.objects.order_by("sequence"))
        return Comic.objects.select_related("channel", "channel__owner").prefetch_related("like", "hashtag", pages_prefetch)

    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.publish is not None:
            q_list.append(Q(publish=filter.publish))
        if filter.channel_id:
            q_list.append(Q(channel_id=filter.channel_id))
        if filter.category_id:
            q_list.append(Q(category__id=filter.category_id))
        if filter.is_recommend:
            q_list.append(filter_recommend())
        if filter.search:
            q_list.append(filter_search(filter.search))

        qs = Comic.objects.filter(*q_list).distinct()
        qs, order_by_key = sort_queryset(qs, sort, filter.is_recommend)
        qs = qs.order_by(order_by_key)

        if exclude.id is not None:
            qs = qs.exclude(id=exclude.id)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[ComicData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[ComicData]) -> list[int]:
        if len(objs) == 0:
            return []

        models = [marshal_data(o) for o in objs]
        new_ids = get_new_ids(models, Comic)

        with transaction.atomic():
            Comic.objects.bulk_create(
                models,
                update_conflicts=True,
                update_fields=COMIC_FIELDS,
            )
            ComicPage.objects.bulk_create([
                ComicPage(comic_id=model.id, image=page_path, sequence=seq)
                for obj, model in zip(objs, models)
                for seq, page_path in enumerate(obj.pages)
            ])

        return new_ids

    def is_liked(self, media_id: int, user_id: int) -> bool:
        return Comic.objects.filter(id=media_id, like__id=user_id).exists()
