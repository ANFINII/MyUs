from api.src.domain.interface.category.data import CategoryData
from api.src.domain.interface.channel.data import ChannelData
from api.utils.common.result import ForbiddenError, Result, ValidationError


def validate_owner_data(user_id: int, channel: ChannelData) -> Result[None, ForbiddenError]:
    if channel.owner_id != user_id:
        return Result.err(ForbiddenError("error.forbidden"))

    return Result.ok(None)


def validate_category_data(category: CategoryData | None) -> Result[CategoryData, ValidationError]:
    if category is None:
        return Result.err(ValidationError("error.categoryRequired"))

    return Result.ok(category)
