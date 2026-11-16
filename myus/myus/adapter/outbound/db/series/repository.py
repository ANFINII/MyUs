from django.db import transaction
from django.db.models import Prefetch, Q
from django.db.models.query import QuerySet
from myus.db.models.series import Series, SeriesMedia
from myus.domain.series.data import SeriesData
from myus.domain.series.interface import FilterOption, PageOption, SeriesInterface, SortOption
from myus.domain.series.validation import validate
from myus.utils.common.result import FatalError, Result
from ._convert import convert_data, marshal_data
from ..common import get_save_new_ids, page_queryset, sort_ids


SERIES_FIELDS = ["channel_id", "media_type", "title", "updated"]


class SeriesRepository(SeriesInterface):
    def queryset(self) -> QuerySet[Series]:
        return Series.objects.prefetch_related(Prefetch("series_media", queryset=SeriesMedia.objects.order_by("sequence")))

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.channel_id:
            q_list.append(Q(channel_id=filter.channel_id))
        if filter.media_type is not None:
            q_list.append(Q(media_type=filter.media_type))
        if len(filter.media_ids) > 0:
            q_list.append(Q(series_media__object_id__in=filter.media_ids))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Series.objects.filter(*q_list).distinct().order_by(order_by_key, "id" if sort.is_asc else "-id")
        qs = page_queryset(qs, page)

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[SeriesData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[SeriesData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]

        with transaction.atomic():
            new_ids = get_save_new_ids(models, SERIES_FIELDS)
            series_ids = [model.id for model in models]
            SeriesMedia.objects.filter(series_id__in=series_ids).delete()
            SeriesMedia.objects.bulk_create([
                SeriesMedia(series_id=model.id, media_type=obj.media_type, object_id=media_id, sequence=seq)
                for obj, model in zip(objs, models)
                for seq, media_id in enumerate(obj.media_ids)
            ])

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        if len(ids) == 0:
            return Result.ok(None)
        Series.objects.filter(id__in=ids).delete()
        return Result.ok(None)
