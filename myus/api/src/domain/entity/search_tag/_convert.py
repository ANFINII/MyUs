from api.db.models.users import SearchTag
from api.src.domain.interface.search_tag.data import SearchTagData


def convert_data(obj: SearchTag) -> SearchTagData:
    return SearchTagData(
        id=obj.id,
        author_id=obj.author_id,
        sequence=obj.sequence,
        name=obj.name,
    )


def marshal_data(data: SearchTagData) -> SearchTag:
    return SearchTag(
        id=data.id if data.id != 0 else None,
        author_id=data.author_id,
        sequence=data.sequence,
        name=data.name,
    )
