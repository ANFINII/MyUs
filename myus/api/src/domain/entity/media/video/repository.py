from django.db.models.query import QuerySet
from api.db.models.media import Video
from api.src.domain.entity.media.video._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.entity.media.index import distinct_queryset, filter_q_list, sort_queryset
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption


VIDEO_FIELDS = ["channel_id", "title", "content", "image", "video", "convert", "read", "publish"]


class VideoRepository(VideoInterface):
    def queryset(self) -> QuerySet[Video]:
        return Video.objects.select_related("channel", "channel__owner").prefetch_related("like", "hashtag", "category")

    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, page: PageOption, user_id: int | None = None) -> list[int]:
        qs = Video.objects.filter(*filter_q_list(filter, exclude))
        qs = distinct_queryset(qs, filter)
        qs, order_by_key = sort_queryset(qs, sort, filter.is_recommend, user_id)
        qs = qs.order_by(order_by_key)
        qs = qs[page.offset:page.offset + page.limit]
        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[VideoData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[VideoData]) -> list[int]:
        if len(objs) == 0:
            return []

        models = [marshal_data(o) for o in objs]
        new_ids = get_new_ids(models, Video)

        Video.objects.bulk_create(
            models,
            update_conflicts=True,
            update_fields=VIDEO_FIELDS,
        )

        return new_ids

    def bulk_delete(self, ids: list[int]) -> None:
        Video.objects.filter(id__in=ids).delete()

    def count(self, filter: FilterOption) -> int:
        qs = Video.objects.filter(*filter_q_list(filter))
        return distinct_queryset(qs, filter).count()

    def is_liked(self, media_id: int, user_id: int) -> bool:
        return Video.objects.filter(id=media_id, like__id=user_id).exists()
