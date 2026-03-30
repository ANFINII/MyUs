from dataclasses import asdict, dataclass
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from api.modules.logger import log
from api.src.types.dto.message import MessageDTO


@dataclass(frozen=True, slots=True)
class AuthorPayload:
    avatar: str
    ulid: str
    nickname: str
    follower_count: int


@dataclass(frozen=True, slots=True)
class MessagePayload:
    ulid: str
    text: str
    created: str
    updated: str
    author: AuthorPayload


@dataclass(frozen=True, slots=True)
class UpdateMessagePayload:
    ulid: str
    text: str


@dataclass(frozen=True, slots=True)
class DeleteMessagePayload:
    ulid: str


def _send_to_group(group_name: str, command: str, message: dict[str, object]) -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        log.warning("channel_layer is None")
        return

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat_message",
            "message": {
                "command": command,
                "message": message,
            },
        },
    )


def _build_message_payload(data: MessageDTO) -> MessagePayload:
    return MessagePayload(
        ulid=data.ulid,
        text=data.text,
        created=data.created.isoformat(),
        updated=data.updated.isoformat(),
        author=AuthorPayload(
            avatar=data.author.avatar,
            ulid=data.author.ulid,
            nickname=data.author.nickname,
            follower_count=data.author.follower_count,
        ),
    )


def broadcast_create_message(chat_ulid: str, data: MessageDTO, parent_ulid: str) -> None:
    is_reply = len(parent_ulid) > 0
    command = "create_reply_message" if is_reply else "create_message"
    payload: dict[str, object] = asdict(_build_message_payload(data))
    if is_reply:
        payload["parent_ulid"] = parent_ulid
    _send_to_group(f"chat_detail_{chat_ulid}", command, payload)


def broadcast_update_message(chat_ulid: str, message_ulid: str, text: str) -> None:
    payload = UpdateMessagePayload(ulid=message_ulid, text=text)
    _send_to_group(f"chat_detail_{chat_ulid}", "update_message", asdict(payload))


def broadcast_delete_message(chat_ulid: str, message_ulid: str) -> None:
    payload = DeleteMessagePayload(ulid=message_ulid)
    _send_to_group(f"chat_detail_{chat_ulid}", "delete_message", asdict(payload))
