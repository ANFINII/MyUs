from django.db import transaction
from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.comment import Comment
from api.db.models.user import MyPage, Profile, User, UserNotification, UserPlan
from api.src.domain.entity.index import sort_ids
from api.src.domain.entity.user._convert import convert_data, get_media_model, marshal_mypage, marshal_notification, marshal_profile, marshal_user, marshal_user_plan
from api.src.domain.interface.user.data import UserAllData
from api.src.domain.interface.user.interface import FilterOption, SortOption, UserInterface
from api.utils.enum.index import MediaType


USER_FIELDS = ["avatar", "username", "nickname", "email", "is_active"]
PROFILE_FIELDS = [
    "last_name", "first_name", "birthday", "gender", "phone",
    "country_code", "postal_code", "prefecture", "city", "street", "introduction",
]
MYPAGE_FIELDS = ["banner", "email", "content", "follower_count", "following_count", "tag_manager_id", "is_advertise"]
NOTIFICATION_FIELDS = [
    "is_video", "is_music", "is_comic", "is_picture", "is_blog",
    "is_chat", "is_follow", "is_reply", "is_like", "is_views",
]
USER_PLAN_FIELDS = ["customer_id", "subscription", "is_paid", "start_date", "end_date"]


class UserRepository(UserInterface):
    def queryset(self) -> QuerySet[User]:
        return User.objects.select_related("profile", "mypage", "notification", "user_plan", "user_plan__plan")

    def get_ids(self, filter: FilterOption, sort: SortOption | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.id:
            q_list.append(Q(id=filter.id))
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))

        qs = User.objects.filter(*q_list)

        if sort is not None:
            field_name = sort.sort_type.name
            order_by_key = field_name if sort.is_asc else f"-{field_name}"
            qs = qs.order_by(order_by_key)

        return list(qs.values_list("id", flat=True))

    def bulk_get(self, ids: list[int]) -> list[UserAllData]:
        if len(ids) == 0:
            return []

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return [convert_data(obj) for obj in sorted_objs]

    def bulk_save(self, objs: list[UserAllData]) -> list[int]:
        if len(objs) == 0:
            return []

        with transaction.atomic():
            save_objs = User.objects.bulk_create(
                [marshal_user(o.user) for o in objs],
                update_conflicts=True,
                update_fields=USER_FIELDS,
            )
            Profile.objects.bulk_create(
                [marshal_profile(user, o) for user, o in zip(save_objs, objs)],
                update_conflicts=True,
                update_fields=PROFILE_FIELDS,
            )
            MyPage.objects.bulk_create(
                [marshal_mypage(user, o) for user, o in zip(save_objs, objs)],
                update_conflicts=True,
                update_fields=MYPAGE_FIELDS,
            )
            UserNotification.objects.bulk_create(
                [marshal_notification(user, o) for user, o in zip(save_objs, objs)],
                update_conflicts=True,
                update_fields=NOTIFICATION_FIELDS,
            )
            UserPlan.objects.bulk_create(
                [marshal_user_plan(user, o) for user, o in zip(save_objs, objs)],
                update_conflicts=True,
                update_fields=USER_PLAN_FIELDS,
            )

        return [o.id for o in save_objs]

    def media_like(self, user_id: int, media_type: MediaType, media_id: int) -> tuple[bool, int]:
        model_class = get_media_model(media_type)
        obj = model_class.objects.prefetch_related("like").get(id=media_id)
        is_like = obj.like.filter(id=user_id).exists()
        if is_like:
            obj.like.remove(user_id)
        else:
            obj.like.add(user_id)
        return (not is_like, obj.like.count())

    def comment_like(self, user_id: int, comment_id: int) -> tuple[bool, int]:
        obj = Comment.objects.prefetch_related("like").get(id=comment_id)
        is_like = obj.like.filter(id=user_id).exists()
        if is_like:
            obj.like.remove(user_id)
        else:
            obj.like.add(user_id)
        return (not is_like, obj.like.count())
