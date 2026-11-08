import hmac
from django_ulid.models import ulid
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.channel.interface import ChannelInterface
from api.src.domain.interface.user.data import UserAllData
from api.src.domain.interface.user.interface import UserInterface
from api.src.injectors.container import injector
from api.utils.common.result import FatalError, Result
from api.utils.functions.token import password_fingerprint


@Result.shield_exception()
def get_active_user(user_id: int) -> Result[UserAllData | None, FatalError]:
    repo = injector.get(UserInterface)
    ret = repo.bulk_get([user_id])
    if ret.is_err:
        return Result.err(ret.err_value)

    users = ret.ok_value
    if len(users) == 0 or not users[0].user.is_active:
        return Result.ok(None)

    return Result.ok(users[0])


def is_same_password(fingerprint: object, password_hash: str) -> bool:
    if not isinstance(fingerprint, str):
        return False
    return hmac.compare_digest(fingerprint, password_fingerprint(password_hash))


@Result.shield_exception()
def create_user_data(data: UserAllData, channel_name: str) -> Result[None, FatalError]:
    repo = injector.get(UserInterface)
    channel_repo = injector.get(ChannelInterface)
    user_ret = repo.bulk_save(objs=[data])
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user_ids = user_ret.ok_value
    channel_ret = channel_repo.bulk_save([ChannelData(
        id=0,
        ulid=str(ulid.new()),
        owner_id=user_ids[0],
        owner_ulid="",
        avatar="",
        name=channel_name,
        description="",
        is_default=True,
        count=0,
    )])
    if channel_ret.is_err:
        return Result.err(channel_ret.err_value)

    return Result.ok(None)
