from dataclasses import replace
from myus.domain.follow.data import FollowData
from myus.domain.follow.interface import FilterOption, FollowInterface
from myus.domain.user.data import UserAllData
from myus.domain.user.interface import UserInterface
from myus.injectors.container import injector
from myus.usecase.notification._convert import create_notification_data
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.notification import NotificationObjectType, NotificationTypeNo


@Result.shield_exception()
def save_follow_data(follower: UserAllData, following: UserAllData, follow: FollowData | None, is_follow: bool) -> Result[int, FatalError]:
    user_repo = injector.get(UserInterface)
    repo = injector.get(FollowInterface)
    follower_id = follower.user.id
    following_id = following.user.id
    if follow is None:
        new_ids_ret = repo.bulk_save([FollowData(
            id=0,
            follower_id=follower_id,
            following_id=following_id,
            is_follow=is_follow,
        )])
        if new_ids_ret.is_err:
            return Result.err(new_ids_ret.err_value)

        new_ids = new_ids_ret.ok_value
        if is_follow:
            notification_ret = create_notification_data(follower_id, following_id, NotificationTypeNo.FOLLOW, new_ids[0], NotificationObjectType.FOLLOW)
            if notification_ret.is_err:
                return Result.err(notification_ret.err_value)
    else:
        updated_follow = replace(follow, is_follow=is_follow)
        save_ret = repo.bulk_save([updated_follow])
        if save_ret.is_err:
            return Result.err(save_ret.err_value)

    follower_count_ret = repo.count(FilterOption(following_id=following_id, is_follow=True))
    if follower_count_ret.is_err:
        return Result.err(follower_count_ret.err_value)

    following_count_ret = repo.count(FilterOption(follower_id=follower_id, is_follow=True))
    if following_count_ret.is_err:
        return Result.err(following_count_ret.err_value)

    follower_count = follower_count_ret.ok_value
    following_count = following_count_ret.ok_value
    follow_count_ret = user_repo.save_follow_count(follower_id, following_id, follower_count, following_count)
    if follow_count_ret.is_err:
        return Result.err(follow_count_ret.err_value)

    return Result.ok(follower_count)
