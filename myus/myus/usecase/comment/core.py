from dataclasses import replace
from datetime import datetime
from myus.domain.comment.data import CommentData
from myus.domain.comment.interface import CommentInterface, FilterOption, SortOption
from myus.domain.common import ExcludeOption, FilterOption as MediaFilterOption, PageOption, SortOption as MediaSortOption
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import AccessError, FindError, ForbiddenError, NotFoundError, Result
from myus.utils.enum.media import MediaType
from myus.utils.enum.notification import NotificationObjectType, NotificationTypeNo
from myus.utils.functions.map import comment_type_no_map
from myus.utils.functions.transaction import atomic_result
from ._convert import get_comment_data, save_comment_data, delete_comment_data
from ..dto.comment import CommentCreateDTO, CommentDTO
from ..media._convert import get_media_repository
from ..notification._convert import create_notification_data
from ..user._convert import get_author_data


@Result.shield_exception()
def create_comment(user_id: int, input: CommentCreateDTO) -> Result[CommentDTO, FindError]:
    repo = injector.get(CommentInterface)
    media_repo = get_media_repository(MediaType(input.type_name.value))
    media_ids_ret = media_repo.get_ids(MediaFilterOption(ulid=input.object_ulid, publish=True), ExcludeOption(), MediaSortOption(), PageOption())
    if media_ids_ret.is_err:
        return Result.err(media_ids_ret.err_value)

    media_ids = media_ids_ret.ok_value
    if len(media_ids) == 0:
        log.warning("メディアが見つかりませんでした")
        return Result.err(NotFoundError("error.commentCreateFailed"))

    type_no = comment_type_no_map(input.type_name)
    parent: CommentData | None = None
    if input.parent_ulid:
        parent_ids_ret = repo.get_ids(FilterOption(ulid=input.parent_ulid, type_no=type_no, object_id=media_ids[0], is_parent=True), SortOption())
        if parent_ids_ret.is_err:
            return Result.err(parent_ids_ret.err_value)

        parent_ids = parent_ids_ret.ok_value
        if len(parent_ids) == 0:
            return Result.err(NotFoundError("error.commentCreateFailed"))

        parents_ret = repo.bulk_get(parent_ids)
        if parents_ret.is_err:
            return Result.err(parents_ret.err_value)

        parents = parents_ret.ok_value
        parent = parents[0]

    author_ret = get_author_data(user_id)
    if author_ret.is_err:
        return Result.err(author_ret.err_value)

    author = author_ret.ok_value
    new_comment = CommentData(
        id=0,
        ulid="",
        author_id=user_id,
        parent_id=parent.id if parent is not None else None,
        type_no=type_no,
        type_name=input.type_name,
        object_id=media_ids[0],
        text=input.text,
        deleted=False,
        created=datetime.min,
        updated=datetime.min,
        like_count=0,
    )

    new_ids_ret = repo.bulk_save([new_comment])
    if new_ids_ret.is_err:
        return Result.err(new_ids_ret.err_value)

    new_ids = new_ids_ret.ok_value
    comments_ret = repo.bulk_get(new_ids)
    if comments_ret.is_err:
        return Result.err(comments_ret.err_value)

    comments = comments_ret.ok_value
    assert len(comments) > 0, "error.commentCreateFailed"
    comment = comments[0]

    if parent is not None:
        notification_ret = create_notification_data(user_id, parent.author_id, NotificationTypeNo.REPLY, comment.id, NotificationObjectType.COMMENT)
        if notification_ret.is_err:
            log.error("通知の作成に失敗しました", error=notification_ret.err_value.message, comment_id=comment.id)

    data = CommentDTO(
        ulid=comment.ulid,
        text=comment.text,
        created=comment.created,
        updated=comment.updated,
        is_comment_like=False,
        like_count=comment.like_count,
        author=author,
        replys=[],
    )

    return Result.ok(data)


@Result.shield_exception()
def update_comment(user_id: int, comment_ulid: str, text: str) -> Result[None, AccessError]:
    comment_ret = get_comment_data(comment_ulid)
    if comment_ret.is_err:
        return Result.err(comment_ret.err_value)

    comment = comment_ret.ok_value
    if comment is None:
        return Result.err(NotFoundError("Not Found"))

    if comment.author_id != user_id:
        log.warning("コメントの編集権限がありません", comment_ulid=comment_ulid, user_id=user_id)
        return Result.err(ForbiddenError("Forbidden"))

    save_ret = save_comment_data(replace(comment, text=text))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_comment(user_id: int, comment_ulid: str) -> Result[None, AccessError]:
    comment_ret = get_comment_data(comment_ulid)
    if comment_ret.is_err:
        return Result.err(comment_ret.err_value)

    comment = comment_ret.ok_value
    if comment is None:
        return Result.err(NotFoundError("Not Found"))

    if comment.author_id != user_id:
        log.warning("コメントの削除権限がありません", comment_ulid=comment_ulid, user_id=user_id)
        return Result.err(ForbiddenError("Forbidden"))

    delete_ret = atomic_result(lambda: delete_comment_data(comment))
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)
