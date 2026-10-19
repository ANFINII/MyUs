from dataclasses import replace
from datetime import datetime
from django.db import transaction
from api.modules.logger import log
from api.src.domain.interface.comment.data import CommentData
from api.src.domain.interface.comment.interface import CommentInterface, FilterOption, SortOption
from api.src.domain.interface.media.index import ExcludeOption, FilterOption as MediaFilterOption, PageOption, SortOption as MediaSortOption
from api.src.domain.interface.user.interface import UserInterface
from api.src.injectors.container import injector
from api.src.types.dto.comment import CommentDTO, ReplyDTO
from api.src.types.dto.user import AuthorDTO
from api.src.types.schema.comment import CommentCreateIn
from api.src.usecase.notification import create_notification, delete_object_notifications
from api.src.usecase.user import get_author_data
from api.utils.common.result import FatalError, NotFoundError, Result
from api.utils.enum.media import CommentTypeNo, MediaType
from api.utils.enum.notification import NotificationObjectType, NotificationTypeNo
from api.utils.functions.index import create_url
from api.utils.functions.media import get_media_repository


@Result.shield_exception()
def get_comment_data(comment_ulid: str) -> Result[CommentData | None, FatalError]:
    repository = injector.get(CommentInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=comment_ulid), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("コメントが見つかりませんでした")
        return Result.ok(None)

    comments_ret = repository.bulk_get(ids)
    if comments_ret.is_err:
        return Result.err(comments_ret.err_value)

    return Result.ok(comments_ret.ok_value[0])


@Result.shield_exception()
def save_comment_data(data: CommentData) -> Result[None, FatalError]:
    repository = injector.get(CommentInterface)
    ret = repository.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


def get_author_data_map(ids: list[int]) -> dict[int, AuthorDTO]:
    if len(ids) == 0:
        return {}

    repository = injector.get(UserInterface)
    authors = repository.bulk_get(ids)
    author_map: dict[int, AuthorDTO] = {}
    for author in authors:
        author_map[author.user.id] = AuthorDTO(
            avatar=create_url(author.user.avatar),
            ulid=author.user.ulid,
            nickname=author.user.nickname,
            follower_count=author.mypage.follower_count,
        )

    return author_map


@Result.shield_exception()
def get_comments(type_no: CommentTypeNo, object_id: int, user_id: int | None) -> Result[list[CommentDTO], FatalError]:
    comment_repo = injector.get(CommentInterface)
    ids_ret = comment_repo.get_ids(FilterOption(type_no=type_no, object_id=object_id), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    all_comments_ret = comment_repo.bulk_get(ids)
    if all_comments_ret.is_err:
        return Result.err(all_comments_ret.err_value)

    all_comments = all_comments_ret.ok_value
    comments = [c for c in all_comments if c.parent_id is None]
    replies = [c for c in all_comments if c.parent_id is not None]
    author_ids = list({c.author_id for c in comments} | {r.author_id for r in replies})
    author_map = get_author_data_map(author_ids)

    reply_map: dict[int, list[CommentData]] = {}
    for r in replies:
        if r.parent_id is not None:
            reply_map.setdefault(r.parent_id, []).append(r)

    liked_ids: set[int] = set()
    if user_id is not None:
        liked_ids_ret = comment_repo.get_liked_ids(ids, user_id)
        if liked_ids_ret.is_err:
            return Result.err(liked_ids_ret.err_value)

        liked_ids = set(liked_ids_ret.ok_value)

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


@Result.shield_exception()
def create_comment(user_id: int, input: CommentCreateIn) -> Result[CommentDTO, NotFoundError | FatalError]:
    comment_repo = injector.get(CommentInterface)
    media_repo = get_media_repository(MediaType(input.type_name.value))
    media_ids_ret = media_repo.get_ids(MediaFilterOption(ulid=input.object_ulid, publish=True), ExcludeOption(), MediaSortOption(), PageOption())
    if media_ids_ret.is_err:
        return Result.err(media_ids_ret.err_value)

    media_ids = media_ids_ret.ok_value
    if len(media_ids) == 0:
        log.warning("メディアが見つかりませんでした")
        return Result.err(NotFoundError("コメントの作成に失敗しました"))

    parent: CommentData | None = None
    if input.parent_ulid:
        parent_ids_ret = comment_repo.get_ids(FilterOption(ulid=input.parent_ulid, is_parent=True), SortOption())
        if parent_ids_ret.is_err:
            return Result.err(parent_ids_ret.err_value)

        parent_ids = parent_ids_ret.ok_value
        if len(parent_ids) == 0:
            return Result.err(NotFoundError("コメントの作成に失敗しました"))

        parents_ret = comment_repo.bulk_get(parent_ids)
        if parents_ret.is_err:
            return Result.err(parents_ret.err_value)

        parent = parents_ret.ok_value[0]

    author = get_author_data(user_id)
    new_comment = CommentData(
        id=0,
        ulid="",
        author_id=user_id,
        parent_id=parent.id if parent is not None else None,
        type_no=input.type_no,
        type_name=input.type_name,
        object_id=media_ids[0],
        text=input.text,
        deleted=False,
        created=datetime.min,
        updated=datetime.min,
        like_count=0,
    )

    new_ids_ret = comment_repo.bulk_save([new_comment])
    if new_ids_ret.is_err:
        return Result.err(new_ids_ret.err_value)

    comments_ret = comment_repo.bulk_get(new_ids_ret.ok_value)
    if comments_ret.is_err:
        return Result.err(comments_ret.err_value)

    comments = comments_ret.ok_value
    assert len(comments) > 0, "コメントの作成に失敗しました"
    comment = comments[0]

    if parent is not None:
        notification_ret = create_notification(user_id, parent.author_id, NotificationTypeNo.REPLY, comment.id, NotificationObjectType.COMMENT)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

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
def update_comment(user_id: int, comment_ulid: str, text: str) -> Result[None, NotFoundError | FatalError]:
    comment_ret = get_comment_data(comment_ulid)
    if comment_ret.is_err:
        return Result.err(comment_ret.err_value)

    comment = comment_ret.ok_value
    if comment is None:
        return Result.err(NotFoundError("Forbidden"))

    if comment.author_id != user_id:
        log.warning("コメントの編集権限がありません", comment_ulid=comment_ulid, user_id=user_id)
        return Result.err(NotFoundError("Forbidden"))

    save_ret = save_comment_data(replace(comment, text=text))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_comment(user_id: int, comment_ulid: str) -> Result[None, NotFoundError | FatalError]:
    comment_ret = get_comment_data(comment_ulid)
    if comment_ret.is_err:
        return Result.err(comment_ret.err_value)

    comment = comment_ret.ok_value
    if comment is None:
        return Result.err(NotFoundError("Forbidden"))

    if comment.author_id != user_id:
        log.warning("コメントの削除権限がありません", comment_ulid=comment_ulid, user_id=user_id)
        return Result.err(NotFoundError("Forbidden"))

    repository = injector.get(CommentInterface)
    with transaction.atomic():
        save_ret = repository.bulk_save([replace(comment, deleted=True)])
        if save_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(save_ret.err_value)

        notification_ret = delete_object_notifications(NotificationObjectType.COMMENT, [comment.id])
        if notification_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(notification_ret.err_value)

    return Result.ok(None)
