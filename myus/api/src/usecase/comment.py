from dataclasses import replace
from datetime import datetime
from api.modules.logger import log
from api.src.domain.interface.comment.data import CommentData
from api.src.domain.interface.comment.interface import CommentInterface, FilterOption, SortOption
from api.src.domain.interface.media.index import ExcludeOption, FilterOption as MediaFilterOption, SortOption as MediaSortOption
from api.src.domain.interface.user.interface import UserInterface
from api.src.injectors.container import injector
from api.src.types.dto.comment import CommentDTO, ReplyDTO
from api.src.types.dto.user import AuthorDTO
from api.src.types.schema.comment import CommentCreateIn
from api.src.usecase.user import get_author_data
from api.utils.enum.index import CommentTypeNo, MediaType
from api.utils.functions.index import create_url
from api.utils.functions.media import get_media_repository


def get_comment_data(comment_ulid: str) -> CommentData | None:
    repository = injector.get(CommentInterface)
    ids = repository.get_ids(FilterOption(ulid=comment_ulid), SortOption())
    if len(ids) == 0:
        log.warning("コメントが見つかりませんでした")
        return None

    comment = repository.bulk_get(ids)[0]
    return comment


def save_comment_data(data: CommentData) -> bool:
    repository = injector.get(CommentInterface)
    try:
        repository.bulk_save([data])
        return True
    except Exception as e:
        log.error("save_comment_data error", exc=e)
        return False


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


def get_comments(type_no: CommentTypeNo, object_id: int, user_id: int | None) -> list[CommentDTO]:
    comment_repo = injector.get(CommentInterface)
    ids = comment_repo.get_ids(FilterOption(type_no=type_no, object_id=object_id), SortOption())
    all_comments = comment_repo.bulk_get(ids)

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
        liked_ids = set(comment_repo.get_liked_ids(ids, user_id))

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
    return data


def create_comment(user_id: int, input: CommentCreateIn) -> CommentDTO | None:
    comment_repo = injector.get(CommentInterface)
    media_repo = get_media_repository(MediaType(input.type_name.value))
    media_ids = media_repo.get_ids(MediaFilterOption(ulid=input.object_ulid, publish=True), ExcludeOption(), MediaSortOption())
    if len(media_ids) == 0:
        log.warning("メディアが見つかりませんでした")
        return None

    parent_id = None
    if input.parent_ulid:
        parent_ids = comment_repo.get_ids(FilterOption(ulid=input.parent_ulid, is_parent=True), SortOption())
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
        like_count=0,
    )

    new_ids = comment_repo.bulk_save([new_comment])
    comments = comment_repo.bulk_get(new_ids)
    assert len(comments) > 0, "コメントの作成に失敗しました"
    comment = comments[0]

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

    return data


def update_comment(comment_ulid: str, text: str) -> None:
    comment = get_comment_data(comment_ulid)
    if comment is None:
        return

    save_comment_data(replace(comment, text=text))


def delete_comment(comment_ulid: str) -> None:
    comment = get_comment_data(comment_ulid)
    if comment is None:
        return

    save_comment_data(replace(comment, deleted=True))
