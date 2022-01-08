from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import F, Count, Exists, OuterRef
from django.db.models.query import QuerySet
from itertools import chain
from myus.models import SearchTagModel, NotifySettingModel, NotificationModel, CommentModel, FollowModel, TodoModel
from myus.models import VideoModel, LiveModel, MusicModel, PictureModel, BlogModel, ChatModel, CollaboModel, AdvertiseModel
import datetime

User = get_user_model()

def notify_data(self):
    user_id = self.request.user.id
    notify_obj, notify_obj_list_1, notify_obj_list_2 = QuerySet, [], []
    notify_list_1, notify_list_confirmed = [], []
    confirmed_kwargs = {}
    confirmed_kwargs['id'] = OuterRef('pk')
    confirmed_kwargs['confirmed'] = user_id
    subquery_confirmed = NotificationModel.objects.filter(**confirmed_kwargs)
    following_list = list(FollowModel.objects.filter(follower_id=user_id).values_list('following_id', 'created'))
    if user_id is not None:
        notify_obj = NotifySettingModel.objects.get(owner_id=user_id)
        if notify_obj.video:
            notify_obj_list_1 += [1]
        if notify_obj.live:
            notify_obj_list_1 += [2]
        if notify_obj.music:
            notify_obj_list_1 += [3]
        if notify_obj.picture:
            notify_obj_list_1 += [4]
        if notify_obj.blog:
            notify_obj_list_1 += [5]
        if notify_obj.chat:
            notify_obj_list_1 += [6]
        if notify_obj.collabo:
            notify_obj_list_1 += [7]
        if notify_obj.follow:
            notify_obj_list_2 += [8]
        if notify_obj.like:
            notify_obj_list_2 += [9]
        if notify_obj.reply:
            notify_obj_list_2 += [10]
        if notify_obj.views:
            notify_obj_list_2 += [11]
        for id, dates in following_list:
            notify_list_1 += NotificationModel.objects.filter(user_from_id__in=[id], created__gt=dates, user_to_id=None, type_no__in=notify_obj_list_1).exclude(deleted=user_id).annotate(user_confirmed=Exists(subquery_confirmed)).order_by('-created')
            notify_list_confirmed += NotificationModel.objects.filter(user_from_id__in=[id], created__gt=dates, user_to_id=None, type_no__in=notify_obj_list_1).exclude(deleted=user_id, confirmed=user_id).annotate(user_confirmed=Exists(subquery_confirmed)).order_by('-created')
        notify_list_2 = NotificationModel.objects.filter(user_to_id=user_id, type_no__in=notify_obj_list_2).exclude(deleted=user_id).annotate(user_confirmed=Exists(subquery_confirmed)).order_by('-created')
        notify_list_data = {
            'notification_count': len(list(chain(notify_list_confirmed, notify_list_2.exclude(confirmed=user_id)))),
            'notification_list': list(chain(notify_list_1, notify_list_2)),
        }
        return notify_list_data

