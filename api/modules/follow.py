from api.models import Follow, Notification
from api.modules import contains


def follow_update_data(follower, following, follow_obj):
    if follower == following:
        # '自分はフォローできません'
        pass
    elif follow_obj.exists():
        notification_obj = Notification.objects.filter(type_no=contains.notification_type_no['follow'], object_id=follow_obj[0].id)
        notification_obj.delete()
        follow_obj.delete()
        followed = False
        #ログインユーザーのフォロー数
        following_count = Follow.objects.filter(follower=follower.user).count()
        follower.following_num = following_count
        follower.save()
        #フォローユーザーのフォロワー数
        follower_count = Follow.objects.filter(following=following.user).count()
        following.follower_num = follower_count
        following.save()
        # 'フォローを外しました'
    else:
        follow_obj = Follow.objects.create(follower=follower.user, following=following.user)
        followed = True
        #ログインユーザーのフォロー数
        following_count = Follow.objects.filter(follower=follower.user).count()
        follower.following_num = following_count
        follower.save()
        #フォローユーザーのフォロワー数
        follower_count = Follow.objects.filter(following=following.user).count()
        following.follower_num = follower_count
        following.save()
        # 'フォローしました'
        Notification.objects.create(
            user_from_id=following.id,
            user_to_id=follower.id,
            type_no=contains.notification_type_no['follow'],
            type_name='follow',
            content_object=follow_obj,
        )
    return {'followed': followed, 'follower_count': follower_count}
