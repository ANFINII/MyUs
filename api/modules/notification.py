from django.db.models import Exists, OuterRef
from api.models import NotificationSetting, Notification, Follow
from api.modules import contains


def notification_data(self):
    user = self.request.user
    notification_type_list_1, notification_type_list_2 = [], []

    if user is not None:
        notification_setting_obj = NotificationSetting.objects.get(user=user)
        if notification_setting_obj.is_video:
            notification_type_list_1 += [contains.notification_type_no['video']]
        if notification_setting_obj.is_live:
            notification_type_list_1 += [contains.notification_type_no['live']]
        if notification_setting_obj.is_music:
            notification_type_list_1 += [contains.notification_type_no['music']]
        if notification_setting_obj.is_picture:
            notification_type_list_1 += [contains.notification_type_no['picture']]
        if notification_setting_obj.is_blog:
            notification_type_list_1 += [contains.notification_type_no['blog']]
        if notification_setting_obj.is_chat:
            notification_type_list_1 += [contains.notification_type_no['chat']]
        if notification_setting_obj.is_collabo:
            notification_type_list_1 += [contains.notification_type_no['collabo']]
        if notification_setting_obj.is_follow:
            notification_type_list_2 += [contains.notification_type_no['follow']]
        if notification_setting_obj.is_like:
            notification_type_list_2 += [contains.notification_type_no['like']]
        if notification_setting_obj.is_reply:
            notification_type_list_2 += [contains.notification_type_no['reply']]
        if notification_setting_obj.is_views:
            notification_type_list_2 += [contains.notification_type_no['views']]

        notification_obj_1 = None
        confirmed_kwargs = {'id': OuterRef('pk'), 'confirmed': user}
        subquery = Notification.objects.filter(**confirmed_kwargs)
        following_list = Follow.objects.filter(follower=user).values_list('following_id', 'created')

        for id, dates in following_list:
            notification_obj_1 = Notification.objects.filter(user_from__in=[id], user_to=None, type_no__in=notification_type_list_1, created__gt=dates).exclude(deleted=user).annotate(user_confirmed=Exists(subquery))
        notification_obj_2 = Notification.objects.filter(user_to=user, type_no__in=notification_type_list_2).exclude(deleted=user).annotate(user_confirmed=Exists(subquery))

        notification_list, notification_count = [], 0
        if notification_obj_1 is not None:
            notification_list = notification_obj_1.union(notification_obj_2).order_by('-created')
            notification_count = notification_obj_1.exclude(confirmed=user).union(notification_obj_2.exclude(confirmed=user)).count()
        notification_list_data = {
            'notification_list': notification_list,
            'notification_count': notification_count,
        }
        return notification_list_data


def notification_setting_update(notification, notification_type, notification_obj):
    if notification == 'True':
        notification = False
        if notification_type == 'video':
            notification_obj.is_video = False
        if notification_type == 'live':
            notification_obj.is_live = False
        if notification_type == 'music':
            notification_obj.is_music = False
        if notification_type == 'picture':
            notification_obj.is_picture = False
        if notification_type == 'blog':
            notification_obj.is_blog = False
        if notification_type == 'chat':
            notification_obj.is_chat = False
        if notification_type == 'collabo':
            notification_obj.is_collabo = False
        if notification_type == 'follow':
            notification_obj.is_follow = False
        if notification_type == 'reply':
            notification_obj.is_reply = False
        if notification_type == 'like':
            notification_obj.is_like = False
        if notification_type == 'views':
            notification_obj.is_views = False
    if notification == 'False':
        notification = True
        if notification_type == 'video':
            notification_obj.is_video = True
        if notification_type == 'live':
            notification_obj.is_live = True
        if notification_type == 'music':
            notification_obj.is_music = True
        if notification_type == 'picture':
            notification_obj.is_picture = True
        if notification_type == 'blog':
            notification_obj.is_blog = True
        if notification_type == 'chat':
            notification_obj.is_chat = True
        if notification_type == 'collabo':
            notification_obj.is_collabo = True
        if notification_type == 'follow':
            notification_obj.is_follow = True
        if notification_type == 'reply':
            notification_obj.is_reply = True
        if notification_type == 'like':
            notification_obj.is_like = True
        if notification_type == 'views':
            notification_obj.is_views = True
    notification_obj.save()
