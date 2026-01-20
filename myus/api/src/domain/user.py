from dataclasses import dataclass
from enum import Enum
from django.db.models import Q
from api.db.models.comment import Comment
from api.db.models.user import User
from api.src.domain.index import sort_ids
from api.utils.functions.index import set_attr
from api.utils.functions.media import MediaModel


class SortType(Enum):
    CREATED = "date_joined"
    NICKNAME = "nickname"


@dataclass(frozen=True, slots=True)
class FilterOption:
    id: int = 0
    ulid: str = ""


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = False
    sort_type: SortType = SortType.CREATED


class UserDomain:
    @classmethod
    def queryset(cls):
        return User.objects.select_related("profile", "mypage", "notification")

    @classmethod
    def get_ids(cls, filter: FilterOption, sort: SortOption, limit: int | None = None) -> list[int]:
        q_list: list[Q] = []
        if filter.id:
            q_list.append(Q(id=filter.id))
        if filter.ulid:
            q_list.append(Q(ulid=filter.ulid))

        field_name = sort.sort_type.value
        order_by_key = field_name if sort.is_asc else f"-{field_name}"
        qs = User.objects.filter(*q_list).order_by(order_by_key)

        if limit:
            qs = qs[:limit]

        return list(qs.values_list("id", flat=True))

    @classmethod
    def bulk_get(cls, ids: list[int]) -> list[User]:
        if len(ids) == 0:
            return []

        objs = cls.queryset().filter(id__in=ids)
        return sort_ids(objs, ids)

    @classmethod
    def create(cls, **kwargs) -> User:
        return User.objects.create_user(**kwargs)

    @classmethod
    def update(cls, obj: User, **kwargs) -> None:
        if not kwargs:
            return

        [set_attr(obj, key, value) for key, value in kwargs.items()]
        obj.save(update_fields=list(kwargs.keys()))

    @classmethod
    def update_profile(cls, obj: User, **kwargs) -> None:
        if not kwargs:
            return

        if not hasattr(obj, "profile"):
            return

        [set_attr(obj.profile, key, value) for key, value in kwargs.items()]
        obj.profile.save(update_fields=list(kwargs.keys()))

    @classmethod
    def update_mypage(cls, obj: User, **kwargs) -> None:
        if not kwargs:
            return

        if not hasattr(obj, "mypage"):
            return

        [set_attr(obj.mypage, key, value) for key, value in kwargs.items()]
        obj.mypage.save(update_fields=list(kwargs.keys()))

    @classmethod
    def update_notification(cls, obj: User, **kwargs) -> None:
        if not kwargs:
            return

        if not hasattr(obj, "notification"):
            return

        [set_attr(obj.notification, key, value) for key, value in kwargs.items()]
        obj.notification.save(update_fields=list(kwargs.keys()))
        return

    @classmethod
    def media_like(cls, user: User, obj: MediaModel) -> bool:
        is_like = obj.like.filter(id=user.id).exists()
        if is_like:
            obj.like.remove(user)
        else:
            obj.like.add(user)
        return not is_like

    @classmethod
    def comment_like(cls, user: User, obj: Comment) -> bool:
        is_like = obj.like.filter(id=user.id).exists()
        if is_like:
            obj.like.remove(user)
        else:
            obj.like.add(user)
        return not is_like
