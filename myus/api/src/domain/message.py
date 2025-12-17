from api.models.message import Message


class MessageDomain:
    @classmethod
    def bulk_get(cls, chat_id: int, is_parent: bool) -> list[Message]:
        return Message.objects.filter(chat_id=chat_id, parent__isnull=is_parent).select_related("author")
