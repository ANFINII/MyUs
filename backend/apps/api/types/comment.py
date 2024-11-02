from dataclasses import dataclass
from apps.api.types.user import AuthorData


@dataclass(frozen=True, slots=True)
class CommentData:
    id: str
    text: str
    reply_count: str
    created: bool
    author: AuthorData
