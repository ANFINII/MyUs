from django.db import transaction
from django.db.models import Count, Prefetch, F
from django.db.models.query import QuerySet
from myus.db.models.media import Comic, ComicPage
from myus.domain.media.comic.data import ComicData
from myus.domain.media.comic.interface import ComicInterface
from myus.domain.media.comic.validation import validate
from myus.domain.media.common import FilterOption, PageOption, SortOption
from myus.utils.common.result import FatalError, Result
from ._convert import convert_data, marshal_data
from ..common import filter_queryset, get_ids_queryset
from ...common import get_save_new_ids, sort_ids


COMIC_FIELDS = ["channel_id", "title", "content", "image", "publish", "publish_at", "updated"]


class ComicRepository(ComicInterface):
    def queryset(self) -> QuerySet[Comic]:
        pages_prefetch = Prefetch("comic", queryset=ComicPage.objects.order_by("sequence"))
        return Comic.objects.select_related("channel", "channel__owner").prefetch_related("hashtag", "category", pages_prefetch).annotate(like_count=Count("like"))

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        qs = get_ids_queryset(Comic.objects.all(), filter, sort, page)
        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[ComicData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[ComicData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]

        with transaction.atomic():
            new_ids = get_save_new_ids(models, COMIC_FIELDS)
            new_id_set = set(new_ids)
            ComicPage.objects.bulk_create([
                ComicPage(comic_id=model.id, image=page_path, sequence=seq)
                for obj, model in zip(objs, models)
                if model.id in new_id_set
                for seq, page_path in enumerate(obj.pages)
            ])

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        Comic.objects.filter(id__in=ids).delete()
        return Result.ok(None)

    @Result.shield_exception()
    def count(self, filter: FilterOption) -> Result[int, FatalError]:
        qs = filter_queryset(Comic.objects.all(), filter)
        return Result.ok(qs.count())

    @Result.shield_exception()
    def is_liked(self, media_id: int, user_id: int) -> Result[bool, FatalError]:
        return Result.ok(Comic.objects.filter(id=media_id, like__id=user_id).exists())

    @Result.shield_exception()
    def save_read(self, media_id: int) -> Result[int, FatalError]:
        Comic.objects.filter(id=media_id).update(read=F("read") + 1)
        read = Comic.objects.filter(id=media_id).values_list("read", flat=True).first()
        return Result.ok(read if read is not None else 0)
