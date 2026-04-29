from django.db import transaction
from django.db.models import Count, Prefetch
from django.db.models.query import QuerySet
from api.db.models.media import Comic, ComicPage
from api.src.domain.entity.media.comic._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.entity.media.index import distinct_queryset, filter_q_list, sort_queryset
from api.src.domain.interface.media.comic.data import ComicData
from api.src.domain.interface.media.comic.interface import ComicInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption


COMIC_FIELDS = ["channel_id", "title", "content", "image", "read", "publish"]


class ComicRepository(ComicInterface):
    def queryset(self) -> QuerySet[Comic]:
        pages_prefetch = Prefetch("comic", queryset=ComicPage.objects.order_by("sequence"))
        return Comic.objects.select_related("channel", "channel__owner").prefetch_related("hashtag", "category", pages_prefetch).annotate(like_count=Count("like"))

    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, page: PageOption, user_id: int | None = None) -> list[int]:
        qs = Comic.objects.filter(*filter_q_list(filter, exclude))
        qs = distinct_queryset(qs, filter)
        qs, order_by_key = sort_queryset(qs, sort, filter.is_recommend, user_id)
        qs = qs.order_by(order_by_key)
        qs = qs[page.offset:page.offset + page.limit]
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
        new_id_set = set(new_ids)

        with transaction.atomic():
            Comic.objects.bulk_create(
                models,
                update_conflicts=True,
                update_fields=COMIC_FIELDS,
            )
            ComicPage.objects.bulk_create([
                ComicPage(comic_id=model.id, image=page_path, sequence=seq)
                for obj, model in zip(objs, models)
                if model.id in new_id_set
                for seq, page_path in enumerate(obj.pages)
            ])

        return new_ids

    def bulk_delete(self, ids: list[int]) -> None:
        Comic.objects.filter(id__in=ids).delete()

    def count(self, filter: FilterOption) -> int:
        qs = Comic.objects.filter(*filter_q_list(filter))
        return distinct_queryset(qs, filter).count()

    def is_liked(self, media_id: int, user_id: int) -> bool:
        return Comic.objects.filter(id=media_id, like__id=user_id).exists()
