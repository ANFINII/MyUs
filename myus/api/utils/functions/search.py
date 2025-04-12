from functools import reduce
from operator import and_
from django.db.models import Q, F, Count
from api.models import User, Music


def get_q_list(search: str) -> str:
    """除外リストを作成"""
    exclusion_list = {' ', '　'}
    return ''.join([q for q in search if q not in exclusion_list])


def search_q_list(search: str) -> Q:
    q_list = get_q_list(search)
    query = reduce(and_, [
        Q(title__icontains=q) |
        Q(hashtag__jp_name__icontains=q) |
        Q(author__nickname__icontains=q) |
        Q(content__icontains=q) for q in q_list
    ])
    return query


def search_follow(model: any, path: str, user: User, search: str):
    q_list = get_q_list(search)
    if path == 'follow':
        result = model.objects.filter(follower=user.id).exclude(following=user.id).select_related('following__mypage')
        query = reduce(and_, [
            Q(following__nickname__icontains=q) |
            Q(following__introduction__icontains=q) for q in q_list
        ])
    if path == 'follower':
        result = model.objects.filter(following=user.id).exclude(follower=user.id).select_related('follower__mypage')
        query = reduce(and_, [
            Q(follower__nickname__icontains=q) |
            Q(follower__introduction__icontains=q) for q in q_list
        ])
    return result.filter(query).distinct()


def search_media(model: any, search: str):
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
