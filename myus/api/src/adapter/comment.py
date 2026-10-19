from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.types.schema.comment import CommentCreateIn, CommentListIn, CommentOut, CommentUpdateIn, ReplyOut
from api.src.types.schema.common import ErrorOut
from api.src.types.schema.user import AuthorOut
from api.src.usecase.auth import auth_check
from api.src.usecase.comment import create_comment, delete_comment, get_comments, update_comment
from api.utils.common.result import FatalError


class CommentAPI:
    """コメントAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: list[CommentOut], 401: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest, input: CommentListIn):
        log.info("CommentAPI get", type_no=input.type_no, object_id=input.object_id)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        comments_ret = get_comments(type_no=input.type_no, object_id=input.object_id, user_id=user_id)
        if comments_ret.is_err:
            return 500, ErrorOut(message="Internal Server Error")

        comments = comments_ret.ok_value
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
    @router.post("", response={201: CommentOut, 400: ErrorOut, 401: ErrorOut, 500: ErrorOut})
    def post(request: HttpRequest, input: CommentCreateIn):
        log.info("CommentAPI post", input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        try:
            comment_ret = create_comment(user_id, input)
            if comment_ret.is_err:
                if isinstance(comment_ret.err_value, FatalError):
                    return 500, ErrorOut(message="Internal Server Error")
                return 400, ErrorOut(message=comment_ret.err_value.error_message)

            comment = comment_ret.ok_value
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
            return 500, ErrorOut(message="コメントの作成に失敗しました")

    @staticmethod
    @router.put("/{comment_ulid}", response={200: ErrorOut, 400: ErrorOut, 401: ErrorOut, 403: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, comment_ulid: str, input: CommentUpdateIn):
        log.info("CommentAPI put", comment_ulid=comment_ulid, input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        try:
            update_ret = update_comment(user_id, comment_ulid, input.text)
            if update_ret.is_err:
                if isinstance(update_ret.err_value, FatalError):
                    return 500, ErrorOut(message="Internal Server Error")
                return 403, ErrorOut(message=update_ret.err_value.error_message)

            return 200, ErrorOut(message="コメントを更新しました")
        except Exception as e:
            log.error("CommentAPI put error", exc=e)
            return 500, ErrorOut(message="コメントの更新に失敗しました")

    @staticmethod
    @router.delete("/{comment_ulid}", response={200: ErrorOut, 400: ErrorOut, 401: ErrorOut, 403: ErrorOut, 500: ErrorOut})
    def delete(request: HttpRequest, comment_ulid: str):
        log.info("CommentAPI delete", comment_ulid=comment_ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        try:
            delete_ret = delete_comment(user_id, comment_ulid)
            if delete_ret.is_err:
                if isinstance(delete_ret.err_value, FatalError):
                    return 500, ErrorOut(message="Internal Server Error")
                return 403, ErrorOut(message=delete_ret.err_value.error_message)

            return 200, ErrorOut(message="コメントを削除しました")
        except Exception as e:
            log.error("CommentAPI delete error", exc=e)
            return 500, ErrorOut(message="コメントの削除に失敗しました")
