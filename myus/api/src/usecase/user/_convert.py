from api.src.injectors.container import injector
from api.src.domain.interface.user.data import UserAllData
from api.src.domain.interface.user.interface import UserInterface
from api.utils.common.result import FatalError, Result


@Result.shield_exception()
def save_user_data(data: UserAllData) -> Result[None, FatalError]:
    repo = injector.get(UserInterface)
    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)
