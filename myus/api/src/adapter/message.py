from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.types.schema.common import ErrorOut
from api.src.types.schema.message import MessageOut, MessageReplyOut, MessageCreateIn, MessageUpdateIn
from api.src.types.schema.user import AuthorOut
from api.src.usecase.auth import auth_check
from api.src.usecase.broadcast import broadcast_create_message, broadcast_delete_message, broadcast_update_message
from api.src.usecase.message import create_message, delete_message, get_replies, update_message
from api.utils.common.result import FatalError


class MessageAPI:
    """メッセージAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={201: MessageOut, 400: ErrorOut, 401: ErrorOut, 500: ErrorOut})
    def post(request: HttpRequest, input: MessageCreateIn):
        log.info("MessageAPI post", input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(message="サーバーエラーが発生しました")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        try:
            message_ret = create_message(user_id, input.chat_ulid, input.text, input.parent_ulid)
            if message_ret.is_err:
                if isinstance(message_ret.err_value, FatalError):
                    return 500, ErrorOut(message="サーバーエラーが発生しました")
                return 400, ErrorOut(message=message_ret.err_value.error_message)

            message = message_ret.ok_value
            data = MessageOut(
                ulid=message.ulid,
                text=message.text,
                reply_count=0,
                created=message.created,
                updated=message.updated,
                author=AuthorOut(
                    avatar=message.author.avatar,
                    ulid=message.author.ulid,
                    nickname=message.author.nickname,
                    follower_count=message.author.follower_count,
                ),
            )

            broadcast_create_message(input.chat_ulid, message, input.parent_ulid)

            return 201, data
        except Exception as e:
            log.error("MessageAPI post error", exc=e)
            return 500, ErrorOut(message="メッセージの作成に失敗しました")

    @staticmethod
    @router.get("/{message_ulid}", response={200: list[MessageReplyOut], 401: ErrorOut, 500: ErrorOut})
    def get(request: HttpRequest, message_ulid: str):
        log.info("MessageAPI get", message_ulid=message_ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(message="サーバーエラーが発生しました")

        if user_id_ret.ok_value is None:
            return 401, ErrorOut(message="Unauthorized")

        replies_ret = get_replies(message_ulid)
        if replies_ret.is_err:
            return 500, ErrorOut(message="サーバーエラーが発生しました")

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
    @router.put("/{message_ulid}", response={200: ErrorOut, 400: ErrorOut, 401: ErrorOut, 403: ErrorOut, 500: ErrorOut})
    def put(request: HttpRequest, message_ulid: str, input: MessageUpdateIn):
        log.info("MessageAPI put", message_ulid=message_ulid, input=input)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(message="サーバーエラーが発生しました")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        try:
            update_ret = update_message(user_id, message_ulid, input.text)
            if update_ret.is_err:
                if isinstance(update_ret.err_value, FatalError):
                    return 500, ErrorOut(message="サーバーエラーが発生しました")
                return 403, ErrorOut(message=update_ret.err_value.error_message)

            broadcast_update_message(input.chat_ulid, message_ulid, input.text)

            return 200, ErrorOut(message="メッセージを更新しました")
        except Exception as e:
            log.error("MessageAPI put error", exc=e)
            return 500, ErrorOut(message="メッセージの更新に失敗しました")

    @staticmethod
    @router.delete("/{message_ulid}", response={200: ErrorOut, 400: ErrorOut, 401: ErrorOut, 403: ErrorOut, 500: ErrorOut})
    def delete(request: HttpRequest, message_ulid: str):
        log.info("MessageAPI delete", message_ulid=message_ulid)

        user_id_ret = auth_check(request)
        if user_id_ret.is_err:
            return 500, ErrorOut(message="サーバーエラーが発生しました")

        user_id = user_id_ret.ok_value
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        try:
            delete_ret = delete_message(user_id, message_ulid)
            if delete_ret.is_err:
                if isinstance(delete_ret.err_value, FatalError):
                    return 500, ErrorOut(message="サーバーエラーが発生しました")
                return 403, ErrorOut(message=delete_ret.err_value.error_message)

            broadcast_delete_message(delete_ret.ok_value, message_ulid)

            return 200, ErrorOut(message="メッセージを削除しました")
        except Exception as e:
            log.error("MessageAPI delete error", exc=e)
            return 500, ErrorOut(message="メッセージの削除に失敗しました")
