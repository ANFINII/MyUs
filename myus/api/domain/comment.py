from dataclasses import asdict, dataclass
from enum import Enum, auto
from django.db.models import Exists, OuterRef, Prefetch
from api.models.comment import Comment
from api.types.data.comment import CommentData, ReplyData, CommentInData
from api.utils.enum.index import CommentTypeNo
from api.utils.functions.user import get_author


class SortType(Enum):
    CREATED = "created"


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class CommentDomain:
    @classmethod
    def get(cls, type_no: CommentTypeNo, object_id: int, author_id: int) -> list[CommentData]:
        filter_obj = dict(type_no=type_no, object_id=object_id)
        subquery = Comment.objects.filter(id=OuterRef("pk"), like__id=author_id, **filter_obj)
        field_name = SortType.CREATED.value
        order_by_key = field_name if SortOption().is_asc else f'-{field_name}'

        objs = (
            Comment.objects
            .filter(parent__isnull=True, **filter_obj)
            .select_related("author")
            .prefetch_related(Prefetch("reply", queryset=Comment.objects.select_related("author")))
            .annotate(is_comment_like=Exists(subquery))
            .order_by(order_by_key)
        )

        return get_comment_data(objs)

    @classmethod
    def create(cls, comment_data: CommentInData) -> CommentData:
        obj = Comment.objects.create(**asdict(comment_data))

        data = CommentData(
            id=obj.id,
            text=obj.text,
            created=obj.created,
            updated=obj.updated,
            replys=[],
            author=get_author(obj.author),
        )
        return data


def get_comment_data(comments: list[Comment]) -> list[CommentData]:
    data = [
        CommentData(
            id=c.id,
            text=c.text,
            created=c.created,
            updated=c.updated,
            replys=[
                ReplyData(id=r.id, text=r.text, created=r.created, updated=r.updated, author=get_author(r.author))
                for r in c.reply.all()
            ],
            author=get_author(c.author),
        ) for c in comments
    ]
    return data
