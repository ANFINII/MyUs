from dataclasses import replace
from django.db import transaction
from api.src.domain.interface.follow.data import FollowData
from api.src.domain.interface.follow.interface import FilterOption, FollowInterface, SortOption
from api.src.domain.interface.user.data import UserAllData
from api.src.domain.interface.user.interface import UserInterface
from api.src.injectors.container import injector
from api.src.types.dto.follow import FollowDTO, FollowUserDTO
from api.src.usecase.notification import create_notification
from api.src.usecase.user import get_user_data
from api.utils.common.result import FatalError, InputError, NotFoundError, Result, ValidationError
from api.utils.enum.notification import NotificationObjectType, NotificationTypeNo
from api.utils.functions.index import create_url


@Result.shield_exception()
def get_follows(user_id: int, search: str, limit: int) -> Result[list[FollowUserDTO], FatalError]:
    repo = injector.get(FollowInterface)
    user_repo = injector.get(UserInterface)
    ids_ret = repo.get_ids(FilterOption(follower_id=user_id, search=search), SortOption(), limit)
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
    ids_ret = repo.get_ids(FilterOption(following_id=user_id, search=search), SortOption(), limit)
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
    user_repo = injector.get(UserInterface)
    repo = injector.get(FollowInterface)
    following_ret = get_user_data(ulid=ulid)
    if following_ret.is_err:
        return Result.err(following_ret.err_value)

    following = following_ret.ok_value
    if following is None:
        return Result.err(NotFoundError("ユーザーが見つかりません!"))

    follower_id = follower.user.id
    following_id = following.user.id
    if follower_id == following_id:
        return Result.err(ValidationError("自分自身はフォローできません!"))

    follow_ids_ret = repo.get_ids(FilterOption(follower_id=follower_id, following_id=following_id), SortOption())
    if follow_ids_ret.is_err:
        return Result.err(follow_ids_ret.err_value)

    follow_ids = follow_ids_ret.ok_value
    follows_ret = repo.bulk_get(follow_ids)
    if follows_ret.is_err:
        return Result.err(follows_ret.err_value)

    follows = follows_ret.ok_value
    follow = follows[0] if len(follows) > 0 else None

    with transaction.atomic():
        if follow is None:
            new_ids_ret = repo.bulk_save([FollowData(
                id=0,
                follower_id=follower_id,
                following_id=following_id,
                is_follow=is_follow,
            )])
            if new_ids_ret.is_err:
                transaction.set_rollback(True)
                return Result.err(new_ids_ret.err_value)

            new_ids = new_ids_ret.ok_value
            if is_follow:
                notification_ret = create_notification(follower_id, following_id, NotificationTypeNo.FOLLOW, new_ids[0], NotificationObjectType.FOLLOW)
                if notification_ret.is_err:
                    transaction.set_rollback(True)
                    return Result.err(notification_ret.err_value)
        else:
            updated_follow = replace(follow, is_follow=is_follow)
            save_ret = repo.bulk_save([updated_follow])
            if save_ret.is_err:
                transaction.set_rollback(True)
                return Result.err(save_ret.err_value)

        follower_count_ret = repo.count(FilterOption(following_id=following.user.id, is_follow=True))
        if follower_count_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(follower_count_ret.err_value)

        following_count_ret = repo.count(FilterOption(follower_id=follower.user.id, is_follow=True))
        if following_count_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(following_count_ret.err_value)

        follower_count = follower_count_ret.ok_value
        following_count = following_count_ret.ok_value

        follow_count_ret = user_repo.save_follow_count(follower.user.id, following.user.id, follower_count, following_count)
        if follow_count_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(follow_count_ret.err_value)

    return Result.ok(FollowDTO(is_follow=is_follow, follower_count=follower_count))
