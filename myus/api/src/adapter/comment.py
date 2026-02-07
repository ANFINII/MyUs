from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.types.schema.comment import CommentCreateIn, CommentListIn, CommentOut, CommentUpdateIn, ReplyOut
from api.src.types.schema.common import ErrorOut, MessageOut
from api.src.types.schema.user import AuthorOut
from api.src.usecase.auth import auth_check
from api.src.usecase.comment import create_comment, delete_comment, get_comments, update_comment


class CommentAPI:
    """コメントAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: list[CommentOut], 401: ErrorOut})
    def get(request: HttpRequest, query: CommentListIn):
        log.info("CommentAPI get", type_no=query.type_no, object_id=query.object_id)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        comments = get_comments(type_no=query.type_no, object_id=query.object_id, user_id=user_id)
        data = [
            CommentOut(
                ulid=x.ulid,
                text=x.text,
                created=x.created,
                updated=x.updated,
                is_comment_like=x.is_comment_like,
                like_count=x.like_count,
                author=AuthorOut(
                    avatar=x.author.avatar,
                    ulid=x.author.ulid,
                    nickname=x.author.nickname,
                    follower_count=x.author.follower_count,
                ),
                replys=[
                    ReplyOut(
                        ulid=r.ulid,
                        text=r.text,
                        created=r.created,
                        updated=r.updated,
                        is_comment_like=r.is_comment_like,
                        like_count=r.like_count,
                        author=AuthorOut(
                            avatar=r.author.avatar,
                            ulid=r.author.ulid,
                            nickname=r.author.nickname,
                            follower_count=r.author.follower_count,
                        ),
                    )
                    for r in x.replys
                ],
            )
            for x in comments
        ]

        return 200, data

    @staticmethod
    @router.post("", response={201: CommentOut, 400: MessageOut, 401: ErrorOut, 500: ErrorOut})
    def post(request: HttpRequest, input: CommentCreateIn):
        log.info("CommentAPI post", input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        try:
            comment = create_comment(user_id, input)
            if comment is None:
                return 400, MessageOut(error=True, message="コメントの作成に失敗しました")

            data = CommentOut(
                ulid=comment.ulid,
                text=comment.text,
                created=comment.created,
                updated=comment.updated,
                is_comment_like=comment.is_comment_like,
                like_count=comment.like_count,
                author=AuthorOut(
                    avatar=comment.author.avatar,
                    ulid=comment.author.ulid,
                    nickname=comment.author.nickname,
                    follower_count=comment.author.follower_count,
                ),
                replys=[],
            )

            return 201, data
        except Exception as e:
            log.error("CommentAPI post error", exc=e)
            return 500, MessageOut(error=True, message="コメントの作成に失敗しました")

    @staticmethod
    @router.put("/{comment_ulid}", response={200: MessageOut, 400: MessageOut, 401: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, comment_ulid: str, input: CommentUpdateIn):
        log.info("CommentAPI put", comment_ulid=comment_ulid, input=input)

        if auth_check(request) is None:
            return 401, ErrorOut(message="Unauthorized")

        try:
            update_comment(comment_ulid, input.text)
            return 200, MessageOut(error=False, message="コメントを更新しました")
        except Exception as e:
            log.error("CommentAPI put error", exc=e)
            return 500, MessageOut(error=True, message="コメントの更新に失敗しました")

    @staticmethod
    @router.delete("/{comment_ulid}", response={200: MessageOut, 400: MessageOut, 401: ErrorOut, 500: ErrorOut})
    def delete(request: HttpRequest, comment_ulid: str):
        log.info("CommentAPI delete", comment_ulid=comment_ulid)

        if auth_check(request) is None:
            return 401, ErrorOut(message="Unauthorized")

        try:
            delete_comment(comment_ulid)
            return 200, MessageOut(error=False, message="コメントを削除しました")
        except Exception as e:
            log.error("CommentAPI delete error", exc=e)
            return 500, MessageOut(error=True, message="コメントの削除に失敗しました")
