from django.db.models import Q, F, Count
from functools import reduce
from operator import and_

def search_follow(self, model):
    result = model.objects.filter(follower_id=self.request.user.id)
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
