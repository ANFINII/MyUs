from django.db.models import Count, F
from django.db.models.query import QuerySet
from api.db.models.media import Video
from api.src.domain.entity.media.video._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_save_new_ids, sort_ids
from api.src.domain.entity.media.index import distinct_queryset, filter_q_list, sort_queryset
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption
from api.utils.common.result import FatalError, Result


VIDEO_FIELDS = ["channel_id", "title", "content", "image", "video", "convert", "publish", "publish_at", "updated"]


class VideoRepository(VideoInterface):
    def queryset(self) -> QuerySet[Video]:
        return Video.objects.select_related("channel", "channel__owner").prefetch_related("hashtag", "category").annotate(like_count=Count("like"))

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, page: PageOption, user_id: int | None = None) -> Result[list[int], FatalError]:
        qs = Video.objects.filter(*filter_q_list(filter, exclude))
        qs = distinct_queryset(qs, filter)
        qs, order_by_key = sort_queryset(qs, sort, filter.is_recommend, user_id)
        qs = qs.order_by(order_by_key)
        qs = qs[page.offset:page.offset + page.limit]
        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[VideoData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[VideoData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, VIDEO_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        Video.objects.filter(id__in=ids).delete()
        return Result.ok(None)

    @Result.shield_exception()
    def count(self, filter: FilterOption) -> Result[int, FatalError]:
        qs = Video.objects.filter(*filter_q_list(filter))
        return Result.ok(distinct_queryset(qs, filter).count())

    @Result.shield_exception()
    def is_liked(self, media_id: int, user_id: int) -> Result[bool, FatalError]:
        return Result.ok(Video.objects.filter(id=media_id, like__id=user_id).exists())

    @Result.shield_exception()
    def save_read(self, media_id: int) -> Result[int, FatalError]:
        Video.objects.filter(id=media_id).update(read=F("read") + 1)
        read = Video.objects.filter(id=media_id).values_list("read", flat=True).first()
        return Result.ok(read if read is not None else 0)
