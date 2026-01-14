from dataclasses import asdict
from api.db.models.comment import Comment
from api.db.models.user import User
from api.modules.logger import log
from api.src.domain.comment import CommentDomain, FilterOption as CommentFilterOption, SortOption as CommentSortOption
from api.src.domain.media.blog import BlogDomain
from api.src.domain.media.index import FilterOption as MediaFilterOption, SortOption as MediaSortOption, ExcludeOption
from api.src.types.data.comment import CommentData, ReplyData, CommentCreateData
from api.src.types.schema.comment import CommentCreateIn
from api.utils.enum.index import CommentTypeNo
from api.utils.functions.user import get_author


def get_comments(type_no: CommentTypeNo, object_id: int, user_id: int | None) -> list[CommentData]:
    filter_option = CommentFilterOption(type_no=type_no, object_id=object_id, user_id=user_id)
    ids = CommentDomain.get_ids(filter_option, CommentSortOption())
    objs = CommentDomain.bulk_get(ids, user_id)
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


def create_comment(user: User, input: CommentCreateIn) -> CommentData | None:
    media_ids = BlogDomain.get_ids(MediaFilterOption(ulid=input.object_ulid, publish=True), ExcludeOption(), MediaSortOption())
    if len(media_ids) == 0:
        log.warning("メディアが見つかりませんでした")
        return None

    media = BlogDomain.bulk_get(media_ids)[0]
    parent_id = None
    if input.parent_ulid:
        ids = CommentDomain.get_ids(CommentFilterOption(ulid=input.parent_ulid), CommentSortOption())
        if len(ids) == 0:
            log.warning("親コメントが見つかりませんでした")
            return None

        comment = CommentDomain.bulk_get(ids)[0]
        parent_id = comment.id

    comment_create_data = CommentCreateData(
        author_id=user.id,
        text=input.text,
        type_no=input.type_no,
        type_name=input.type_name,
        object_id=media.id,
        parent_id=parent_id,
    )

    obj = CommentDomain.create(**asdict(comment_create_data))
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


def update_comment(comment_ulid: str, text: str) -> None:
    ids = CommentDomain.get_ids(CommentFilterOption(ulid=comment_ulid), CommentSortOption())
    if len(ids) == 0:
        log.warning("コメントが見つかりませんでした")
        return None

    comment = CommentDomain.bulk_get(ids)[0]
    CommentDomain.update(comment, text=text)
    return None


def delete_comment(comment_ulid: str) -> None:
    filter_option = CommentFilterOption(ulid=comment_ulid)
    ids = CommentDomain.get_ids(filter_option, CommentSortOption())
    if not ids:
        log.warning("コメントが見つかりませんでした")
        return None

    comment = CommentDomain.bulk_get(ids)[0]
    CommentDomain.update(comment, deleted=True)
    return None
