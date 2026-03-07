from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.comment import Comment
from api.src.domain.entity.comment._convert import convert_data, marshal_data
from api.src.domain.entity.index import get_new_ids, sort_ids
from api.src.domain.interface.comment.data import CommentData
from api.src.domain.interface.comment.interface import CommentInterface, FilterOption, SortOption


COMMENT_FIELDS = ["author_id", "parent_id", "type_no", "type_name", "object_id", "text", "deleted"]


class CommentRepository(CommentInterface):
    def queryset(self) -> QuerySet[Comment]:
        return Comment.objects.prefetch_related("like")

    def get_ids(self, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.type_no is not None:
            q_list.append(Q(type_no=filter.type_no))
        if filter.object_id:
            q_list.append(Q(object_id=filter.object_id))
        if filter.user_id:
            q_list.append(Q(author_id=filter.user_id))
        if filter.is_parent:
            q_list.append(Q(parent__isnull=filter.is_parent))

        field_name = sort.sort_type.name.lower()
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Comment.objects.filter(deleted=False, *q_list).order_by(order_by_key)

        if limit is not None:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[CommentData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[CommentData]) -> list[int]:
        if len(objs) == 0:
            return []

        models = [marshal_data(o) for o in objs]
        new_ids = get_new_ids(models, Comment)

        Comment.objects.bulk_create(
            models,
            update_conflicts=True,
            update_fields=COMMENT_FIELDS,
        )

        return new_ids

    def get_liked_ids(self, ids: list[int], user_id: int) -> list[int]:
        if len(ids) == 0:
            return []

        liked_ids = set(Comment.objects.filter(id__in=ids, like__id=user_id).values_list("id", flat=True))
        return list(liked_ids)
