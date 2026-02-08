from django.db.models import Exists, OuterRef
from api.db.models import Follow, Notification, UserNotification
from api.utils.constant import notification_type_no
from api.utils.functions.index import set_attr


def get_notification(user_id: int):
    fields_1 = ["is_video", "is_music", "is_comic", "is_picture", "is_blog", "is_chat"]
    fields_2 = ["is_follow", "is_like", "is_reply", "is_views"]

    user_notification = UserNotification.objects.get(user_id=user_id)
    notification_no_list_1 = [notification_type_no[field] for field in fields_1 if getattr(user_notification, field)]
    notification_no_list_2 = [notification_type_no[field] for field in fields_2 if getattr(user_notification, field)]

    notification_none = Notification.objects.none()
    notification_union_1, notification_union_2 = notification_none, notification_none
    notification_confirmed_list = []
    confirmed_kwargs = {"id": OuterRef("pk"), "confirmed": user_id}
    subquery = Notification.objects.filter(**confirmed_kwargs)
    following_list = Follow.objects.filter(follower_id=user_id).values_list("following_id", "created")

    for id, dates in following_list:
        notification_qs_1 = Notification.objects.filter(user_from__in=[id], user_to=None, type_no__in=notification_no_list_1, created__gt=dates).annotate(is_confirmed=Exists(subquery)).exclude(deleted=user_id)
        notification_union_2 = notification_qs_1.select_related("user_from")
        notification_union_1 = notification_union_1.union(notification_union_2)
        notification_confirmed_list += notification_qs_1.exclude(confirmed=user_id)
    notification_qs_2 = Notification.objects.filter(user_to_id=user_id, type_no__in=notification_no_list_2).annotate(is_confirmed=Exists(subquery)).exclude(deleted=user_id).select_related("user_from")

    context = {
        "count": len(notification_confirmed_list) + notification_qs_2.exclude(confirmed=user_id).count(),
        "datas": notification_union_1.union(notification_qs_2).order_by("-created"),
    }
    return context


def user_notification_update(is_notification, notification_type, notification_obj):
    attribute_name = f"is_{notification_type}"
    is_bool = is_notification != "True"
    if hasattr(notification_obj, attribute_name):
        set_attr(notification_obj, attribute_name, is_bool)
        notification_obj.save(update_fields=[attribute_name])


def get_content_object(notification: Notification) -> dict:
    obj_list = ["video", "music", "comic", "picture", "blog", "chat"]
    data = {"id": notification.object_id}

    # if notification.type_name in obj_list:
    #     data.update({
    #         "title": notification.content_object.title,
    #         "text": notification.content_object.text,
    #         "read": notification.content_object.read,
    #     })
    return data
