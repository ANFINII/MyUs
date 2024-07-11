from apps.api.types.user import Author


class Comment:
    def __init__(self, id: int, text: str, reply_count: int, created: str, author: Author):
        self.id = id
        self.text = text
        self.reply_count = reply_count
        self.created = created
        self.author = author
