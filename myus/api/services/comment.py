from api.domain.comment import CommentDomain
from api.types.data.comment import CommentData, ReplyData, CommentInData
from api.utils.enum.index import CommentTypeNo
from api.utils.functions.user import get_author


def get_comments(type_no: CommentTypeNo, object_id: int, author_id: int) -> list[CommentData]:
    objs = CommentDomain.bulk_get(type_no, object_id, author_id)
    data = [
        CommentData(
            id=c.id,
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


def create_comment(comment_data: CommentInData) -> CommentData:
    obj = CommentDomain.create(comment_data)
    data = CommentData(
        id=obj.id,
        text=obj.text,
        created=obj.created,
        updated=obj.updated,
        is_comment_like=False,
        like_count=obj.total_like(),
        author=get_author(obj.author),
        replys=[],
    )
    return data
