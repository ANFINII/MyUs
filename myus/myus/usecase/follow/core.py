from myus.domain.follow.interface import FilterOption, FollowInterface, SortOption
from myus.domain.user.data import UserAllData
from myus.domain.user.interface import UserInterface
from myus.injectors.container import injector
from myus.utils.common.result import FatalError, InputError, NotFoundError, Result, ValidationError
from myus.utils.functions.transaction import atomic_result
from myus.utils.functions.url import create_url
from ._convert import save_follow_data
from ..dto.follow import FollowDTO, FollowUserDTO
from ..user.core import get_user_data


@Result.shield_exception()
def get_follows(user_id: int, search: str, limit: int) -> Result[list[FollowUserDTO], FatalError]:
    repo = injector.get(FollowInterface)
    user_repo = injector.get(UserInterface)
    ids_ret = repo.get_ids(FilterOption(follower_id=user_id, is_follow=True, search=search), SortOption(), limit)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    follows_ret = repo.bulk_get(ids)
    if follows_ret.is_err:
        return Result.err(follows_ret.err_value)

    follows = follows_ret.ok_value
    following_ids = [f.following_id for f in follows]
    users_ret = user_repo.bulk_get(following_ids)
    if users_ret.is_err:
        return Result.err(users_ret.err_value)

    users = users_ret.ok_value
    return Result.ok([
        FollowUserDTO(
            ulid=u.user.ulid,
            avatar=create_url(u.user.avatar),
            nickname=u.user.nickname,
            introduction=u.profile.introduction,
            follower_count=u.mypage.follower_count,
            following_count=u.mypage.following_count,
        ) for u in users
    ])


@Result.shield_exception()
def get_followers(user_id: int, search: str, limit: int) -> Result[list[FollowUserDTO], FatalError]:
    repo = injector.get(FollowInterface)
    user_repo = injector.get(UserInterface)
    ids_ret = repo.get_ids(FilterOption(following_id=user_id, is_follow=True, search=search), SortOption(), limit)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    follows_ret = repo.bulk_get(ids)
    if follows_ret.is_err:
        return Result.err(follows_ret.err_value)

    follows = follows_ret.ok_value
    follower_ids = [f.follower_id for f in follows]
    users_ret = user_repo.bulk_get(follower_ids)
    if users_ret.is_err:
        return Result.err(users_ret.err_value)

    users = users_ret.ok_value
    return Result.ok([
        FollowUserDTO(
            ulid=u.user.ulid,
            avatar=create_url(u.user.avatar),
            nickname=u.user.nickname,
            introduction=u.profile.introduction,
            follower_count=u.mypage.follower_count,
            following_count=u.mypage.following_count,
        ) for u in users
    ])


@Result.shield_exception()
def upsert_follow(follower: UserAllData, ulid: str, is_follow: bool) -> Result[FollowDTO, InputError]:
    repo = injector.get(FollowInterface)
    following_ret = get_user_data(ulid=ulid)
    if following_ret.is_err:
        return Result.err(following_ret.err_value)

    following = following_ret.ok_value
    if following is None:
        return Result.err(NotFoundError("error.userNotFound"))

    follower_id = follower.user.id
    following_id = following.user.id
    if follower_id == following_id:
        return Result.err(ValidationError("error.followSelf"))

    follow_ids_ret = repo.get_ids(FilterOption(follower_id=follower_id, following_id=following_id), SortOption())
    if follow_ids_ret.is_err:
        return Result.err(follow_ids_ret.err_value)

    follow_ids = follow_ids_ret.ok_value
    follows_ret = repo.bulk_get(follow_ids)
    if follows_ret.is_err:
        return Result.err(follows_ret.err_value)

    follows = follows_ret.ok_value
    follow = follows[0] if len(follows) > 0 else None

    save_ret = atomic_result(lambda: save_follow_data(follower, following, follow, is_follow))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    follower_count = save_ret.ok_value
    return Result.ok(FollowDTO(is_follow=is_follow, follower_count=follower_count))
