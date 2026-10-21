from typing import assert_never
from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.adapter._auth import auth_check
from api.src.types.schema.common import ErrorOut, ErrorType, SuccessOut
from api.src.types.schema.message import MessageOut, MessageReplyOut, MessageCreateIn, MessageUpdateIn
from api.src.types.schema.user import AuthorOut
from api.src.usecase.broadcast import broadcast_create_message, broadcast_delete_message, broadcast_update_message
from api.src.usecase.message import create_message, delete_message, get_replies, update_message
from api.utils.common.result import FatalError, ForbiddenError, NotFoundError


class MessageAPI:
    """メッセージAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={200: MessageOut, 400: ErrorOut, 500: ErrorOut})
    def post(request: HttpRequest, input: MessageCreateIn):
        log.info("MessageAPI post", input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        message_ret = create_message(user_id, input.chat_ulid, input.text, input.parent_ulid)
        if message_ret.is_err:
            message = message_ret.err_value.message
            match message_ret.err_value:
                case NotFoundError():
                    return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
                case FatalError():
                    return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
                case _:
                    assert_never(message_ret.err_value)

        obj = message_ret.ok_value
        data = MessageOut(
            ulid=obj.ulid,
            text=obj.text,
            reply_count=0,
            created=obj.created,
            updated=obj.updated,
            author=AuthorOut(
                avatar=obj.author.avatar,
                ulid=obj.author.ulid,
                nickname=obj.author.nickname,
                follower_count=obj.author.follower_count,
            ),
        )

        broadcast_create_message(input.chat_ulid, obj, input.parent_ulid)

        return 200, data

    @staticmethod
    @router.get("/{message_ulid}", response={200: list[MessageReplyOut], 400: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest, message_ulid: str):
        log.info("MessageAPI get", message_ulid=message_ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        replies_ret = get_replies(message_ulid)
        if replies_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        replies = replies_ret.ok_value
        data = [
            MessageReplyOut(
                ulid=r.ulid,
                parent_id=r.parent_id,
                text=r.text,
                created=r.created,
                updated=r.updated,
                author=AuthorOut(
                    avatar=r.author.avatar,
                    ulid=r.author.ulid,
                    nickname=r.author.nickname,
                    follower_count=r.author.follower_count,
                ),
            )
            for r in replies
        ]

        return 200, data

    @staticmethod
    @router.put("/{message_ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, message_ulid: str, input: MessageUpdateIn):
        log.info("MessageAPI put", message_ulid=message_ulid, input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        update_ret = update_message(user_id, message_ulid, input.text)
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

        chat_ulid = update_ret.ok_value
        broadcast_update_message(chat_ulid, message_ulid, input.text)

        return 200, SuccessOut(message="メッセージを更新しました")

    @staticmethod
    @router.delete("/{message_ulid}", response={200: SuccessOut, 400: ErrorOut, 500: ErrorOut})
    def delete(request: HttpRequest, message_ulid: str):
        log.info("MessageAPI delete", message_ulid=message_ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 400, ErrorOut(type=ErrorType.UNAUTHENTICATED, message="Unauthorized")

        delete_ret = delete_message(user_id, message_ulid)
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

        chat_ulid = delete_ret.ok_value
        broadcast_delete_message(chat_ulid, message_ulid)

        return 200, SuccessOut(message="メッセージを削除しました")
