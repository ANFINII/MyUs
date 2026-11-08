from dataclasses import replace
from api.modules.logger import log
from api.src.domain.interface.comment.data import CommentData
from api.src.domain.interface.comment.interface import CommentInterface, FilterOption, SortOption
from api.src.injectors.container import injector
from api.src.types.dto.comment import CommentDTO, ReplyDTO
from api.src.usecase.notification._convert import delete_notification_data
from api.src.usecase.user._convert import get_author_map_data
from api.utils.common.result import FatalError, Result
from api.utils.enum.media import CommentTypeNo
from api.utils.enum.notification import NotificationObjectType


@Result.shield_exception()
def get_comment_data(comment_ulid: str) -> Result[CommentData | None, FatalError]:
    repo = injector.get(CommentInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=comment_ulid), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("コメントが見つかりませんでした")
        return Result.ok(None)

    comments_ret = repo.bulk_get(ids)
    if comments_ret.is_err:
        return Result.err(comments_ret.err_value)

    comments = comments_ret.ok_value
    return Result.ok(comments[0])


@Result.shield_exception()
def save_comment_data(data: CommentData) -> Result[None, FatalError]:
    repo = injector.get(CommentInterface)
    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_comment_data(data: CommentData) -> Result[None, FatalError]:
    repo = injector.get(CommentInterface)
    save_ret = repo.bulk_save([replace(data, deleted=True)])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    notification_ret = delete_notification_data(NotificationObjectType.COMMENT, [data.id])
    if notification_ret.is_err:
        return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_comments_data(type_no: CommentTypeNo, object_id: int, user_id: int | None) -> Result[list[CommentDTO], FatalError]:
    repo = injector.get(CommentInterface)
    ids_ret = repo.get_ids(FilterOption(type_no=type_no, object_id=object_id), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    all_comments_ret = repo.bulk_get(ids)
    if all_comments_ret.is_err:
        return Result.err(all_comments_ret.err_value)

    all_comments = all_comments_ret.ok_value
    comments = [c for c in all_comments if c.parent_id is None]
    replies = [c for c in all_comments if c.parent_id is not None]
    author_ids = list({c.author_id for c in comments} | {r.author_id for r in replies})
    author_map_ret = get_author_map_data(author_ids)
    if author_map_ret.is_err:
        return Result.err(author_map_ret.err_value)

    author_map = author_map_ret.ok_value

    reply_map: dict[int, list[CommentData]] = {}
    for r in replies:
        if r.parent_id is not None:
            reply_map.setdefault(r.parent_id, []).append(r)

    liked_ids: set[int] = set()
    if user_id is not None:
        liked_ids_ret = repo.get_liked_ids(ids, user_id)
        if liked_ids_ret.is_err:
            return Result.err(liked_ids_ret.err_value)

        liked_comment_ids = liked_ids_ret.ok_value
        liked_ids = set(liked_comment_ids)

    data = [
        CommentDTO(
            ulid=c.ulid,
            text=c.text,
            created=c.created,
            updated=c.updated,
            is_comment_like=c.id in liked_ids,
            like_count=c.like_count,
            author=author_map[c.author_id],
            replys=[
                ReplyDTO(
                    ulid=r.ulid,
                    text=r.text,
                    created=r.created,
                    updated=r.updated,
                    is_comment_like=r.id in liked_ids,
                    like_count=r.like_count,
                    author=author_map[r.author_id],
                )
                for r in reply_map.get(c.id, [])
            ],
        ) for c in comments
    ]
    return Result.ok(data)
