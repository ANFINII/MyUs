from dataclasses import asdict, dataclass
from enum import Enum
from django.db.models import Exists, OuterRef, Prefetch
from django.utils import timezone
from api.models.comment import Comment
from api.types.data.comment import CommentInData
from api.utils.enum.index import CommentTypeNo


class SortType(Enum):
    CREATED = "created"


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class CommentDomain:
    @classmethod
    def bulk_get(cls, type_no: CommentTypeNo, object_id: int, author_id: int) -> list[Comment]:
        filter_obj = dict(type_no=type_no, object_id=object_id)
        subquery = Comment.objects.filter(id=OuterRef("pk"), like__id=author_id, **filter_obj)
        field_name = SortType.CREATED.value
        order_by_key = field_name if SortOption().is_asc else f'-{field_name}'

        objs = (
            Comment.objects
            .filter(parent__isnull=True, deleted=False, **filter_obj)
            .select_related("author")
            .prefetch_related(Prefetch("reply", queryset=Comment.objects.select_related("author")))
            .annotate(is_comment_like=Exists(subquery))
            .order_by(order_by_key)
        )

        return objs

    @classmethod
    def create(cls, comment_data: CommentInData) -> Comment:
       return Comment.objects.create(**asdict(comment_data))

    @classmethod
    def update(cls, id: int, **kwargs) -> None:
        if not kwargs:
            return
        
        kwargs["updated"] = timezone.now()
        Comment.objects.filter(id=id).update(**kwargs)
