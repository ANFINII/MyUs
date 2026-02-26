from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.types.schema.common import ErrorOut, MessageOut
from api.src.types.schema.message import ChatMessageOut, ChatMessageReplyOut, MessageCreateIn, MessageUpdateIn
from api.src.types.schema.user import AuthorOut
from api.src.usecase.auth import auth_check
from api.src.usecase.message import create_message, delete_message, get_replies, update_message


class MessageAPI:
    """メッセージAPI"""

    router = Router()

    @staticmethod
    @router.post("", response={201: ChatMessageOut, 400: MessageOut, 401: ErrorOut, 500: MessageOut})
    def post(request: HttpRequest, input: MessageCreateIn):
        log.info("MessageAPI post", input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        try:
            message = create_message(user_id, input.chat_ulid, input.text, input.parent_ulid)
            if message is None:
                return 400, MessageOut(error=True, message="メッセージの作成に失敗しました")

            data = ChatMessageOut(
                ulid=message.ulid,
                text=message.text,
                created=message.created,
                updated=message.updated,
                author=AuthorOut(
                    avatar=message.author.avatar,
                    ulid=message.author.ulid,
                    nickname=message.author.nickname,
                    follower_count=message.author.follower_count,
                ),
            )

            # WebSocket broadcast
            channel_layer = get_channel_layer()
            if channel_layer is not None:
                is_reply = len(input.parent_ulid) > 0
                command = "create_reply_message" if is_reply else "create_message"
                broadcast_message: dict[str, object] = {
                    "ulid": message.ulid,
                    "text": message.text,
                    "created": message.created.isoformat(),
                    "updated": message.updated.isoformat(),
                    "author": {
                        "avatar": message.author.avatar,
                        "ulid": message.author.ulid,
                        "nickname": message.author.nickname,
                        "follower_count": message.author.follower_count,
                    },
                }
                if is_reply:
                    broadcast_message["parent_ulid"] = input.parent_ulid
                async_to_sync(channel_layer.group_send)(
                    f"chat_detail_{input.chat_ulid}",
                    {
                        "type": "chat_message",
                        "message": {
                            "command": command,
                            "message": broadcast_message,
                        },
                    },
                )

            return 201, data
        except Exception as e:
            log.error("MessageAPI post error", exc=e)
            return 500, MessageOut(error=True, message="メッセージの作成に失敗しました")

    @staticmethod
    @router.get("/{message_ulid}", response={200: list[ChatMessageReplyOut], 401: ErrorOut})
    def get(request: HttpRequest, message_ulid: str):
        log.info("MessageAPI get", message_ulid=message_ulid)

        if auth_check(request) is None:
            return 401, ErrorOut(message="Unauthorized")

        replies = get_replies(message_ulid)
        data = [
            ChatMessageReplyOut(
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
    @router.put("/{message_ulid}", response={200: MessageOut, 400: MessageOut, 401: ErrorOut, 403: ErrorOut, 500: MessageOut})
    def put(request: HttpRequest, message_ulid: str, input: MessageUpdateIn):
        log.info("MessageAPI put", message_ulid=message_ulid, input=input)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        try:
            result = update_message(user_id, message_ulid, input.text)
            if result is None:
                return 403, ErrorOut(message="Forbidden")

            channel_layer = get_channel_layer()
            if channel_layer is not None:
                async_to_sync(channel_layer.group_send)(
                    f"chat_detail_{input.chat_ulid}",
                    {
                        "type": "chat_message",
                        "message": {
                            "command": "update_message",
                            "message": {
                                "ulid": message_ulid,
                                "text": input.text,
                            },
                        },
                    },
                )

            return 200, MessageOut(error=False, message="メッセージを更新しました")
        except Exception as e:
            log.error("MessageAPI put error", exc=e)
            return 500, MessageOut(error=True, message="メッセージの更新に失敗しました")

    @staticmethod
    @router.delete("/{message_ulid}", response={200: MessageOut, 400: MessageOut, 401: ErrorOut, 403: ErrorOut, 500: MessageOut})
    def delete(request: HttpRequest, message_ulid: str):
        log.info("MessageAPI delete", message_ulid=message_ulid)

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        try:
            chat_ulid = delete_message(user_id, message_ulid)
            if chat_ulid is None:
                return 403, ErrorOut(message="Forbidden")

            channel_layer = get_channel_layer()
            if channel_layer is not None:
                async_to_sync(channel_layer.group_send)(
                    f"chat_detail_{chat_ulid}",
                    {
                        "type": "chat_message",
                        "message": {
                            "command": "delete_message",
                            "message": {
                                "ulid": message_ulid,
                            },
                        },
                    },
                )

            return 200, MessageOut(error=False, message="メッセージを削除しました")
        except Exception as e:
            log.error("MessageAPI delete error", exc=e)
            return 500, MessageOut(error=True, message="メッセージの削除に失敗しました")
