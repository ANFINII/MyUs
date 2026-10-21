from typing import assert_never
from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.adapter._auth import auth_check
from api.src.types.schema.comment import CommentCreateIn, CommentOut, CommentUpdateIn, ReplyOut
from api.src.types.schema.common import ErrorOut, ErrorType, SuccessOut
from api.src.types.schema.user import AuthorOut
from api.src.usecase.comment import create_comment, delete_comment, update_comment
from api.utils.common.result import FatalError, ForbiddenError, NotFoundError


class CommentAPI:
    """コメントAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={200: CommentOut, 400: ErrorOut, 500: ErrorOut})
    def post(request: HttpRequest, input: CommentCreateIn):
        log.info("CommentAPI post", input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        comment_ret = create_comment(user_id, input)
        if comment_ret.is_err:
            message = comment_ret.err_value.message
            match comment_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(comment_ret.err_value)

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

        return 200, data

    @staticmethod
    @router.put("/{comment_ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, comment_ulid: str, input: CommentUpdateIn):
        log.info("CommentAPI put", comment_ulid=comment_ulid, input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        update_ret = update_comment(user_id, comment_ulid, input.text)
        if update_ret.is_err:
            message = update_ret.err_value.message
            match update_ret.err_value:
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(update_ret.err_value)

        return 200, SuccessOut(message="コメントを更新しました")

    @staticmethod
    @router.delete("/{comment_ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def delete(request: HttpRequest, comment_ulid: str):
        log.info("CommentAPI delete", comment_ulid=comment_ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        delete_ret = delete_comment(user_id, comment_ulid)
        if delete_ret.is_err:
            message = delete_ret.err_value.message
            match delete_ret.err_value:
                case ForbiddenError():
                    return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(delete_ret.err_value)

        return 200, SuccessOut(message="コメントを削除しました")
