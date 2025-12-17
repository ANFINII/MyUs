from dataclasses import dataclass
from enum import Enum
from django.db.models import Exists, OuterRef, Prefetch
from django.utils import timezone
from api.db.models.comment import Comment
from api.db.models.user import User
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
    def get(cls, ulid: str) -> Comment | None:
        return Comment.objects.filter(ulid=ulid).first()

    @classmethod
    def bulk_get(cls, type_no: CommentTypeNo, object_id: int, user_id: int | None) -> list[Comment]:
        filter_obj = dict(type_no=type_no, object_id=object_id)
        subquery = Comment.objects.filter(id=OuterRef("pk"), like__id=user_id)
        queryset = Comment.objects.select_related("author").annotate(is_comment_like=Exists(subquery))
        field_name = SortType.CREATED.value
        order_by_key = field_name if SortOption().is_asc else f"-{field_name}"

        objs = (
            Comment.objects
            .filter(parent__isnull=True, deleted=False, **filter_obj)
            .select_related("author")
            .prefetch_related(Prefetch("reply", queryset=queryset))
            .annotate(is_comment_like=Exists(subquery))
            .order_by(order_by_key)
        )

        return list(objs)

    @classmethod
    def create(cls, **kwargs) -> Comment:
       return Comment.objects.create(**kwargs)

    @classmethod
    def update(cls, comment: Comment, **kwargs) -> None:
        if not kwargs:
            return

        kwargs["updated"] = timezone.now
        [set_attr(comment, key, value) for key, value in kwargs.items()]
        comment.save(update_fields=list(kwargs.keys()))

    @classmethod
    def comment_like(cls, model: Comment, user: User) -> bool:
        is_like = model.like.filter(id=user.id).exists()
        if is_like:
            model.like.remove(user)
        else:
            model.like.add(user)
        return not is_like
