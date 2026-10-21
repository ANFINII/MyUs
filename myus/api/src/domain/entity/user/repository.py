from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import Q
from django.db.models.query import QuerySet
from api.db.models.comment import Comment
from api.db.models.user import MyPage, Profile, User, UserNotification, UserPlan
from api.src.domain.entity.index import get_save_new_ids, sort_ids
from api.src.domain.entity.user._convert import convert_data, get_media_model, marshal_mypage, marshal_notification, marshal_profile, marshal_user, marshal_user_plan, sort_field
from api.src.domain.interface.user.data import UserAllData
from api.src.domain.interface.user.interface import FilterOption, SortOption, UserInterface
from api.utils.common.result import FatalError, Result
from api.utils.enum.media import MediaType


USER_FIELDS = ["avatar", "username", "nickname", "email", "password", "is_active"]
PROFILE_FIELDS = [
    "last_name", "first_name", "birthday", "gender", "phone",
    "country_code", "postal_code", "prefecture", "city", "street", "introduction",
]
MYPAGE_FIELDS = ["banner", "email", "content", "tag_manager_id", "is_advertise"]
NOTIFICATION_FIELDS = [
    "is_video", "is_music", "is_blog", "is_comic", "is_picture",
    "is_chat", "is_follow", "is_reply", "is_like", "is_views",
]
USER_PLAN_FIELDS = ["plan", "customer_id", "subscription", "is_paid", "start_date", "end_date"]


class UserRepository(UserInterface):
    def queryset(self) -> QuerySet[User]:
        return User.objects.select_related("profile", "mypage", "notification", "user_plan")

    @Result.shield_exception()
    def get_ids(self, filter: FilterOption, sort: SortOption | None = None) -> Result[list[int], FatalError]:
        q_list: list[Q] = []
        if filter.id:
            q_list.append(Q(id=filter.id))
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))
        if filter.email:
            q_list.append(Q(email=filter.email))
        if filter.username:
            q_list.append(Q(username=filter.username))
        if filter.nickname:
            q_list.append(Q(nickname=filter.nickname))

        qs = User.objects.filter(*q_list)

        if sort is not None:
            field_name = sort_field(sort.sort_type)
            order_by_key = field_name if sort.is_asc else f"-{field_name}"
            qs = qs.order_by(order_by_key)

        return Result.ok(list(qs.values_list("id", flat=True)))

    @Result.shield_exception()
    def bulk_get(self, ids: list[int]) -> Result[list[UserAllData], FatalError]:
        if len(ids) == 0:
            return Result.ok([])

        objs = list(self.queryset().filter(id__in=ids))
        sorted_objs = sort_ids(objs, ids)
        return Result.ok([convert_data(obj) for obj in sorted_objs])

    @Result.shield_exception()
    def bulk_save(self, objs: list[UserAllData]) -> Result[list[int], FatalError]:
        if len(objs) == 0:
            return Result.ok([])

        models = [marshal_user(o.user) for o in objs]

        with transaction.atomic():
            new_ids = get_save_new_ids(models, USER_FIELDS)
            Profile.objects.bulk_create(
                [marshal_profile(user, o) for user, o in zip(models, objs)],
                update_conflicts=True,
                update_fields=PROFILE_FIELDS,
            )
            MyPage.objects.bulk_create(
                [marshal_mypage(user, o) for user, o in zip(models, objs)],
                update_conflicts=True,
                update_fields=MYPAGE_FIELDS,
            )
            UserNotification.objects.bulk_create(
                [marshal_notification(user, o) for user, o in zip(models, objs)],
                update_conflicts=True,
                update_fields=NOTIFICATION_FIELDS,
            )
            UserPlan.objects.bulk_create(
                [marshal_user_plan(user, o) for user, o in zip(models, objs)],
                update_conflicts=True,
                update_fields=USER_PLAN_FIELDS,
            )

        return Result.ok(new_ids)

    @Result.shield_exception()
    def authenticate(self, login_id: str, password: str) -> Result[int | None, FatalError]:
        user = authenticate(username=login_id, password=password)
        if user is None:
            return Result.ok(None)

        return Result.ok(user.id)

    @Result.shield_exception()
    def media_like(self, user_id: int, media_type: MediaType, media_id: int) -> Result[tuple[bool, int], FatalError]:
        model_class = get_media_model(media_type)
        obj = model_class.objects.only("id").get(id=media_id)
        is_like = obj.like.filter(id=user_id).exists()
        if is_like:
            obj.like.remove(user_id)
        else:
            obj.like.add(user_id)
        return Result.ok((not is_like, obj.like.count()))

    @Result.shield_exception()
    def comment_like(self, user_id: int, comment_id: int) -> Result[tuple[bool, int], FatalError]:
        obj = Comment.objects.only("id").get(id=comment_id)
        is_like = obj.like.filter(id=user_id).exists()
        if is_like:
            obj.like.remove(user_id)
        else:
            obj.like.add(user_id)
        return Result.ok((not is_like, obj.like.count()))

    @Result.shield_exception()
    def save_follow_count(self, follower_id: int, following_id: int, follower_count: int, following_count: int) -> Result[None, FatalError]:
        with transaction.atomic():
            MyPage.objects.filter(user_id=follower_id).update(following_count=following_count)
            MyPage.objects.filter(user_id=following_id).update(follower_count=follower_count)

        return Result.ok(None)
