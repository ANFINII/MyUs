from django.db.models import Exists, OuterRef
from api.models import NotificationSetting, Notification, Follow
from api.modules import contains


def notification_data(self):
    user_id = self.request.user.id
    notification_obj_list_1 = []
    notification_obj_list_2 = []
    confirmed_kwargs = {}
    confirmed_kwargs['id'] = OuterRef('pk')
    confirmed_kwargs['confirmed'] = user_id
    subquery = Notification.objects.filter(**confirmed_kwargs)
    following_list = list(Follow.objects.filter(follower_id=user_id).values_list('following_id', 'created'))
    if user_id is not None:
        notification_obj = NotificationSetting.objects.get(user_id=user_id)
        if notification_obj.is_video:
            notification_obj_list_1 += [contains.notification_type_no['video']]
        if notification_obj.is_live:
            notification_obj_list_1 += [contains.notification_type_no['live']]
        if notification_obj.is_music:
            notification_obj_list_1 += [contains.notification_type_no['music']]
        if notification_obj.is_picture:
            notification_obj_list_1 += [contains.notification_type_no['picture']]
        if notification_obj.is_blog:
            notification_obj_list_1 += [contains.notification_type_no['blog']]
        if notification_obj.is_chat:
            notification_obj_list_1 += [contains.notification_type_no['chat']]
        if notification_obj.is_collabo:
            notification_obj_list_1 += [contains.notification_type_no['collabo']]
        if notification_obj.is_follow:
            notification_obj_list_2 += [contains.notification_type_no['follow']]
        if notification_obj.is_like:
            notification_obj_list_2 += [contains.notification_type_no['like']]
        if notification_obj.is_reply:
            notification_obj_list_2 += [contains.notification_type_no['reply']]
        if notification_obj.is_views:
            notification_obj_list_2 += [contains.notification_type_no['views']]
        for id, dates in following_list:
            qs_1 = Notification.objects.filter(user_from_id__in=[id], created__gt=dates, user_to_id=None, type_no__in=notification_obj_list_1).exclude(deleted=user_id).annotate(user_confirmed=Exists(subquery))
            qs_2 = Notification.objects.filter(user_to_id=user_id, type_no__in=notification_obj_list_2).exclude(deleted=user_id).annotate(user_confirmed=Exists(subquery))
        notification_list_data = {
            'notification_list': qs_1.union(qs_2).order_by('-created'),
            'notification_count': qs_1.exclude(confirmed=user_id).union(qs_2.exclude(confirmed=user_id)).count(),
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
