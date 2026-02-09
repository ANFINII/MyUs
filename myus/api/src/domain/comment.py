from dataclasses import dataclass
from enum import Enum
from django.db.models import BooleanField, Count, Exists, OuterRef, Prefetch, Q, Value
from django.db.models.expressions import BaseExpression
from api.db.models.comment import Comment
from api.src.domain.index import sort_ids
from api.utils.enum.index import CommentTypeNo


class SortType(Enum):
    CREATED = "created"


@dataclass(frozen=True, slots=True)
class FilterOption:
    ulid: str = ""
    type_no: CommentTypeNo | None = None
    object_id: int = 0
    user_id: int | None = None
    is_parent: bool | None = None


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


COMMENT_FIELDS = ["author_id", "parent_id", "type_no", "type_name", "object_id", "text", "deleted"]


class CommentDomain:
    @classmethod
    def queryset(cls):
        qs = Comment.objects.annotate(reply_count=Count("reply", filter=Q(reply__deleted=False)))
        return qs.select_related("author", "parent").prefetch_related("like")

    @classmethod
    def get_ids(cls, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.type_no:
            q_list.append(Q(type_no=filter.type_no))
        if filter.object_id:
            q_list.append(Q(object_id=filter.object_id))
        if filter.is_parent:
            q_list.append(Q(parent__isnull=filter.is_parent))

        field_name = sort.sort_type.value
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = Comment.objects.filter(deleted=False, *q_list).order_by(order_by_key)

        if limit:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    @classmethod
    def bulk_get(cls, ids: list[int], user_id: int | None = None) -> list[Comment]:
        if len(ids) == 0:
            return []

        field_name = SortType.CREATED.value
        order_by_key = f"-{field_name}"

        is_comment_like: BaseExpression
        if user_id is None:
            is_comment_like = Value(False, output_field=BooleanField())
        else:
            subquery = Comment.objects.filter(pk=OuterRef("pk"), like__id=user_id)
            is_comment_like = Exists(subquery)

        reply_qs = (
            cls.queryset()
            .filter(deleted=False)
            .annotate(is_comment_like=is_comment_like)
            .order_by(order_by_key)
        )

        objs = (
            cls.queryset()
            .filter(id__in=ids)
            .annotate(is_comment_like=is_comment_like)
            .prefetch_related(Prefetch("reply", queryset=reply_qs))
        )

        return sort_ids(objs, ids)

    @classmethod
    def bulk_save(cls, objs: list[Comment]) -> list[Comment]:
        if len(objs) == 0:
            return []

        Comment.objects.bulk_create(
            objs,
            update_conflicts=True,
            update_fields=COMMENT_FIELDS,
        )

        return cls.bulk_get([o.id for o in objs])
