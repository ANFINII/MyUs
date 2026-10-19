from api.src.domain.interface.subscribe.interface import FilterOption, SortOption, SubscribeInterface
from api.src.injectors.container import injector
from api.src.types.dto.user import MediaUserDTO
from api.utils.common.result import FatalError, Result


@Result.shield_exception()
def get_media_user(is_like: bool, channel_id: int, user_id: int | None) -> Result[MediaUserDTO, FatalError]:
    subscribe_repo = injector.get(SubscribeInterface)
    subscribe = None
    if user_id is not None:
        ids_ret = subscribe_repo.get_ids(FilterOption(user_id=user_id, channel_id=channel_id), SortOption())
        if ids_ret.is_err:
            return Result.err(ids_ret.err_value)

        ids = ids_ret.ok_value
        subscribes_ret = subscribe_repo.bulk_get(ids)
        if subscribes_ret.is_err:
            return Result.err(subscribes_ret.err_value)

        subscribes = subscribes_ret.ok_value
        subscribe = subscribes[0] if len(subscribes) > 0 else None

    data = MediaUserDTO(
        is_like=is_like,
        is_subscribe=subscribe.is_subscribe if subscribe else False,
    )

    return Result.ok(data)
