from api.db.models.master import Category
from api.src.domain.interface.category.data import CategoryData


def convert_data(obj: Category) -> CategoryData:
    return CategoryData(
        id=obj.id,
        ulid=obj.ulid,
        jp_name=obj.jp_name,
        en_name=obj.en_name,
    )
