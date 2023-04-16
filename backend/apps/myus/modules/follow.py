from apps.myus.models import Follow, Notification
from apps.myus.modules.contains import NotificationTypeNo


def follow_update_data(follower, following, follow):
    if follower == following:
        # '自分はフォローできません'
        pass
    elif follow:
        notification = Notification.objects.filter(type_no=NotificationTypeNo.follow, object_id=follow.id)
        notification.delete()
        # 'フォローを外しました'
        follow.delete()
        is_follow = False
        #ログインユーザーのフォロー数
        following_count = Follow.objects.filter(follower=follower.user).count()
        follower.following_count = following_count
        follower.save(update_fields=['following_count'])
        #フォローユーザーのフォロワー数
        follower_count = Follow.objects.filter(following=following.user).count()
        following.follower_count = follower_count
        following.save(update_fields=['follower_count'])
    else:
        follow = Follow.objects.create(follower=follower.user, following=following.user)
        is_follow = True
        #ログインユーザーのフォロー数
        following_count = Follow.objects.filter(follower=follower.user).count()
        follower.following_count = following_count
        follower.save(update_fields=['following_count'])
        #フォローユーザーのフォロワー数
        follower_count = Follow.objects.filter(following=following.user).count()
        following.follower_count = follower_count
        following.save(update_fields=['follower_count'])
        # 'フォローしました'
        if following.user.notificationsetting.is_follow:
            Notification.objects.create(
                user_from=follower.user,
                user_to=following.user,
                type_no=NotificationTypeNo.follow,
                type_name='follow',
                content_object=follow,
            )
    return {'is_follow': is_follow, 'follower_count': follower_count}
