from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Count
from functools import reduce
from operator import and_
from itertools import chain
from myusapp.models import VideoModel, LiveModel, MusicModel, PictureModel, BlogModel, ChatModel

User = get_user_model()

class Search:
    def search_index(self):
        search = self.request.GET.get('search', None)
        if search is not None:
            result1 = VideoModel.objects.search(search)
            result2 = LiveModel.objects.search(search)
            result3 = MusicModel.objects.search(search)
            result4 = PictureModel.objects.search(search)
            result5 = BlogModel.objects.search(search)
            result6 = ChatModel.objects.search(search)
            queryset_chain = chain(result1, result2, result3, result4, result5, result6)
            result = sorted(queryset_chain, key=lambda instance: instance.score(), reverse=True)
            self.count = len(result)
            return result
        return VideoModel.objects.none()

    def search_userpage(self):
        search = self.request.GET.get('search', None)
        author = get_object_or_404(User, nickname=self.kwargs['nickname'])
        if search is not None:
            result1 = VideoModel.objects.filter(author_id=author, publish=True).search(search)
            result2 = LiveModel.objects.filter(author_id=author, publish=True).search(search)
            result3 = MusicModel.objects.filter(author_id=author, publish=True).search(search)
            result4 = PictureModel.objects.filter(author_id=author, publish=True).search(search)
            result5 = BlogModel.objects.filter(author_id=author, publish=True).search(search)
            result6 = ChatModel.objects.filter(author_id=author, publish=True).search(search)
            queryset_chain = chain(result1, result2, result3, result4, result5, result6)
            result = sorted(queryset_chain, key=lambda instance: instance.score(), reverse=True)
            self.count = len(result)
            return result
        return VideoModel.objects.none()

    def search_follower(self, model):
        result = model.objects.filter(following_id=self.request.user.id).exclude(follower_id=self.request.user.id)
        search = self.request.GET.get('search')
        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(follower__nickname__icontains=q) |
                        Q(follower__introduction__icontains=q) for q in q_list]
                    )
            result = result.filter(query).distinct()
            self.count = len(result)
        return result

    def search_following(self, model):
        result = model.objects.filter(follower_id=self.request.user.id).exclude(following_id=self.request.user.id)
        search = self.request.GET.get('search')
        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(following__nickname__icontains=q) |
                        Q(following__introduction__icontains=q) for q in q_list]
                    )
            result = result.filter(query).distinct()
            self.count = len(result)
        return result

    def search_models(self, model):
        result = model.objects.filter(publish=True).order_by('-created')
        search = self.request.GET.get('search')
        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(title__icontains=q) |
                        Q(tags__tag__icontains=q) |
                        Q(author__nickname__icontains=q) |
                        Q(content__icontains=q) for q in q_list]
                    )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10).order_by('-score').distinct()
            self.count = len(result)
        return result

    def search_music(self, model):
        result = model.objects.filter(publish=True).order_by('-created')
        search = self.request.GET.get('search')
        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(title__icontains=q) |
                        Q(tags__tag__icontains=q) |
                        Q(author__nickname__icontains=q) |
                        Q(content__icontains=q) |
                        Q(lyrics__icontains=q) for q in q_list]
                    )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10).order_by('-score').distinct()
            self.count = len(result)
        return result

    def search_blog(self, model):
        result = model.objects.filter(publish=True).order_by('-created')
        search = self.request.GET.get('search')
        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(title__icontains=q) |
                        Q(tags__tag__icontains=q) |
                        Q(author__nickname__icontains=q) |
                        Q(content__icontains=q) |
                        Q(richtext__icontains=q) for q in q_list]
                    )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10).order_by('-score').distinct()
            self.count = len(result)
        return result

    def search_todo(self, model):
        result = model.objects.filter(author_id=self.request.user.id)
        search = self.request.GET.get('search')
        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(title__icontains=q) |
                        Q(content__icontains=q) |
                        Q(duedate__icontains=q) for q in q_list]
                    )
            result = result.filter(query).order_by('-duedate').distinct()
            self.count = len(result)
        return result
