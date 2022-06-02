import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import F, Count, Exists, OuterRef
from api.models import MyPage, NotificationSetting, SearchTag, Follow, Comment
from api.models import Video, Live, Music, Picture, Blog, Chat, Collabo, Todo, Advertise
from api.modules.notification import notification_data

User = get_user_model()

class ContextData:
    def context_data(self, models, **kwargs):
        context = super(models, self).get_context_data(**kwargs)
        user = self.request.user
        if user.id is not None:
            notification_list = notification_data(self)
            context['notification_list'] = notification_list['notification_list']
            context['notification_count'] = notification_list['notification_count']
            context['searchtag_list'] = SearchTag.objects.filter(author=user).order_by('sequence')[:20]
        if hasattr(self, 'count'):
            context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        if 'NotificationSettingView' in str(models.__name__):
            context.update(notification_setting_list=NotificationSetting.objects.filter(user=user.id))

        if 'ProfileUpdate' in str(models.__name__):
            context['gender'] = {'0':'男性', '1':'女性', '2':'秘密'}

        if 'MyPageView' in str(models.__name__):
            context.update(mypage_list=MyPage.objects.filter(user=user.id))

        if 'Index' in str(models.__name__):
            context.update({
                'video_list': Video.objects.filter(publish=True).order_by('-created')[:8],
                'live_list': Live.objects.filter(publish=True).order_by('-created')[:8],
                'music_list': Music.objects.filter(publish=True).order_by('-created')[:8],
                'picture_list': Picture.objects.filter(publish=True).order_by('-created')[:8],
                'blog_list': Blog.objects.filter(publish=True).order_by('-created')[:8],
                'chat_list': Chat.objects.filter(publish=True).order_by('-created')[:8],
            })

        if 'Recommend' in str(models.__name__):
            # 急上昇はcreatedが1日以内かつscoreが100000以上の上位8レコード
            # テストはcreatedが100日以内かつscoreが50以上の上位8レコード
            # socre = (read + like*10) + read * like/read * 20
            aggregation_date = datetime.datetime.today() - datetime.timedelta(days=200)
            context['Recommend'] = 'Recommend'
            context.update({
                'video_list': Video.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'live_list': Live.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'music_list': Music.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'picture_list': Picture.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'blog_list': Blog.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'chat_list': Chat.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
            })

        if ('UserPage' or 'UserPageInfo' or 'UserPageAdvertise') in str(models.__name__):
            author = get_object_or_404(User, nickname=self.kwargs['nickname'])
            follow = Follow.objects.filter(follower=self.request.user.id, following=author)
            followed = False
            if follow.exists():
                followed = True
            context['followed'] = followed
            context['author_name'] = author.nickname
            context.update({
                'user_list': User.objects.filter(id=author.id),
                'video_list': Video.objects.filter(author=author, publish=True).order_by('-created'),
                'live_list': Live.objects.filter(author=author, publish=True).order_by('-created'),
                'music_list': Music.objects.filter(author=author, publish=True).order_by('-created'),
                'picture_list': Picture.objects.filter(author=author, publish=True).order_by('-created'),
                'blog_list': Blog.objects.filter(author=author, publish=True).order_by('-created'),
                'chat_list': Chat.objects.filter(author=author, publish=True).order_by('-created'),
            })
        return context


    def models_context_data(self, models, **kwargs):
        context = super(models, self).get_context_data(**kwargs)
        obj = self.object
        user = self.request.user
        follow = Follow.objects.filter(follower=user.id, following=obj.author)
        followed = False
        if follow.exists():
            followed = True
        liked = False
        if 'TodoDetail' not in str(models.__name__):
            if obj.like.filter(id=user.id).exists():
                liked = True
        if 'ChatDetail' in str(models.__name__):
            if obj.period < datetime.date.today():
                is_period = True
            else:
                is_period = False
            context['is_period'] = is_period
            context['comment_list'] = obj.comment.filter(parent__isnull=True).select_related('author')
        else:
            filter_kwargs = {'id': OuterRef('pk'), 'like': user.id}
            subquery = Comment.objects.filter(**filter_kwargs)
            context['comment_list'] = obj.comment.filter(parent__isnull=True).annotate(comment_liked=Exists(subquery)).select_related('author').prefetch_related('like')
            context['reply_list'] = obj.comment.filter(parent__isnull=False).annotate(comment_liked=Exists(subquery)).select_related('author', 'parent').prefetch_related('like')
        if user.id is not None:
            notification_list = notification_data(self)
            context['notification_list'] = notification_list['notification_list']
            context['notification_count'] = notification_list['notification_count']
            context['searchtag_list'] = SearchTag.objects.filter(author=user).order_by('sequence')[:20]
        if obj.author.mypage.rate_plan == '1':
            context.update(advertise_list=Advertise.objects.filter(publish=True, type=1, author=obj.author).order_by('?')[:1])
        if obj.author.mypage.rate_plan == '2':
            context.update(advertise_list=Advertise.objects.filter(publish=True, type=1, author=obj.author).order_by('?')[:3])
        if obj.author.mypage.rate_plan == '3':
            context.update(advertise_list=Advertise.objects.filter(publish=True, type=1, author=obj.author).order_by('?')[:4])
        context['liked'] = liked
        context['followed'] = followed
        context['user_id'] = user.id
        context['obj_id'] = obj.id
        context['obj_path'] = self.request.path
        context['advertise_auto_list'] = Advertise.objects.filter(publish=True, type=0).order_by('?')[:1]
        if 'VideoDetail' in str(models.__name__):
            context.update(video_list=Video.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'LiveDetail' in str(models.__name__):
            context.update(live_list=Live.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'MusicDetail' in str(models.__name__):
            context.update(music_list=Music.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'PictureDetail' in str(models.__name__):
            context.update(picture_list=Picture.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'BlogDetail' in str(models.__name__):
            context.update(blog_list=Blog.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'ChatDetail' in str(models.__name__):
            context.update(chat_list=Chat.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'ChatThread' in str(models.__name__):
            comment_id = self.kwargs['comment_id']
            context['comment_id'] = comment_id
            context['comment_parent'] = obj.comment.filter(id=comment_id)
            context['reply_list'] = obj.comment.filter(parent_id=comment_id).select_related('author')
            context.update(chat_list=Chat.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'CollaboDetail' in str(models.__name__):
            if obj.period < datetime.date.today():
                is_period = True
            else:
                is_period = False
            context['is_period'] = is_period
            context.update(collabo_list=Collabo.objects.filter(publish=True).exclude(id=obj.id).select_related('author').order_by('-created')[:50])

        if 'TodoDetail' in str(models.__name__):
            context.update(todo_list=Todo.objects.filter(author=user).exclude(id=obj.id)[:50])
        return context
