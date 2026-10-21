from collections.abc import Callable
import pytest
from django.db import IntegrityError, transaction
from api.db.models.channel import Channel
from api.db.models.subscribe import Subscribe
from api.db.models.user import MyPage, User
from api.db.models.users import Follow
from api.src.usecase.follow import upsert_follow
from api.src.usecase.subscribe import upsert_subscribe
from api.src.usecase.user import get_user_data


def follow(follower: User, following: User, is_follow: bool) -> int:
    follower_ret = get_user_data(user_id=follower.id)
    assert follower_ret.is_ok, follower_ret
    follower_data = follower_ret.ok_value
    assert follower_data is not None

    ret = upsert_follow(follower_data, following.ulid, is_follow)
    assert ret.is_ok, ret
    dto = ret.ok_value
    return dto.follower_count


def subscribe(user: User, channel: Channel, is_subscribe: bool) -> int:
    ret = upsert_subscribe(user.id, channel.ulid, is_subscribe)
    assert ret.is_ok, ret
    dto = ret.ok_value
    return dto.count


def counts(follower: User, following: User) -> tuple[int, int]:
    return MyPage.objects.get(user=follower).following_count, MyPage.objects.get(user=following).follower_count


@pytest.mark.django_db
def test_follow_counts(make_user: Callable[[str], User]) -> None:
    alice = make_user("alice")
    bob = make_user("bob")

    assert follow(alice, bob, True) == 1
    assert counts(alice, bob) == (1, 1)

    assert follow(alice, bob, True) == 1
    assert counts(alice, bob) == (1, 1)

    assert follow(alice, bob, False) == 0
    assert counts(alice, bob) == (0, 0)

    assert follow(alice, bob, True) == 1
    assert counts(alice, bob) == (1, 1)
    assert Follow.objects.filter(follower=alice, following=bob).count() == 1


@pytest.mark.django_db
def test_subscribe_counts(make_user: Callable[[str], User]) -> None:
    alice = make_user("alice")
    bob = make_user("bob")
    channel = Channel.objects.create(owner=bob, name="bob", is_default=True)
    channel = Channel.objects.get(id=channel.id)

    assert subscribe(alice, channel, True) == 1
    assert subscribe(alice, channel, True) == 1
    assert subscribe(alice, channel, False) == 0
    assert subscribe(alice, channel, True) == 1

    assert Channel.objects.get(id=channel.id).count == 1
    assert Subscribe.objects.filter(user=alice, channel=channel).count() == 1


@pytest.mark.django_db
def test_duplicate_follow_and_subscribe_are_rejected(make_user: Callable[[str], User]) -> None:
    alice = make_user("alice")
    bob = make_user("bob")
    channel = Channel.objects.create(owner=bob, name="bob", is_default=True)
    Follow.objects.create(follower=alice, following=bob)
    Subscribe.objects.create(user=alice, channel=channel)

    with pytest.raises(IntegrityError), transaction.atomic():
        Follow.objects.create(follower=alice, following=bob)

    with pytest.raises(IntegrityError), transaction.atomic():
        Subscribe.objects.create(user=alice, channel=channel)
