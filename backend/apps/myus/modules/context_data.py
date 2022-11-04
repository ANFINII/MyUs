from datetime import datetime, timedelta, date
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import F, Count, Exists, OuterRef
from apps.myus.models import MyPage, SearchTag, NotificationSetting, Follow, Comment
from apps.myus.models import Video, Music, Picture, Blog, Chat, Collabo, Todo, Advertise
from apps.myus.modules.contains import model_dict
from apps.myus.modules.notification import notification_data

User = get_user_model()

class ContextData:
    def context_data(self, models, **kwargs):
        context = super(models, self).get_context_data(**kwargs)
        user = self.request.user
        if user.id:
            notification_list = notification_data(self)
            context['notification_list'] = notification_list['notification_list']
            context['notification_count'] = notification_list['notification_count']
            context['searchtag_list'] = SearchTag.objects.filter(author=user).order_by('sequence')[:20]

        if hasattr(self, 'count'):
            context['count'] = self.count or 0
            context['query'] = self.request.GET.get('search')

        if 'NotificationSettingView' in str(models.__name__):
            context['notification_setting_list'] = NotificationSetting.objects.filter(user=user.id)

        if 'ProfileUpdate' in str(models.__name__):
            context['gender'] = {'0':'男性', '1':'女性', '2':'秘密'}

        if 'MyPageView' in str(models.__name__):
            context['mypage_list'] = MyPage.objects.filter(user=user.id)

        if 'Index' in str(models.__name__):
            context.update({
                f'{value}_list': model.objects.filter(publish=True).order_by('-created')[:8]
                for model, value in model_dict.items()
            })

        if 'Recommend' in str(models.__name__):
            # 急上昇はcreatedが1日以内かつscoreが100000以上の上位8レコード
            # テストはcreatedが100日以内かつscoreが50以上の上位8レコード
            # socre = (read + like*10) + read * like/(read+1)*20
            aggregation_date = datetime.today() - timedelta(days=500)
            score = F('read') + Count('like')*10 + F('read')*Count('like')/(F('read')+1)*20
            context['Recommend'] = 'Recommend'
            context.update({
                f'{value}_list': model.objects.annotate(score=score).filter(publish=True, created__gte=aggregation_date, score__gte=50).order_by('-score')[:8]
                for model, value in model_dict.items()
            })

        if ('UserPage' or 'UserPageInfo' or 'UserPageAdvertise') in str(models.__name__):
            author = get_object_or_404(User, nickname=self.kwargs['nickname'])
            follow = Follow.objects.filter(follower=user.id, following=author)
            context['is_follow'] = follow.exists()
            context['author_name'] = author.nickname
            context['user_list'] = User.objects.filter(id=author.id)
            context.update({
                f'{value}_list': model.objects.filter(author=author, publish=True).order_by('-created')
                for model, value in model_dict.items()
            })
        return context


    def models_context_data(self, models, **kwargs):
        context = super(models, self).get_context_data(**kwargs)
        user = self.request.user
        obj = self.object
        author = obj.author
        follow = Follow.objects.filter(follower=user.id, following=author)
        context['user_id'] = user.id
        context['obj_id'] = obj.id
        context['obj_path'] = self.request.path
        context['is_follow'] = follow.exists()

        filter_kwargs = {'id': OuterRef('pk'), 'like': user.id}
        subquery = Comment.objects.filter(**filter_kwargs)
        comment = obj.comment.filter(parent__isnull=True).annotate(is_comment_like=Exists(subquery))
        context['comment_list'] = comment.select_related('author').prefetch_related('like')
        context['reply_list'] = comment.select_related('author', 'parent').prefetch_related('like')

        if user.id:
            notification_list = notification_data(self)
            context['notification_list'] = notification_list['notification_list']
            context['notification_count'] = notification_list['notification_count']
            context['searchtag_list'] = SearchTag.objects.filter(author=user).order_by('sequence')[:20]

        context['advertise_auto_list'] = Advertise.objects.filter(publish=True, type=0).order_by('?')[:1]
        advertise = Advertise.objects.filter(publish=True, type=1, author=author).order_by('?')
        if author.mypage.plan == 'basic':
            context['advertise_list'] = advertise[:1]
        if author.mypage.plan == 'standard':
            context['advertise_list'] = advertise[:3]
        if author.mypage.plan == 'premium':
            context['advertise_list'] = advertise[:4]

        if 'VideoDetail' in str(models.__name__):
            context['video_list'] = Video.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50]

        if 'MusicDetail' in str(models.__name__):
            context['music_list'] = Music.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50]

        if 'PictureDetail' in str(models.__name__):
            context['picture_list'] = Picture.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50]

        if 'BlogDetail' in str(models.__name__):
            context['blog_list'] = Blog.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50]

        if 'ChatDetail' in str(models.__name__):
            context['is_period'] = obj.period < date.today()
            context['comment_list'] = obj.message.filter(parent__isnull=True).select_related('author')
            context['chat_list'] = Chat.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50]

        if 'ChatThread' in str(models.__name__):
            comment_id = self.kwargs['comment_id']
            context['comment_id'] = comment_id
            context['comment_parent'] = obj.message.filter(id=comment_id)
            context['reply_list'] = obj.message.filter(parent_id=comment_id).select_related('author')
            context['chat_list'] = Chat.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50]

        if 'CollaboDetail' in str(models.__name__):
            context['is_period'] = obj.period < date.today()
            context['collabo_list'] = Collabo.objects.filter(publish=True).exclude(id=obj.id).select_related('author').order_by('-created')[:50]

        if 'TodoDetail' in str(models.__name__):
            context['todo_list'] = Todo.objects.filter(author=user).exclude(id=obj.id)[:50]

        if 'TodoDetail' not in str(models.__name__):
            context['liked'] = obj.like.filter(id=user.id).exists()
        return context
