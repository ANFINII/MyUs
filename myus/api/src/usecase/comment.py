from dataclasses import replace
from datetime import datetime
from api.modules.logger import log
from api.src.domain.entity.comment.repository import CommentRepository
from api.src.domain.interface.comment.data import CommentData, ReplyData
from api.src.domain.interface.comment.interface import FilterOption, SortOption
from api.src.domain.interface.media.index import ExcludeOption, FilterOption as MediaFilterOption, SortOption as MediaSortOption
from api.src.types.schema.comment import CommentCreateIn
from api.src.usecase.user import get_author_data
from api.utils.enum.index import CommentTypeNo, MediaType
from api.utils.functions.media import get_media_repository


def get_comment_data(comment_ulid: str) -> CommentData | None:
    repository = CommentRepository()
    ids = repository.get_ids(FilterOption(ulid=comment_ulid), SortOption())
    if len(ids) == 0:
        log.warning("コメントが見つかりませんでした")
        return None

    comment = repository.bulk_get(ids)[0]
    return comment


def save_comment_data(data: CommentData) -> bool:
    repository = CommentRepository()
    try:
        repository.bulk_save([data])
        return True
    except Exception as e:
        log.error("save_comment_data error", exc=e)
        return False


def get_comments(type_no: CommentTypeNo, object_id: int, user_id: int | None) -> list[CommentData]:
    comment_repo = CommentRepository()

    parent_ids = comment_repo.get_ids(FilterOption(type_no=type_no, object_id=object_id, is_parent=True), SortOption())
    comments = comment_repo.bulk_get(parent_ids)

    reply_ids = comment_repo.get_ids(FilterOption(type_no=type_no, object_id=object_id, is_parent=False), SortOption())
    replies = comment_repo.bulk_get(reply_ids)

    reply_map: dict[int, list[CommentData]] = {}
    for r in replies:
        if r.parent_id is not None:
            reply_map.setdefault(r.parent_id, []).append(r)

    all_ids = parent_ids + reply_ids
    liked_ids: set[int] = set()
    if user_id is not None:
        liked_ids = set(comment_repo.get_liked_ids(all_ids, user_id))

    data = [
        replace(
            c,
            is_comment_like=c.id in liked_ids,
            author=get_author_data(c.author_id),
            replys=[
                ReplyData(
                    ulid=r.ulid,
                    text=r.text,
                    created=r.created,
                    updated=r.updated,
                    is_comment_like=r.id in liked_ids,
                    like_count=r.like_count,
                    author=get_author_data(r.author_id),
                )
                for r in reply_map.get(c.id, [])
            ],
        ) for c in comments
    ]
    return data


def create_comment(user_id: int, input: CommentCreateIn) -> CommentData | None:
    comment_repo = CommentRepository()
    media_repo = get_media_repository(MediaType(input.type_name.value))

    media_ids = media_repo.get_ids(MediaFilterOption(ulid=input.object_ulid, publish=True), ExcludeOption(), MediaSortOption())
    if len(media_ids) == 0:
        log.warning("メディアが見つかりませんでした")
        return None

    parent_id = None
    if input.parent_ulid:
        parent_ids = comment_repo.get_ids(FilterOption(ulid=input.parent_ulid), SortOption())
        if len(parent_ids) == 0:
            return None

        parent_id = parent_ids[0]

    author = get_author_data(user_id)

    new_comment = CommentData(
        id=0,
        ulid="",
        author_id=user_id,
        parent_id=parent_id,
        type_no=input.type_no,
        type_name=input.type_name,
        object_id=media_ids[0],
        text=input.text,
        deleted=False,
        created=datetime.min,
        updated=datetime.min,
        is_comment_like=False,
        like_count=0,
        author=author,
        replys=[],
    )

    new_ids = comment_repo.bulk_save([new_comment])
    comment = comment_repo.bulk_get(new_ids)[0]

    data = replace(
        comment,
        is_comment_like=False,
        author=author,
        replys=[],
    )

    return data


def update_comment(comment_ulid: str, text: str) -> None:
    comment = get_comment_data(comment_ulid)
    if comment is None:
        return None

    save_comment_data(replace(comment, text=text))
    return None


def delete_comment(comment_ulid: str) -> None:
    comment = get_comment_data(comment_ulid)
    if comment is None:
        return None

    save_comment_data(replace(comment, deleted=True))
    return None
