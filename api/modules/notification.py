from django.db.models import Exists, OuterRef
from api.models import NotificationSetting, Notification, Follow
from api.modules import contains


def notification_data(self):
    user = self.request.user
    notification_type_list_1, notification_type_list_2 = [], []

    if user is not None:
        notification_setting_obj = NotificationSetting.objects.get(user=user)
        if notification_setting_obj.is_video:
            notification_type_list_1 += [contains.notification_type_dict['video'][0]]
        if notification_setting_obj.is_live:
            notification_type_list_1 += [contains.notification_type_dict['live'][0]]
        if notification_setting_obj.is_music:
            notification_type_list_1 += [contains.notification_type_dict['music'][0]]
        if notification_setting_obj.is_picture:
            notification_type_list_1 += [contains.notification_type_dict['picture'][0]]
        if notification_setting_obj.is_blog:
            notification_type_list_1 += [contains.notification_type_dict['blog'][0]]
        if notification_setting_obj.is_chat:
            notification_type_list_1 += [contains.notification_type_dict['chat'][0]]
        if notification_setting_obj.is_collabo:
            notification_type_list_1 += [contains.notification_type_dict['collabo'][0]]
        if notification_setting_obj.is_follow:
            notification_type_list_2 += [contains.notification_type_dict['follow'][0]]
        if notification_setting_obj.is_like:
            notification_type_list_2 += [contains.notification_type_dict['like'][0]]
        if notification_setting_obj.is_reply:
            notification_type_list_2 += [contains.notification_type_dict['reply'][0]]
        if notification_setting_obj.is_views:
            notification_type_list_2 += [contains.notification_type_dict['views'][0]]

        notification_list_1, notification_list_confirmed = [], []
        confirmed_kwargs = {'id': OuterRef('pk'), 'confirmed': user}
        subquery = Notification.objects.filter(**confirmed_kwargs)
        following_list = Follow.objects.filter(follower=user).values_list('following_id', 'created')

        for id, dates in following_list:
            notification_list_1 += Notification.objects.filter(user_from__in=[id], user_to=None, type_no__in=notification_type_list_1, created__gt=dates).exclude(deleted=user).annotate(user_confirmed=Exists(subquery)).order_by('-created')
            notification_list_confirmed += Notification.objects.filter(user_from__in=[id], user_to=None, type_no__in=notification_type_list_1, created__gt=dates).exclude(deleted=user).exclude(confirmed=user).annotate(user_confirmed=Exists(subquery))
        notification_list_2 = Notification.objects.filter(user_to=user, type_no__in=notification_type_list_2).exclude(deleted=user).annotate(user_confirmed=Exists(subquery)).order_by('-created')

        notification_list_data = {
            'notification_list': notification_list_1 + list(notification_list_2),
            'notification_count': len(notification_list_confirmed) + notification_list_2.exclude(confirmed=user).count(),
        }
        return notification_list_data


def notification_setting_update(is_notification, notification_type, notification_obj):
    if is_notification == 'True':
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
    if is_notification == 'False':
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
    notification_obj.save(update_fields=[contains.notification_type_dict[notification_type][1]])
