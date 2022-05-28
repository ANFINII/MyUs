import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Count
from functools import reduce
from operator import and_
from itertools import chain
from api.models import Video, Live, Music, Picture, Blog, Chat

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


class Search:
    def search_index(self):
        search = self.request.GET.get('search')
        if search:
            result1 = Video.objects.search(search)[:8]
            result2 = Live.objects.search(search)[:8]
            result3 = Music.objects.search(search)[:8]
            result4 = Picture.objects.search(search)[:8]
            result5 = Blog.objects.search(search)[:8]
            result6 = Chat.objects.search(search)[:8]
            queryset_chain = chain(result1, result2, result3, result4, result5, result6)
            result = sorted(queryset_chain, key=lambda instance: instance.score(), reverse=True)
            self.count = len(result)
            return result
        return Video.objects.none()

    def search_recommend(self):
        aggregation_date = datetime.datetime.today() - datetime.timedelta(days=100)
        search = self.request.GET.get('search')
        if search:
            result1 = Video.objects.filter(created__gte=aggregation_date).annotate(scr=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(scr__gte=50).search(search)[:8]
            result2 = Live.objects.filter(created__gte=aggregation_date).annotate(scr=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(scr__gte=50).search(search)[:8]
            result3 = Music.objects.filter(created__gte=aggregation_date).annotate(scr=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(scr__gte=50).search(search)[:8]
            result4 = Picture.objects.filter(created__gte=aggregation_date).annotate(scr=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(scr__gte=50).search(search)[:8]
            result5 = Blog.objects.filter(created__gte=aggregation_date).annotate(scr=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(scr__gte=50).search(search)[:8]
            result6 = Chat.objects.filter(created__gte=aggregation_date).annotate(scr=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(scr__gte=50).search(search)[:8]
            queryset_chain = chain(result1, result2, result3, result4, result5, result6)
            result = sorted(queryset_chain, key=lambda instance: instance.score(), reverse=True)
            self.count = len(result)
            return result
        return Video.objects.none()

    def search_userpage(self):
        author = get_object_or_404(User, nickname=self.kwargs['nickname'])
        search = self.request.GET.get('search')
        if search:
            result1 = Video.objects.filter(author=author, publish=True).search(search)
            result2 = Live.objects.filter(author=author, publish=True).search(search)
            result3 = Music.objects.filter(author=author, publish=True).search(search)
            result4 = Picture.objects.filter(author=author, publish=True).search(search)
            result5 = Blog.objects.filter(author=author, publish=True).search(search)
            result6 = Chat.objects.filter(author=author, publish=True).search(search)
            queryset_chain = chain(result1, result2, result3, result4, result5, result6)
            result = sorted(queryset_chain, key=lambda instance: instance.score(), reverse=True)
            self.count = len(result)
            return result
        return Video.objects.none()

    def search_follow(self, model):
        path = self.request.path
        user = self.request.user
        if '/follow' in path:
            result = model.objects.filter(follower=user.id).exclude(following=user.id).select_related('following__mypage')
        if '/follower' in path:
            result = model.objects.filter(following=user.id).exclude(follower=user.id).select_related('follower__mypage')
        search = self.request.GET.get('search', None)
        if search:
            q_list = get_q_list(search)
            query = reduce(and_, [
                Q(following__nickname__icontains=q) |
                Q(following__introduction__icontains=q) |
                Q(follower__nickname__icontains=q) |
                Q(follower__introduction__icontains=q) for q in q_list]
            )
            result = result.filter(query).distinct()
            self.count = len(result)
        return result

    def search_models(self, model):
        result = model.objects.filter(publish=True).order_by('-created')
        search = self.request.GET.get('search')
        if search:
            q_list = get_q_list(search)
            query = reduce(and_, [
                Q(title__icontains=q) |
                Q(hashtag__jp_name__icontains=q) |
                Q(author__nickname__icontains=q) |
                Q(content__icontains=q) for q in q_list]
            )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).order_by('-score').distinct()
            self.count = len(result)
        return result

    def search_music(self, model):
        result = model.objects.filter(publish=True).order_by('-created')
        search = self.request.GET.get('search')
        if search:
            q_list = get_q_list(search)
            query = reduce(and_, [
                Q(title__icontains=q) |
                Q(hashtag__jp_name__icontains=q) |
                Q(author__nickname__icontains=q) |
                Q(content__icontains=q) |
                Q(lyric__icontains=q) for q in q_list]
            )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).order_by('-score').distinct()
            self.count = len(result)
        return result

    def search_blog(self, model):
        result = model.objects.filter(publish=True).order_by('-created')
        search = self.request.GET.get('search')
        if search:
            q_list = get_q_list(search)
            query = reduce(and_, [
                Q(title__icontains=q) |
                Q(hashtag__jp_name__icontains=q) |
                Q(author__nickname__icontains=q) |
                Q(content__icontains=q) |
                Q(richtext__icontains=q) for q in q_list]
            )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).order_by('-score').distinct()
            self.count = len(result)
        return result

    def search_todo(self, model):
        result = model.objects.filter(author=self.request.user.id)
        search = self.request.GET.get('search')
        if search:
            q_list = get_q_list(search)
            query = reduce(and_, [
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(duedate__icontains=q) for q in q_list]
            )
            result = result.filter(query).order_by('-duedate').distinct()
            self.count = len(result)
        return result

    def search_advertise(self, model):
        author = get_object_or_404(User, nickname=self.kwargs['nickname'])
        result = model.objects.filter(author=author, publish=True).order_by('created')
        search = self.request.GET.get('search')
        if search:
            q_list = get_q_list(search)
            query = reduce(and_, [
                Q(title__icontains=q) |
                Q(content__icontains=q) for q in q_list]
            )
            result = result.filter(query).order_by('created').distinct()
            self.count = len(result)
        return result
