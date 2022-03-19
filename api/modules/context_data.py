from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import F, Count, Exists, OuterRef
from django.db.models.query import QuerySet
from itertools import chain
from api.models import SearchTag, NotificationSetting, Notification, Comment, Follow
from api.models import Video, Live, Music, Picture, Blog, Chat, Collabo, Todo, Advertise
import datetime

User = get_user_model()

def notification_data(self):
    user_id = self.request.user.id
    notification_obj, notification_obj_list_1, notification_obj_list_2 = QuerySet, [], []
    notification_list_1, notification_list_confirmed = [], []
    confirmed_kwargs = {}
    confirmed_kwargs['id'] = OuterRef('pk')
    confirmed_kwargs['confirmed'] = user_id
    subquery_confirmed = Notification.objects.filter(**confirmed_kwargs)
    following_list = list(Follow.objects.filter(follower_id=user_id).values_list('following_id', 'created'))
    if user_id is not None:
        notification_obj = NotificationSetting.objects.get(user_id=user_id)
        if notification_obj.is_video:
            notification_obj_list_1 += [1]
        if notification_obj.is_live:
            notification_obj_list_1 += [2]
        if notification_obj.is_music:
            notification_obj_list_1 += [3]
        if notification_obj.is_picture:
            notification_obj_list_1 += [4]
        if notification_obj.is_blog:
            notification_obj_list_1 += [5]
        if notification_obj.is_chat:
            notification_obj_list_1 += [6]
        if notification_obj.is_collabo:
            notification_obj_list_1 += [7]
        if notification_obj.is_follow:
            notification_obj_list_2 += [8]
        if notification_obj.is_like:
            notification_obj_list_2 += [9]
        if notification_obj.is_reply:
            notification_obj_list_2 += [10]
        if notification_obj.is_views:
            notification_obj_list_2 += [11]
        for id, dates in following_list:
            notification_list_1 += Notification.objects.filter(user_from_id__in=[id], created__gt=dates, user_to_id=None, type_no__in=notification_obj_list_1).exclude(deleted=user_id).annotate(user_confirmed=Exists(subquery_confirmed)).order_by('-created')
            notification_list_confirmed += Notification.objects.filter(user_from_id__in=[id], created__gt=dates, user_to_id=None, type_no__in=notification_obj_list_1).exclude(deleted=user_id, confirmed=user_id).annotate(user_confirmed=Exists(subquery_confirmed)).order_by('-created')
        notification_list_2 = Notification.objects.filter(user_to_id=user_id, type_no__in=notification_obj_list_2).exclude(deleted=user_id).annotate(user_confirmed=Exists(subquery_confirmed)).order_by('-created')
        notification_list_data = {
            'notification_count': len(list(chain(notification_list_confirmed, notification_list_2.exclude(confirmed=user_id)))),
            'notification_list': list(chain(notification_list_1, notification_list_2)),
        }
        return notification_list_data

class ContextData:
    def context_data(self, models, **kwargs):
        context = super(models, self).get_context_data(**kwargs)
        user = self.request.user
        user_id = self.request.user.id
        if user_id is not None:
            notification_list = notification_data(self)
            context['notification_count'] = notification_list['notification_count']
            context['notification_list'] = notification_list['notification_list']
        try:
            context['count'] = self.count or 0
        except AttributeError:
            pass
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=user_id).order_by('sequence')[:20],
        })
        if 'Notification' in str(models.__name__):
            context.update(notification_setting_list=NotificationSetting.objects.filter(user_id=user_id))

        if 'ProfileUpdate' in str(models.__name__):
            context['gender'] = {'0':'男性', '1':'女性', '2':'秘密'}

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
            aggregation_date = datetime.datetime.today() - datetime.timedelta(days=100)
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
            author_id = author.id
            follow = Follow.objects.filter(follower=self.request.user.id).filter(following=author_id)
            followed = False
            if follow.exists():
                followed = True
            context['followed'] = followed
            context['author_name'] = author.nickname
            context.update({
                'user_list': User.objects.filter(id=author_id),
                'video_list': Video.objects.filter(author_id=author_id, publish=True),
                'live_list': Live.objects.filter(author_id=author_id, publish=True),
                'music_list': Music.objects.filter(author_id=author_id, publish=True),
                'picture_list': Picture.objects.filter(author_id=author_id, publish=True),
                'blog_list': Blog.objects.filter(author_id=author_id, publish=True),
                'chat_list': Chat.objects.filter(author_id=author_id, publish=True),
            })
        return context


    def models_context_data(self, models, **kwargs):
        context = super(models, self).get_context_data(**kwargs)
        obj = self.object
        user_id = self.request.user.id
        follow = Follow.objects.filter(follower=user_id).filter(following=obj.author.id)
        followed = False
        if follow.exists():
            followed = True
        liked = False
        if 'TodoDetail' not in str(models.__name__):
            if obj.like.filter(id=user_id).exists():
                liked = True
        if 'Chat' not in str(models.__name__):
            filter_kwargs = {}
            filter_kwargs['id'] = OuterRef('pk')
            filter_kwargs['like'] = user_id
            subquery = Comment.objects.filter(**filter_kwargs)
            context['comment_list'] = obj.comment.filter(parent__isnull=True).annotate(reply_count=Count('reply')).annotate(comment_liked=Exists(subquery)).select_related('author', 'content_type')
            context['reply_list'] = obj.comment.filter(parent__isnull=False).annotate(comment_liked=Exists(subquery)).select_related('author', 'parent', 'content_type')
        else:
            if obj.period < datetime.date.today():
                is_period = True
            else:
                is_period = False
            context['is_period'] = is_period
            context['comment_list'] = obj.comment.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        if user_id is not None:
            notification_list = notification_data(self)
            context['notification_count'] = notification_list['notification_count']
            context['notification_list'] = notification_list['notification_list']
        if obj.author.mypage.rate_plan == '1':
            context.update(advertise_list=Advertise.objects.filter(publish=True, type=1, author=obj.author.id).order_by('?')[:1])
        if obj.author.mypage.rate_plan == '2':
            context.update(advertise_list=Advertise.objects.filter(publish=True, type=1, author=obj.author.id).order_by('?')[:3])
        if obj.author.mypage.rate_plan == '3':
            context.update(advertise_list=Advertise.objects.filter(publish=True, type=1, author=obj.author.id).order_by('?')[:4])
        context['liked'] = liked
        context['followed'] = followed
        context['user_id'] = user_id
        context['obj_id'] = obj.id
        context['obj_path'] = self.request.path
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=user_id).order_by('sequence')[:20],
            'advertise_auto_list': Advertise.objects.filter(publish=True, type=0).order_by('?')[:1],
        })
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
            context['comment_parent'] = obj.comment.filter(id=comment_id).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
            context['reply_list'] = obj.comment.filter(parent__isnull=False, parent_id=comment_id).select_related('author', 'parent', 'content_type')
            context.update(chat_list=Chat.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'CollaboDetail' in str(models.__name__):
            if obj.period < datetime.date.today():
                is_period = True
            else:
                is_period = False
            context['is_period'] = is_period
            context.update(collabo_list=Collabo.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'TodoDetail' in str(models.__name__):
            context.update(todo_list=Todo.objects.filter(author_id=user_id).exclude(id=obj.id)[:50])
        return context
