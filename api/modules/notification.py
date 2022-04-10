from django.db.models import Exists, OuterRef
from itertools import chain
from api.models import NotificationSetting, Notification, Follow
from api.modules import contains


def notification_data(self):
    user_id = self.request.user.id
    notification_obj_list_1, notification_obj_list_2 = [], []
    notification_list_1, notification_list_confirmed = [], []
    confirmed_kwargs = {}
    confirmed_kwargs['id'] = OuterRef('pk')
    confirmed_kwargs['confirmed'] = user_id
    subquery_confirmed = Notification.objects.filter(**confirmed_kwargs)
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
            notification_list_1 += Notification.objects.filter(user_from_id__in=[id], created__gt=dates, user_to_id=None, type_no__in=notification_obj_list_1).exclude(deleted=user_id).annotate(user_confirmed=Exists(subquery_confirmed)).order_by('-created')
            notification_list_confirmed += Notification.objects.filter(user_from_id__in=[id], created__gt=dates, user_to_id=None, type_no__in=notification_obj_list_1).exclude(deleted=user_id, confirmed=user_id).annotate(user_confirmed=Exists(subquery_confirmed)).order_by('-created')
        notification_list_2 = Notification.objects.filter(user_to_id=user_id, type_no__in=notification_obj_list_2).exclude(deleted=user_id).annotate(user_confirmed=Exists(subquery_confirmed)).order_by('-created')
        notification_list_data = {
            'notification_list': list(chain(notification_list_1, notification_list_2)),
            'notification_count': len(list(chain(notification_list_confirmed, notification_list_2.exclude(confirmed=user_id)))),
        }
        return notification_list_data
