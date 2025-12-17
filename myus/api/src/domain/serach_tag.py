from dataclasses import dataclass
from enum import Enum
from api.models.users import SearchTag
from api.utils.functions.index import set_attr


class SortType(Enum):
    CREATED = "date_joined"
    NICKNAME = "nickname"


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class SearchTagDomain:
    @classmethod
    def get(cls, author_id: int) -> list[SearchTag]:
        return SearchTag.objects.filter(author_id=author_id).order_by("sequence")[:20]

    @classmethod
    def create(cls, **kwargs) -> SearchTag:
       return SearchTag.objects.create(**kwargs)

    @classmethod
    def update(cls, search_tag: SearchTag, **kwargs) -> None:
        if not kwargs:
            return

        [set_attr(search_tag, key, value) for key, value in kwargs.items()]
        SearchTag.save(update_fields=list[str](kwargs.keys()))
