from django.db.models import Exists, OuterRef
from api.models import UserNotification, Notification, Follow
from api.utils.contains import notification_type_no


def notification_data(user):
    fields_1 = ["is_video", "is_music", "is_comic", "is_picture", "is_blog", "is_chat"]
    fields_2 = ["is_follow", "is_like", "is_reply", "is_views"]

    user_notification = UserNotification.objects.get(user=user)
    notification_no_list_1 = [notification_type_no[field] for field in fields_1 if getattr(user_notification, field)]
    notification_no_list_2 = [notification_type_no[field] for field in fields_2 if getattr(user_notification, field)]

    notification_none = Notification.objects.none()
    notification_union_1, notification_union_2 = notification_none, notification_none
    notification_confirmed_list = []
    confirmed_kwargs = {"id": OuterRef("pk"), "confirmed": user}
    subquery = Notification.objects.filter(**confirmed_kwargs)
    following_list = Follow.objects.filter(follower=user).values_list("following_id", "created")

    for id, dates in following_list:
        notification_qs_1 = Notification.objects.filter(user_from__in=[id], user_to=None, type_no__in=notification_no_list_1, created__gt=dates).annotate(is_confirmed=Exists(subquery)).exclude(deleted=user)
        notification_union_2 = notification_qs_1.select_related("user_from").prefetch_related("content_object")
        notification_union_1 = notification_union_1.union(notification_union_2)
        notification_confirmed_list += notification_qs_1.exclude(confirmed=user)
    notification_qs_2 = Notification.objects.filter(user_to=user, type_no__in=notification_no_list_2).annotate(is_confirmed=Exists(subquery)).exclude(deleted=user).select_related("user_from").prefetch_related("content_object")

    context = {
        "notification_list": notification_union_1.union(notification_qs_2).order_by("-created"),
        "notification_count": len(notification_confirmed_list) + notification_qs_2.exclude(confirmed=user).count(),
    }
    return context


def user_notification_update(is_notification, notification_type, notification_obj):
    attribute_name = f"is_{notification_type}"
    is_bool = is_notification != "True"
    if hasattr(notification_obj, attribute_name):
        setattr(notification_obj, attribute_name, is_bool)
        notification_obj.save(update_fields=[attribute_name])
