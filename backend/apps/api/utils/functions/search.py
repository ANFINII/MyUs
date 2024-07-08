from functools import reduce
from operator import and_

from django.db.models import Q, F, Count
from apps.myus.models import Music


def get_q_list(search: str) -> str:
    """除外リストを作成"""
    exclusion_list = {' ', '　'}
    return ''.join([q for q in search if q not in exclusion_list])


def search_models(model: any, search: str):
    result = model.objects.filter(publish=True).order_by('-created')
    q_list = get_q_list(search)
    score = F('read') + Count('like')*10 + F('read')*Count('like')/(F('read')+1)*20

    if model == Music:
        query = reduce(and_, [
            Q(title__icontains=q) |
            Q(hashtag__jp_name__icontains=q) |
            Q(author__nickname__icontains=q) |
            Q(content__icontains=q) |
            Q(lyric__icontains=q) for q in q_list
        ])
    else:
        query = reduce(and_, [
            Q(title__icontains=q) |
            Q(hashtag__jp_name__icontains=q) |
            Q(author__nickname__icontains=q) |
            Q(content__icontains=q) for q in q_list
        ])
    return result.filter(query).annotate(score=score).order_by('-score').distinct()
