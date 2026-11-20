from django.db.models import Count, F
from django.db.models.query import QuerySet
from myus.db.models.media import Audio
from myus.domain.media.audio.data import AudioData
from myus.domain.media.audio.interface import AudioInterface
from myus.domain.media.audio.validation import validate
from myus.domain.media.common import FilterOption, PageOption, SortOption
from myus.utils.common.result import FatalError, Result
from ._convert import convert_data, marshal_data
from ..common import filter_queryset, get_ids_queryset
from ...common import get_save_new_ids, sort_ids


AUDIO_FIELDS = ["channel_id", "title", "content", "lyric", "image", "audio", "gain", "publish", "publish_at", "updated"]


class AudioRepository(AudioInterface):
    def queryset(self) -> QuerySet[Audio]:
        return Audio.objects.select_related("channel", "channel__owner").prefetch_related("hashtag", "category").annotate(like_count=Count("like"))

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        qs = get_ids_queryset(Audio.objects.all(), filter, sort, page)
        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[AudioData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[AudioData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
        if len(errors) > 0:
            return Result.err(FatalError(f"Invalid Data: {errors}"))

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, AUDIO_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        Audio.objects.filter(id__in=ids).delete()
        return Result.ok(None)

    @Result.shield_exception()
    def count(self, filter: FilterOption) -> Result[int, FatalError]:
        qs = filter_queryset(Audio.objects.all(), filter)
        return Result.ok(qs.count())

    @Result.shield_exception()
    def is_liked(self, media_id: int, user_id: int) -> Result[bool, FatalError]:
        return Result.ok(Audio.objects.filter(id=media_id, like__id=user_id).exists())

    @Result.shield_exception()
    def save_read(self, media_id: int) -> Result[int, FatalError]:
        Audio.objects.filter(id=media_id).update(read=F("read") + 1)
        read = Audio.objects.filter(id=media_id).values_list("read", flat=True).first()
        return Result.ok(read if read is not None else 0)
