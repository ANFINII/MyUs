from api.models.message import Message


class MessageDomain:
    @classmethod
    def get_messages(cls, chat_id: int) -> list[Message]:
        return Message.objects.filter(chat_id=chat_id, parent__isnull=True).select_related("author")

    @classmethod
    def get_replys(cls, chat_id: int) -> list[Message]:
        return Message.objects.filter(chat_id=chat_id, parent__isnull=False).select_related("author")
