from django.db.models import Count, Q
from django.db.models.query import QuerySet
from api.db.models.comment import Comment
from api.src.domain.entity.comment._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_save_new_ids, sort_ids
from api.src.domain.interface.comment.data import CommentData
from api.src.domain.interface.comment.interface import CommentInterface, FilterOption, SortOption
from api.utils.common.result import FatalError, Result


COMMENT_FIELDS = ["author_id", "parent_id", "type_no", "type_name", "object_id", "text", "deleted", "updated"]


class CommentRepository(CommentInterface):
    def queryset(self) -> QuerySet[Comment]:
        return Comment.objects.select_related("author", "parent").annotate(like_count=Count("like"))

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.type_no is not None:
            q_list.append(Q(type_no=filter.type_no))
        if filter.object_id:
            q_list.append(Q(object_id=filter.object_id))
        if len(filter.object_ids) > 0:
            q_list.append(Q(object_id__in=filter.object_ids))
        if filter.user_id:
            q_list.append(Q(author_id=filter.user_id))
        if filter.is_parent is not None:
            q_list.append(Q(parent__isnull=filter.is_parent))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Comment.objects.filter(deleted=False, *q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[CommentData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[CommentData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        models = [marshal_data(o) for o in objs]
        new_ids = get_save_new_ids(models, COMMENT_FIELDS)

        return Result.ok(new_ids)

    @Result.shield_exception()
    def get_liked_ids(self, ids: list[int], user_id: int) -> Result[list[int], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        liked_ids = set(Comment.objects.filter(id__in=ids, like__id=user_id).values_list("id", flat=True))
        return Result.ok(list(liked_ids))
