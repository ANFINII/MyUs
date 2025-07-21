from dataclasses import dataclass
from enum import Enum
from functools import reduce
from operator import and_
from django.db.models import Q
from api.models.users import Follow
from api.models.user import User
from api.models.notification import Notification
from app.modules.search import get_q_list
from api.types.data.follow import FollowUserData, FollowOutData
from api.utils.enum.index import NotificationType, NotificationTypeNo, NotificationObjectType
from api.utils.functions.index import create_url


class SortType(Enum):
    CREATED = "created"


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class FollowDomain:
    @classmethod
    def get_follows(cls, user_id: int, search: str | None = None, limit: int = 100) -> list[FollowUserData]:
        field_name = SortType.CREATED.value
        order_by_key = field_name if SortOption().is_asc else f'-{field_name}'
        qs = Follow.objects.filter(follower_id=user_id).select_related("following__profile", "following__mypage").distinct()

        if search:
            q_list = get_q_list(search)
            query = reduce(and_, [
                Q(following__nickname__icontains=q) |
                Q(following__profile__introduction__icontains=q) for q in q_list
            ])
            qs = qs.filter(query)

        objs = qs.order_by(order_by_key)[:limit]

        return [
            FollowUserData(
                avatar=create_url(obj.following.avatar.url),
                nickname=obj.following.nickname,
                introduction=obj.following.profile.introduction,
                follower_count=obj.following.mypage.follower_count,
                following_count=obj.following.mypage.following_count,
            ) for obj in objs
        ]

    @classmethod
    def get_followers(cls, user_id: int, search: str | None = None, limit: int = 100) -> list[FollowUserData]:
        field_name = SortType.CREATED.value
        order_by_key = field_name if SortOption().is_asc else f'-{field_name}'
        qs = Follow.objects.filter(following_id=user_id).select_related("follower__profile", "follower__mypage").distinct()

        if search:
            q_list = get_q_list(search)
            search_query = reduce(and_, [
                Q(follower__nickname__icontains=q) |
                Q(follower__profile__introduction__icontains=q) for q in q_list
            ])
            qs = qs.filter(search_query)

        objs = qs.order_by(order_by_key)[:limit]

        return [
            FollowUserData(
                avatar=create_url(obj.follower.avatar.url),
                nickname=obj.follower.nickname,
                introduction=obj.follower.profile.introduction,
                follower_count=obj.follower.mypage.follower_count,
                following_count=obj.follower.mypage.following_count,
            ) for obj in objs
        ]

    @classmethod
    def create(cls, follower_id: int, following_id: int) -> FollowOutData:
        follower = User.objects.get(id=follower_id)
        following = User.objects.get(id=following_id)

        if follower_id == following_id:
            return FollowOutData(is_follow=False, follower_count=following.follower_count)

        follow = Follow.objects.filter(follower=follower, following=following).first()

        if follow:
            notification = Notification.objects.filter(type_no=NotificationTypeNo.FOLLOW, object_id=follow.id)
            notification.delete()
            follow.delete()
            is_follow = False
        else:
            follow = Follow.objects.create(follower=follower, following=following)
            is_follow = True

            if hasattr(following, 'usernotification') and following.usernotification.is_follow:
                Notification.objects.create(
                    user_from=follower,
                    user_to=following,
                    type_no=NotificationTypeNo.FOLLOW,
                    type_name=NotificationType.FOLLOW,
                    object_id=follow.id,
                    object_type=NotificationObjectType.FOLLOW,
                )

        following_count = Follow.objects.filter(follower=follower).count()
        follower.following_count = following_count
        follower.save(update_fields=["following_count"])

        follower_count = Follow.objects.filter(following=following).count()
        following.follower_count = follower_count
        following.save(update_fields=["follower_count"])

        return FollowOutData(is_follow=is_follow, follower_count=follower_count)

    @classmethod
    def delete(cls, follower_id: int, following_nickname: str) -> None:
        following = User.objects.get(nickname=following_nickname)
        follow = Follow.objects.filter(follower_id=follower_id, following=following).first()

        if follow:
            notification = Notification.objects.filter(type_no=NotificationTypeNo.FOLLOW, object_id=follow.id)
            notification.delete()
            follow.delete()

            follower = User.objects.get(id=follower_id)
            following_count = Follow.objects.filter(follower=follower).count()
            follower.following_count = following_count
            follower.save(update_fields=["following_count"])

            follower_count = Follow.objects.filter(following=following).count()
            following.follower_count = follower_count
            following.save(update_fields=["follower_count"])