class ContextData:
    def context_data(self, models, **kwargs):
        context = super(models, self).get_context_data(**kwargs)
        self.count = 0
        user_id = self.request.user.id
        if user_id is not None:
            notify_list = notify_data(self)
            context['notification_count'] = notify_list['notification_count']
            context['notification_list'] = notify_list['notification_list']
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=user_id).order_by('sequence')[:20],
        })
        if 'Notification' in str(models.__name__):
            context.update(notify_setting_list=NotifySettingModel.objects.filter(owner_id=user_id))

        if 'ProfileUpdate' in str(models.__name__):
            context['gender'] = {'0':'男性', '1':'女性', '2':'秘密'}

        if 'Index' in str(models.__name__):
            context.update({
                'video_list': VideoModel.objects.filter(publish=True).order_by('-created')[:8],
                'live_list': LiveModel.objects.filter(publish=True).order_by('-created')[:8],
                'music_list': MusicModel.objects.filter(publish=True).order_by('-created')[:8],
                'picture_list': PictureModel.objects.filter(publish=True).order_by('-created')[:8],
                'blog_list': BlogModel.objects.filter(publish=True).order_by('-created')[:8],
                'chat_list': ChatModel.objects.filter(publish=True).order_by('-created')[:8],
            })

        if 'Recommend' in str(models.__name__):
            # 急上昇はcreatedが1日以内かつscoreが100000以上の上位8レコード
            # テストはcreatedが100日以内かつscoreが50以上の上位8レコード
            # socre = (read + like*10) + read * like/read * 20
            aggregation_date = datetime.datetime.today() - datetime.timedelta(days=100)
            context['Recommend'] = 'Recommend'
            context.update({
                'video_list': VideoModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'live_list': LiveModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'music_list': MusicModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'picture_list': PictureModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'blog_list': BlogModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'chat_list': ChatModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
            })

        if ('UserPage' or 'UserPageInfo' or 'UserPageAdvertise') in str(models.__name__):
            author = get_object_or_404(User, nickname=self.kwargs['nickname'])
            author_id = author.id
            follow = FollowModel.objects.filter(follower=self.request.user.id).filter(following=author_id)
            followed = False
            if follow.exists():
                followed = True
            context['followed'] = followed
            context['author_name'] = author.nickname
            context.update({
                'user_list': User.objects.filter(id=author_id),
                'video_list': VideoModel.objects.filter(author_id=author_id, publish=True),
                'live_list': LiveModel.objects.filter(author_id=author_id, publish=True),
                'music_list': MusicModel.objects.filter(author_id=author_id, publish=True),
                'picture_list': PictureModel.objects.filter(author_id=author_id, publish=True),
                'blog_list': BlogModel.objects.filter(author_id=author_id, publish=True),
                'chat_list': ChatModel.objects.filter(author_id=author_id, publish=True),
            })
        return context


    def models_context_data(self, models, **kwargs):
        context = super(models, self).get_context_data(**kwargs)
        obj = self.object
        user_id = self.request.user.id
        follow = FollowModel.objects.filter(follower=user_id).filter(following=obj.author.id)
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
            subquery = CommentModel.objects.filter(**filter_kwargs)
            context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).annotate(comment_liked=Exists(subquery)).select_related('author', 'content_type')
            context['reply_list'] = obj.comments.filter(parent__isnull=False).annotate(comment_liked=Exists(subquery)).select_related('author', 'parent', 'content_type')
        else:
            if obj.period < datetime.date.today():
                is_period = True
            else:
                is_period = False
            context['is_period'] = is_period
            context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        if user_id is not None:
            notify_list = notify_data(self)
            context['notification_count'] = notify_list['notification_count']
            context['notification_list'] = notify_list['notification_list']
        if obj.author.rate_plan == '1':
            context.update(advertise_list=AdvertiseModel.objects.filter(publish=True, type=1, author=obj.author.id).order_by('?')[:1])
        if obj.author.rate_plan == '2':
            context.update(advertise_list=AdvertiseModel.objects.filter(publish=True, type=1, author=obj.author.id).order_by('?')[:3])
        if obj.author.rate_plan == '3':
            context.update(advertise_list=AdvertiseModel.objects.filter(publish=True, type=1, author=obj.author.id).order_by('?')[:4])
        context['liked'] = liked
        context['followed'] = followed
        context['user_id'] = user_id
        context['obj_id'] = obj.id
        context['obj_path'] = self.request.path
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=user_id).order_by('sequence')[:20],
            'advertise_auto_list': AdvertiseModel.objects.filter(publish=True, type=0).order_by('?')[:1],
        })
        if 'VideoDetail' in str(models.__name__):
            context.update(video_list=VideoModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'LiveDetail' in str(models.__name__):
            context.update(live_list=LiveModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'MusicDetail' in str(models.__name__):
            context.update(music_list=MusicModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'PictureDetail' in str(models.__name__):
            context.update(picture_list=PictureModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'BlogDetail' in str(models.__name__):
            context.update(blog_list=BlogModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'ChatDetail' in str(models.__name__):
            context.update(chat_list=ChatModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'ChatThread' in str(models.__name__):
            comment_id = self.kwargs['comment_id']
            context['comment_id'] = comment_id
            context['comment_parent'] = obj.comments.filter(id=comment_id).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
            context['reply_list'] = obj.comments.filter(parent__isnull=False, parent_id=comment_id).select_related('author', 'parent', 'content_type')
            context.update(chat_list=ChatModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'CollaboDetail' in str(models.__name__):
            if obj.period < datetime.date.today():
                is_period = True
            else:
                is_period = False
            context['is_period'] = is_period
            context.update(collabo_list=CollaboModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'TodoDetail' in str(models.__name__):
            context.update(todo_list=TodoModel.objects.filter(author_id=user_id).exclude(id=obj.id)[:50])
        return context
