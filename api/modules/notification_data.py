from django.db.models import Exists, OuterRef
from django.db.models.query import QuerySet
from itertools import chain
from api.models import NotificationSetting, Notification, Follow


def notification_data(self):
    user_id = self.request.user.id
    notification_obj, notification_obj_list_1, notification_obj_list_2 = QuerySet, [], []
    notification_list_1, notification_list_confirmed = [], []
    confirmed_kwargs = {}
    confirmed_kwargs['id'] = OuterRef('pk')
    confirmed_kwargs['confirmed'] = user_id
    subquery_confirmed = Notification.objects.filter(**confirmed_kwargs)
    following_list = list(Follow.objects.filter(follower_id=user_id).values_list('following_id', 'created'))
    if user_id is not None:
        notification_obj = NotificationSetting.objects.get(user_id=user_id)
        if notification_obj.is_video:
            notification_obj_list_1 += [1]
        if notification_obj.is_live:
            notification_obj_list_1 += [2]
        if notification_obj.is_music:
            notification_obj_list_1 += [3]
        if notification_obj.is_picture:
            notification_obj_list_1 += [4]
        if notification_obj.is_blog:
            notification_obj_list_1 += [5]
        if notification_obj.is_chat:
            notification_obj_list_1 += [6]
        if notification_obj.is_collabo:
            notification_obj_list_1 += [7]
        if notification_obj.is_follow:
            notification_obj_list_2 += [8]
        if notification_obj.is_like:
            notification_obj_list_2 += [9]
        if notification_obj.is_reply:
            notification_obj_list_2 += [10]
        if notification_obj.is_views:
            notification_obj_list_2 += [11]
        for id, dates in following_list:
            notification_list_1 += Notification.objects.filter(user_from_id__in=[id], created__gt=dates, user_to_id=None, type_no__in=notification_obj_list_1).exclude(deleted=user_id).annotate(user_confirmed=Exists(subquery_confirmed)).order_by('-created')
            notification_list_confirmed += Notification.objects.filter(user_from_id__in=[id], created__gt=dates, user_to_id=None, type_no__in=notification_obj_list_1).exclude(deleted=user_id, confirmed=user_id).annotate(user_confirmed=Exists(subquery_confirmed)).order_by('-created')
        notification_list_2 = Notification.objects.filter(user_to_id=user_id, type_no__in=notification_obj_list_2).exclude(deleted=user_id).annotate(user_confirmed=Exists(subquery_confirmed)).order_by('-created')
        notification_list_data = {
            'notification_count': len(list(chain(notification_list_confirmed, notification_list_2.exclude(confirmed=user_id)))),
            'notification_list': list(chain(notification_list_1, notification_list_2)),
        }
        return notification_list_data
