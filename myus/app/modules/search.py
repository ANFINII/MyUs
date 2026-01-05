from datetime import datetime, timedelta
from functools import reduce
from itertools import chain
from operator import and_
from django.contrib.auth import get_user_model
from django.db.models import Q, F, Count
from api.db.models import Video, Music
from api.utils.constant import model_list
from api.utils.filter_data import DeferData


User = get_user_model()


def get_q_list(search):
    """除外リストを作成"""
    exclusion_list = {" ", "　"}
    return "".join([q for q in search if q not in exclusion_list])


class SearchData:
    def media_query(model, search):
        """メディア検索用の Q を生成"""
        q_list = get_q_list(search)
        if not q_list:
            return Q()
        if model == Music:
            return reduce(and_, [
                Q(title__icontains=q) |
                Q(hashtag__jp_name__icontains=q) |
                Q(author__nickname__icontains=q) |
                Q(content__icontains=q) |
                Q(lyric__icontains=q) for q in q_list
            ])
        return reduce(and_, [
            Q(title__icontains=q) |
            Q(hashtag__jp_name__icontains=q) |
            Q(author__nickname__icontains=q) |
            Q(content__icontains=q) for q in q_list
        ])

    def search_index(search):
        result = [
            model.objects.filter(publish=True).filter(SearchData.media_query(model, search)).distinct()[:8]
            for model in model_list
        ]
        queryset_chain = chain(*result)
        return sorted(queryset_chain, key=lambda instance: instance.score(), reverse=True)

    def search_recommend(aggregation_date, search):
        score = F("read") + Count("like")*10 + F("read")*Count("like")/(F("read")+1)*20
        result = [
            model.objects.filter(publish=True, created__gte=aggregation_date)
            .annotate(scr=score).filter(scr__gte=50)
            .filter(SearchData.media_query(model, search)).distinct()[:8]
            for model in model_list
        ]
        queryset_chain = chain(*result)
        return sorted(queryset_chain, key=lambda instance: instance.score(), reverse=True)

    def search_userpage(author, search):
        result = [
            model.objects.filter(author=author, publish=True)
            .filter(SearchData.media_query(model, search)).distinct()
            for model in model_list
        ]
        queryset_chain = chain(*result)
        return sorted(queryset_chain, key=lambda instance: instance.score(), reverse=True)

    def search_follow(model, path, user, search):
        q_list = get_q_list(search)
        if path == "follow":
            result = model.objects.filter(follower=user.id).exclude(following=user.id).select_related("following__mypage")
            query = reduce(and_, [
                Q(following__nickname__icontains=q) |
                Q(following__introduction__icontains=q) for q in q_list
            ])
        if path == "follower":
            result = model.objects.filter(following=user.id).exclude(follower=user.id).select_related("follower__mypage")
            query = reduce(and_, [
                Q(follower__nickname__icontains=q) |
                Q(follower__introduction__icontains=q) for q in q_list
            ])
        return result.filter(query).distinct()

    def search_models(model, search):
        result = model.objects.filter(publish=True).order_by("-created")
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
        return result.filter(query).annotate(score=F("read") + Count("like")*10 + F("read")*Count("like")/(F("read")+1)*20).order_by("-score").distinct()

    def search_advertise(model, author, search):
        result = model.objects.filter(author=author, publish=True).order_by("created")
        q_list = get_q_list(search)
        query = reduce(and_, [
            Q(title__icontains=q) |
            Q(content__icontains=q) for q in q_list
        ])
        return result.filter(query).order_by("created").distinct()


class Search:
    def search_index(self):
        search = self.request.GET.get("search")
        if search:
            result = SearchData.search_index(search)
            self.count = len(result)
            return result
        return Video.objects.none()

    def search_recommend(self):
        search = self.request.GET.get("search")
        if search:
            aggregation_date = datetime.today() - timedelta(days=200)
            result = SearchData.search_recommend(aggregation_date, search)
            self.count = len(result)
            return result
        return Video.objects.none()

    def search_userpage(self):
        search = self.request.GET.get("search")
        if search:
            author = User.objects.get(nickname=self.kwargs["nickname"])
            result = SearchData.search_userpage(author, search)
            self.count = len(result)
            return result
        return Video.objects.none()

    def search_follow(self, model):
        path = self.request.path.lstrip("/")
        user = self.request.user
        search = self.request.GET.get("search")
        if search:
            result = SearchData.search_follow(model, path, user, search)
            self.count = result.count()
            return result
        if path == "follow":
            return model.objects.filter(follower=user.id).exclude(following=user.id).select_related("following__mypage").defer(*DeferData.follow)
        if path == "follower":
            return model.objects.filter(following=user.id).exclude(follower=user.id).select_related("follower__mypage").defer(*DeferData.follow)

    def search_models(self, model):
        search = self.request.GET.get("search")
        if search:
            result = SearchData.search_models(model, search)
            self.count = result.count()
            return result
        return model.objects.filter(publish=True).defer(*DeferData.defer_list).order_by("-created")

    def search_advertise(self, model):
        author = User.objects.get(nickname=self.kwargs["nickname"])
        search = self.request.GET.get("search")
        if search:
            result = SearchData.search_advertise(model, author, search)
            self.count = result.count()
            return result
        return model.objects.filter(author=author, publish=True).order_by("created")
