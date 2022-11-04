from django.db.models import Exists, OuterRef
from apps.myus.models import NotificationSetting, Notification, Follow
from apps.myus.modules.contains import NotificationTypeNo, notification_type_dict


def notification_data(self):
    user = self.request.user

    if user.id is None:
        return {}

    notification_type_list_1, notification_type_list_2 = [], []
    notification_setting_obj = NotificationSetting.objects.get(user=user)

    if notification_setting_obj.is_video:
        notification_type_list_1 += [NotificationTypeNo.video]
    if notification_setting_obj.is_music:
        notification_type_list_1 += [NotificationTypeNo.music]
    if notification_setting_obj.is_picture:
        notification_type_list_1 += [NotificationTypeNo.picture]
    if notification_setting_obj.is_blog:
        notification_type_list_1 += [NotificationTypeNo.blog]
    if notification_setting_obj.is_chat:
        notification_type_list_1 += [NotificationTypeNo.chat]
    if notification_setting_obj.is_collabo:
        notification_type_list_1 += [NotificationTypeNo.collabo]
    if notification_setting_obj.is_follow:
        notification_type_list_2 += [NotificationTypeNo.follow]
    if notification_setting_obj.is_like:
        notification_type_list_2 += [NotificationTypeNo.like]
    if notification_setting_obj.is_reply:
        notification_type_list_2 += [NotificationTypeNo.reply]
    if notification_setting_obj.is_views:
        notification_type_list_2 += [NotificationTypeNo.views]

    notification_qs= Notification.objects.none()
    notification_qs_1 = Notification.objects.none()
    notification_confirmed_list = []
    confirmed_kwargs = {'id': OuterRef('pk'), 'confirmed': user}
    subquery = Notification.objects.filter(**confirmed_kwargs)
    following_list = Follow.objects.filter(follower=user).values_list('following_id', 'created')

    for id, dates in following_list:
        notification_qs_1 = Notification.objects.filter(user_from__in=[id], user_to=None, type_no__in=notification_type_list_1, created__gt=dates).exclude(deleted=user).annotate(user_confirmed=Exists(subquery)).select_related('user_from').prefetch_related('content_object')
        notification_qs = notification_qs.union(notification_qs_1)
        notification_confirmed_list += Notification.objects.filter(user_from__in=[id], user_to=None, type_no__in=notification_type_list_1, created__gt=dates).exclude(deleted=user).exclude(confirmed=user).annotate(user_confirmed=Exists(subquery))
    notification_qs_2 = Notification.objects.filter(user_to=user, type_no__in=notification_type_list_2).exclude(deleted=user).annotate(user_confirmed=Exists(subquery)).select_related('user_from').prefetch_related('content_object')
    notification_list = notification_qs.union(notification_qs_2).order_by('-created')

    context = {
        'notification_list': notification_list,
        'notification_count': len(notification_confirmed_list) + notification_qs_2.exclude(confirmed=user).count(),
    }
    return context


def notification_setting_update(is_notification, notification_type, notification_obj):
    is_bool = True if is_notification == 'False' else False
    if notification_type == 'video': notification_obj.is_video = is_bool
    if notification_type == 'music': notification_obj.is_music = is_bool
    if notification_type == 'picture': notification_obj.is_picture = is_bool
    if notification_type == 'blog': notification_obj.is_blog = is_bool
    if notification_type == 'chat': notification_obj.is_chat = is_bool
    if notification_type == 'collabo': notification_obj.is_collabo = is_bool
    if notification_type == 'follow': notification_obj.is_follow = is_bool
    if notification_type == 'reply': notification_obj.is_reply = is_bool
    if notification_type == 'like': notification_obj.is_like = is_bool
    if notification_type == 'views': notification_obj.is_views = is_bool
    notification_obj.save(update_fields=[notification_type_dict[notification_type]])
