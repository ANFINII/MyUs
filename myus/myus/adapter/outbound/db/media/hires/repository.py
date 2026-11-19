from django.db.models import Q
from myus.db.models.media import MusicHires
from myus.domain.media.hires.data import MusicHiresData
from myus.domain.media.hires.interface import FilterOption, PageOption, SortOption, MusicHiresInterface
from myus.domain.media.hires.validation import validate
from myus.utils.common.result import FatalError, Result
from ._convert import convert_data, marshal_data
from ...common import get_save_new_ids, page_queryset, sort_ids


MUSIC_HIRES_FIELDS = ["music_id", "file", "sample_rate", "bit_depth", "price", "currency"]


class MusicHiresRepository(MusicHiresInterface):
    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.music_id != 0:
            q_list.append(Q(music_id=filter.music_id))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = MusicHires.objects.filter(*q_list).order_by(order_by_key)
        qs = page_queryset(qs, page)

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[MusicHiresData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(MusicHires.objects.filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[MusicHiresData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, MUSIC_HIRES_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        if len(ids) == 0:
            return Result.ok(None)
        MusicHires.objects.filter(id__in=ids).delete()
        return Result.ok(None)
