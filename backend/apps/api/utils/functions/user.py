from config.settings.base import DOMAIN_URL
from apps.api.types.user import Author, MediaUser
from apps.myus.models import Follow


def get_author(author: Author) -> dict:
    data = {
        'avatar': f'{DOMAIN_URL}{author.image()}',
        'nickname': author.nickname,
        'follower_count': author.mypage.follower_count,
    }
    return data


def get_media_user(user: MediaUser, obj) -> dict:
    data = {
        'avatar': f'{DOMAIN_URL}{user.image()}',
        'nickname': user.nickname,
        'is_like': obj.like.filter(id=user.id).exists(),
        'is_follow': Follow.objects.filter(follower=user.id, following=obj.author).exists()
    }
    return data


def get_notification_user(user: MediaUser) -> dict:
    data = {
        'avatar': f'{DOMAIN_URL}{user.image()}',
        'nickname': user.nickname,
    }
    return data
