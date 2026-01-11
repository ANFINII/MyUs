from dataclasses import dataclass
from enum import Enum
from django.db.models import BooleanField, Count, Exists, OuterRef, Prefetch, Q, Value
from django.db.models.expressions import BaseExpression
from django.utils import timezone
from api.db.models.comment import Comment
from api.utils.enum.index import CommentTypeNo
from api.utils.functions.index import set_attr


class SortType(Enum):
    CREATED = "created"


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class CommentDomain:
    @classmethod
    def queryset(cls):
        qs = Comment.objects.annotate(reply_count=Count("reply", filter=Q(reply__deleted=False)))
        return qs.select_related("author", "parent").prefetch_related("like")

    @classmethod
    def get(cls, ulid: str) -> Comment | None:
        return cls.queryset().filter(ulid=ulid).first()

    @classmethod
    def bulk_get(cls, type_no: CommentTypeNo, object_id: int, user_id: int | None) -> list[Comment]:
        filter_obj = dict(type_no=type_no, object_id=object_id)
        field_name = SortType.CREATED.value
        order_by_key = field_name if SortOption().is_asc else f"-{field_name}"

        is_comment_like: BaseExpression
        if user_id is None:
            is_comment_like = Value(False, output_field=BooleanField())
        else:
            subquery = Comment.objects.filter(pk=OuterRef("pk"), like__id=user_id)
            is_comment_like = Exists(subquery)

        queryset = (
            cls.queryset()
            .filter(deleted=False)
            .annotate(is_comment_like=is_comment_like)
            .order_by(order_by_key)
        )

        objs = (
            cls.queryset()
            .filter(parent__isnull=True, deleted=False, **filter_obj)
            .annotate(is_comment_like=is_comment_like)
            .prefetch_related(Prefetch("reply", queryset=queryset))
            .order_by(order_by_key)
        )

        return list(objs)

    @classmethod
    def create(cls, **kwargs) -> Comment:
        return Comment.objects.create(**kwargs)

    @classmethod
    def update(cls, obj: Comment, **kwargs) -> None:
        if not kwargs:
            return

        kwargs["updated"] = timezone.now
        [set_attr(obj, key, value) for key, value in kwargs.items()]
        obj.save(update_fields=list(kwargs.keys()))
        return
