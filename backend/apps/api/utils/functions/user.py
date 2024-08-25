from config.settings.base import DOMAIN_URL
from apps.api.types.user import Author, MediaUser


def get_author(author: Author) -> dict:
    data = {
        'nickname': author.nickname,
        'image': f'{DOMAIN_URL}{author.image()}',
        'follower_count': author.mypage.follower_count,
    }
    return data


def get_media_user(user: MediaUser, obj) -> dict:
    data = {
        'nickname': user.nickname,
        'image': f'{DOMAIN_URL}{user.image()}',
        'is_like': obj.like.filter(id=user.id).exists(),
    }
    return data
