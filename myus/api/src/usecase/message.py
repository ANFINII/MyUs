from api.src.domain.entity.message.repository import MessageRepository
from api.src.domain.entity.user.repository import UserRepository
from api.src.domain.interface.message.interface import FilterOption, SortOption
from api.src.types.data.message import MessageData, MessageReplyData
from api.src.usecase._convert import get_author


def get_messages(chat_id: int) -> list[MessageData]:
    message_repo = MessageRepository()
    user_repo = UserRepository()

    ids = message_repo.get_ids(FilterOption(chat_id=chat_id, is_parent=True), SortOption())
    messages = message_repo.bulk_get(ids)

    author_ids = list(set(m.author_id for m in messages))
    users = user_repo.bulk_get(author_ids)
    user_map = {u.user.id: u for u in users}

    data = [
        MessageData(
            ulid=m.ulid,
            text=m.text,
            created=m.created,
            updated=m.updated,
            author=get_author(user_map, m.author_id),
        ) for m in messages
    ]
    return data


def get_replys(chat_id: int) -> list[MessageReplyData]:
    message_repo = MessageRepository()
    user_repo = UserRepository()

    ids = message_repo.get_ids(FilterOption(chat_id=chat_id, is_parent=False), SortOption())
    messages = message_repo.bulk_get(ids)

    author_ids = list(set(m.author_id for m in messages))
    users = user_repo.bulk_get(author_ids)
    user_map = {u.user.id: u for u in users}

    data = [
        MessageReplyData(
            ulid=m.ulid,
            parent_id=m.parent_ulid,
            text=m.text,
            created=m.created,
            updated=m.updated,
            author=get_author(user_map, m.author_id),
        ) for m in messages
    ]
    return data
