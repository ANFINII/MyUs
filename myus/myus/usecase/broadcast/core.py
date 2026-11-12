from dataclasses import asdict, dataclass
from ..dto.message import MessageDTO
from ._convert import send_to_group, build_message_payload


@dataclass(frozen=True, slots=True)
class UpdateMessagePayload:
    ulid: str
    text: str


@dataclass(frozen=True, slots=True)
class DeleteMessagePayload:
    ulid: str


def broadcast_create_message(chat_ulid: str, data: MessageDTO, parent_ulid: str) -> None:
    is_reply = len(parent_ulid) > 0
    command = "create_reply_message" if is_reply else "create_message"
    payload: dict[str, object] = asdict(build_message_payload(data))
    if is_reply:
        payload["parent_ulid"] = parent_ulid
    send_to_group(f"chat_detail_{chat_ulid}", command, payload)


def broadcast_update_message(chat_ulid: str, message_ulid: str, text: str) -> None:
    payload = UpdateMessagePayload(ulid=message_ulid, text=text)
    send_to_group(f"chat_detail_{chat_ulid}", "update_message", asdict(payload))


def broadcast_delete_message(chat_ulid: str, message_ulid: str) -> None:
    payload = DeleteMessagePayload(ulid=message_ulid)
    send_to_group(f"chat_detail_{chat_ulid}", "delete_message", asdict(payload))
