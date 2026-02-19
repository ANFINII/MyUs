from api.db.models.comment import Comment
from api.src.domain.interface.comment.data import CommentData


def convert_data(obj: Comment) -> CommentData:
    return CommentData(
        id=obj.id,
        ulid=obj.ulid,
        author_id=obj.author_id,
        parent_id=obj.parent_id,
        type_no=obj.type_no,
        type_name=obj.type_name,
        object_id=obj.object_id,
        text=obj.text,
        deleted=obj.deleted,
        created=obj.created,
        updated=obj.updated,
        like_count=obj.total_like(),
    )


def marshal_data(data: CommentData) -> Comment:
    comment = Comment(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid,
        author_id=data.author_id,
        parent_id=data.parent_id,
        type_no=data.type_no,
        type_name=data.type_name,
        object_id=data.object_id,
        text=data.text,
    )
    return comment
