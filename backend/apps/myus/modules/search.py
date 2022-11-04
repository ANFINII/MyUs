from datetime import datetime, timedelta
from functools import reduce
from itertools import chain
from operator import and_
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Count
from apps.myus.models import Video, Music, Picture, Blog, Chat
from apps.myus.modules.filter_data import DeferData

User = get_user_model()

def get_q_list(search):
    """除外リストを作成"""
    exclusion_list = set([' ', '　'])
    q_list = ''
    for q in search:
        # 半角と全角の空文字が含まれたら無視
        if q in exclusion_list:
            pass
        else:
            q_list += q
    return q_list


class SearchData:
    def search_index(search):
        result1 = Video.objects.search(search)[:8]
        result2 = Music.objects.search(search)[:8]
        result3 = Picture.objects.search(search)[:8]
        result4 = Blog.objects.search(search)[:8]
        result5 = Chat.objects.search(search)[:8]
        queryset_chain = chain(result1, result2, result3, result4, result5)
        return sorted(queryset_chain, key=lambda instance: instance.score(), reverse=True)

    def search_recommend(aggregation_date, search):
        result1 = Video.objects.filter(created__gte=aggregation_date).annotate(scr=F('read') + Count('like')*10 + F('read')*Count('like')/(F('read')+1)*20).filter(scr__gte=50).search(search)[:8]
        result2 = Music.objects.filter(created__gte=aggregation_date).annotate(scr=F('read') + Count('like')*10 + F('read')*Count('like')/(F('read')+1)*20).filter(scr__gte=50).search(search)[:8]
        result3 = Picture.objects.filter(created__gte=aggregation_date).annotate(scr=F('read') + Count('like')*10 + F('read')*Count('like')/(F('read')+1)*20).filter(scr__gte=50).search(search)[:8]
        result4 = Blog.objects.filter(created__gte=aggregation_date).annotate(scr=F('read') + Count('like')*10 + F('read')*Count('like')/(F('read')+1)*20).filter(scr__gte=50).search(search)[:8]
        result5 = Chat.objects.filter(created__gte=aggregation_date).annotate(scr=F('read') + Count('like')*10 + F('read')*Count('like')/(F('read')+1)*20).filter(scr__gte=50).search(search)[:8]
        queryset_chain = chain(result1, result2, result3, result4, result5)
        return sorted(queryset_chain, key=lambda instance: instance.score(), reverse=True)

    def search_userpage(author, search):
        result1 = Video.objects.filter(author=author, publish=True).search(search)
        result2 = Music.objects.filter(author=author, publish=True).search(search)
        result3 = Picture.objects.filter(author=author, publish=True).search(search)
        result4 = Blog.objects.filter(author=author, publish=True).search(search)
        result5 = Chat.objects.filter(author=author, publish=True).search(search)
        queryset_chain = chain(result1, result2, result3, result4, result5)
        return sorted(queryset_chain, key=lambda instance: instance.score(), reverse=True)

    def search_follow(model, path, user, search):
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

    def search_models(model, search):
        result = model.objects.filter(publish=True).order_by('-created')
        q_list = get_q_list(search)
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
        return result.filter(query).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/(F('read')+1)*20).order_by('-score').distinct()

    def search_todo(model, user, search):
        result = model.objects.filter(author=user.id)
        q_list = get_q_list(search)
        query = reduce(and_, [
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(duedate__icontains=q) for q in q_list
        ])
        return result.filter(query).order_by('-duedate').distinct()

    def search_advertise(model, author, search):
        result = model.objects.filter(author=author, publish=True).order_by('created')
        q_list = get_q_list(search)
        query = reduce(and_, [
            Q(title__icontains=q) |
            Q(content__icontains=q) for q in q_list
        ])
        return result.filter(query).order_by('created').distinct()


class Search:
    def search_index(self):
        search = self.request.GET.get('search')
        if search:
            result = SearchData.search_index(search)
            self.count = len(result)
            return result
        return Video.objects.none()

    def search_recommend(self):
        search = self.request.GET.get('search')
        if search:
            aggregation_date = datetime.today() - timedelta(days=200)
            result = SearchData.search_recommend(aggregation_date, search)
            self.count = len(result)
            return result
        return Video.objects.none()

    def search_userpage(self):
        search = self.request.GET.get('search')
        if search:
            author = get_object_or_404(User, nickname=self.kwargs['nickname'])
            result = SearchData.search_userpage(author, search)
            self.count = len(result)
            return result
        return Video.objects.none()

    def search_follow(self, model):
        path = self.request.path.lstrip('/')
        user = self.request.user
        search = self.request.GET.get('search')
        if search:
            result = SearchData.search_follow(model, path, user, search)
            self.count = result.count()
            return result
        if path == 'follow':
            return model.objects.filter(follower=user.id).exclude(following=user.id).select_related('following__mypage').defer(*DeferData.follow)
        if path == 'follower':
            return model.objects.filter(following=user.id).exclude(follower=user.id).select_related('follower__mypage').defer(*DeferData.follow)

    def search_models(self, model):
        search = self.request.GET.get('search')
        if search:
            result = SearchData.search_models(model, search)
            self.count = result.count()
            return result
        return model.objects.filter(publish=True).defer(*DeferData.defer_list).order_by('-created')

    def search_todo(self, model):
        user = self.request.user
        search = self.request.GET.get('search')
        if search:
            result = SearchData.search_todo(model, user, search)
            self.count = result.count()
            return result
        return model.objects.filter(author=user.id).defer(*DeferData.defer_list)

    def search_advertise(self, model):
        author = get_object_or_404(User, nickname=self.kwargs['nickname'])
        search = self.request.GET.get('search')
        if search:
            result = SearchData.search_advertise(model, author, search)
            self.count = result.count()
            return result
        return model.objects.filter(author=author, publish=True).order_by('created')
