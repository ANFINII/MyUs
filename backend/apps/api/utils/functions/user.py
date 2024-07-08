from config.settings.base import DOMAIN_URL
from apps.api.types.user import Author


def get_author(author: Author) -> dict:
    data = {
        'id': author.id,
        'nickname': author.nickname,
        'image': f'{DOMAIN_URL}{author.image()}',
    }
    return data
