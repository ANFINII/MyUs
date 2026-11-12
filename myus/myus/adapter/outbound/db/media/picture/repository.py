from django.db.models import Count, F
from django.db.models.query import QuerySet
from myus.db.models.media import Picture
from myus.domain.media.option import ExcludeOption, FilterOption, PageOption, SortOption
from myus.domain.media.picture.data import PictureData
from myus.domain.media.picture.interface import PictureInterface
from myus.domain.media.picture.validation import validate
from myus.utils.common.result import FatalError, Result
from ._convert import convert_data, marshal_data
from ..query import distinct_queryset, filter_q_list, sort_queryset
from ...base import get_save_new_ids, sort_ids


PICTURE_FIELDS = ["channel_id", "title", "content", "image", "publish", "publish_at", "updated"]


class PictureRepository(PictureInterface):
    def queryset(self) -> QuerySet[Picture]:
        return Picture.objects.select_related("channel", "channel__owner").prefetch_related("hashtag", "category").annotate(like_count=Count("like"))

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, page: PageOption, user_id: int | None = None) -> Result[list[int], FatalError]:
        qs = Picture.objects.filter(*filter_q_list(filter, exclude))
        qs = distinct_queryset(qs, filter)
        qs, order_by_key = sort_queryset(qs, sort, filter.is_recommend, user_id)
        qs = qs.order_by(order_by_key)
        qs = qs[page.offset:page.offset + page.limit]
        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[PictureData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[PictureData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, PICTURE_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        Picture.objects.filter(id__in=ids).delete()
        return Result.ok(None)

    @Result.shield_exception()
    def count(self, filter: FilterOption) -> Result[int, FatalError]:
        qs = Picture.objects.filter(*filter_q_list(filter))
        return Result.ok(distinct_queryset(qs, filter).count())

    @Result.shield_exception()
    def is_liked(self, media_id: int, user_id: int) -> Result[bool, FatalError]:
        return Result.ok(Picture.objects.filter(id=media_id, like__id=user_id).exists())

    @Result.shield_exception()
    def save_read(self, media_id: int) -> Result[int, FatalError]:
        Picture.objects.filter(id=media_id).update(read=F("read") + 1)
        read = Picture.objects.filter(id=media_id).values_list("read", flat=True).first()
        return Result.ok(read if read is not None else 0)
