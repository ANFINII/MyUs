from dataclasses import dataclass
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from myus.utils.common.logger import log
from ..dto.message import MessageDTO


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


def send_to_group(group_name: str, command: str, message: dict[str, object]) -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        log.warning("channel_layer is None")
        return

    try:
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
    except Exception as e:
        log.error("WebSocket broadcast failed", exc=e, group_name=group_name, command=command)


def build_message_payload(data: MessageDTO) -> MessagePayload:
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
