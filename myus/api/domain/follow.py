from dataclasses import dataclass
from enum import Enum
from functools import reduce
from operator import and_
from django.db.models import Q
from api.models.users import Follow
from api.models.user import User
from app.modules.search import get_q_list
from api.types.data.follow import FollowOutData


class SortType(Enum):
    CREATED = "created"


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class FollowDomain:
    @classmethod
    def get_follows(cls, user_id: int, search: str | None, limit: int) -> list[Follow]:
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

        return qs.order_by(order_by_key)[:limit]

    @classmethod
    def get_followers(cls, user_id: int, search: str | None, limit: int) -> list[Follow]:
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

        return qs.order_by(order_by_key)[:limit]

    @classmethod
    def create(cls, follower: User, following: User) -> FollowOutData:
        if follower == following:
            return FollowOutData(is_follow=False, follower_count=following.follower_count)

        follow = Follow.objects.filter(follower=follower, following=following).first()

        if follow:
            follow.delete()
            is_follow = False
        else:
            follow = Follow.objects.create(follower=follower, following=following)
            is_follow = True

        following_count = Follow.objects.filter(follower=follower).count()
        follower.following_count = following_count
        follower.save(update_fields=["following_count"])

        follower_count = Follow.objects.filter(following=following).count()
        following.follower_count = follower_count
        following.save(update_fields=["follower_count"])

        return FollowOutData(is_follow=is_follow, follower_count=follower_count)

    @classmethod
    def delete(cls, follower: User, following: User) -> None:
        follow = Follow.objects.filter(follower=follower, following=following).first()

        if not follow:
            return None

        follow.delete()

        following_count = Follow.objects.filter(follower=follower).count()
        follower.following_count = following_count
        follower.save(update_fields=["following_count"])

        follower_count = Follow.objects.filter(following=following).count()
        following.follower_count = follower_count
        following.save(update_fields=["follower_count"])
