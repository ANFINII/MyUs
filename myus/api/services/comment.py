from api.domain.comment import CommentDomain
from api.types.data.comment.index import CommentData, ReplyData, CommentCreateData
from api.utils.enum.index import CommentTypeNo
from api.utils.functions.user import get_author


def get_comments(type_no: CommentTypeNo, object_id: int, user_id: int | None) -> list[CommentData]:
    objs = CommentDomain.bulk_get(type_no, object_id, user_id)
    data = [
        CommentData(
            ulid=c.ulid,
            text=c.text,
            created=c.created,
            updated=c.updated,
            is_comment_like=c.is_comment_like,
            like_count=c.total_like(),
            author=get_author(c.author),
            replys=[
                ReplyData(
                    id=r.id,
                    text=r.text,
                    created=r.created,
                    updated=r.updated,
                    is_comment_like=r.is_comment_like,
                    like_count=r.total_like(),
                    author=get_author(r.author),
                )
                for r in c.reply.all() if not r.deleted
            ],
        ) for c in objs
    ]
    return data


def create_comment(comment_data: CommentCreateData) -> CommentData:
    obj = CommentDomain.create(comment_data)
    data = CommentData(
        ulid=str(obj.ulid),
        text=obj.text,
        created=obj.created,
        updated=obj.updated,
        is_comment_like=False,
        like_count=obj.total_like(),
        author=get_author(obj.author),
        replys=[],
    )
    return data
