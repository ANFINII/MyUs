from api.src.domain.interface.category.data import CategoryData
from api.utils.common.result import Result, ValidationError


def validate_category_data(category: CategoryData | None) -> Result[CategoryData, ValidationError]:
    if category is None:
        return Result.err(ValidationError("error.categoryRequired"))

    return Result.ok(category)
