from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import F, Count, Exists, OuterRef
from myusapp.models import SearchTagModel, NotificationModel, CommentModel, FollowModel, AdvertiseModel, TodoModel
from myusapp.models import VideoModel, LiveModel, MusicModel, PictureModel, BlogModel, ChatModel, CollaboModel
import datetime

User = get_user_model()

class ContextData:
    def create_context_data(self, model_create, **kwargs):
        context = super(model_create, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        following_id_list = list(FollowModel.objects.filter(follower_id=user_id).values_list('following_id', flat=True))
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=user_id).order_by('sequence')[:20],
            'notification_list': NotificationModel.objects.filter(user_from_id__in=following_id_list, user_to_id=user_id).order_by('-created')[:50],
        })
        return context


    def list_context_data(self, model_list, **kwargs):
        context = super(model_list, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        following_id_list = list(FollowModel.objects.filter(follower_id=user_id).values_list('following_id', flat=True))
        # following_created_list = list(FollowModel.objects.filter(follower_id=user_id).values_list('created', flat=True))
        # following_id_list = FollowModel.objects.filter(follower_id=user_id).values('following_id', 'created')
        print(following_id_list)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=user_id).order_by('sequence')[:20],
            'notification_list': NotificationModel.objects.filter(user_from_id__in=following_id_list, user_to_id=user_id).order_by('-created')[:50],
        })
        if 'myusapp.views.Index' in str(model_list):
            context.update({
                'video_list': VideoModel.objects.filter(publish=True).order_by('-created')[:8],
                'live_list': LiveModel.objects.filter(publish=True).order_by('-created')[:8],
                'music_list': MusicModel.objects.filter(publish=True).order_by('-created')[:8],
                'picture_list': PictureModel.objects.filter(publish=True).order_by('-created')[:8],
                'blog_list': BlogModel.objects.filter(publish=True).order_by('-created')[:8],
                'chat_list': ChatModel.objects.filter(publish=True).order_by('-created')[:8],
            })

        if 'myusapp.views.Recommend' in str(model_list):
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

        if ('myusapp.views.UserPage' or 'myusapp.views.UserPageInfo' or 'myusapp.views.UserPageAdvertise') in str(model_list):
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


    def models_context_data(self, model_detail, **kwargs):
        context = super(model_detail, self).get_context_data(**kwargs)
        obj = self.object
        user_id = self.request.user.id
        following_id_list = list(FollowModel.objects.filter(follower_id=user_id).values_list('following_id', flat=True))
        follow = FollowModel.objects.filter(follower=user_id).filter(following=obj.author.id)
        liked = False
        if obj.like.filter(id=user_id).exists():
            liked = True
        followed = False
        if follow.exists():
            followed = True
        filter_kwargs = {}
        filter_kwargs['id'] = OuterRef('pk')
        filter_kwargs['like'] = user_id
        subquery = CommentModel.objects.filter(**filter_kwargs)
        context['liked'] = liked
        context['followed'] = followed
        context['user_id'] = user_id
        context['obj_id'] = obj.id
        context['obj_path'] = self.request.path
        context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).annotate(comment_liked=Exists(subquery)).select_related('author', 'content_type')
        context['reply_list'] = obj.comments.filter(parent__isnull=False).annotate(comment_liked=Exists(subquery)).select_related('author', 'parent', 'content_type')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=user_id).order_by('sequence')[:20],
            'notification_list': NotificationModel.objects.filter(user_from_id__in=following_id_list, user_to_id=user_id).order_by('-created')[:50],
            'advertise_list': AdvertiseModel.objects.filter(publish=True, type=1, author=obj.author.id).order_by('?')[:6],
            'advertise_auto_list': AdvertiseModel.objects.filter(publish=True, type=0).order_by('?')[:1],
        })
        if 'myusapp.views.VideoDetail' in str(model_detail):
            context.update(video_list=VideoModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'myusapp.views.LiveDetail' in str(model_detail):
            context.update(live_list=LiveModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'myusapp.views.MusicDetail' in str(model_detail):
            context.update(music_list=MusicModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'myusapp.views.PictureDetail' in str(model_detail):
            context.update(picture_list=PictureModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'myusapp.views.BlogDetail' in str(model_detail):
            context.update(blog_list=BlogModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])

        if 'myusapp.views.CollaboDetail' in str(model_detail):
            if obj.period < datetime.date.today():
                is_period = True
            else:
                is_period = False
            context['is_period'] = is_period
            context.update(collabo_list=CollaboModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50])
        return context


    def chat_context_data(self, model_detail, **kwargs):
        context = super(model_detail, self).get_context_data(**kwargs)
        obj = self.object
        user_id = self.request.user.id
        following_id_list = list(FollowModel.objects.filter(follower_id=user_id).values_list('following_id', flat=True))
        follow = FollowModel.objects.filter(follower=user_id).filter(following=obj.author.id)
        liked = False
        if obj.like.filter(id=user_id).exists():
            liked = True
        followed = False
        if follow.exists():
            followed = True
        if obj.period < datetime.date.today():
            is_period = True
        else:
            is_period = False
        context['liked'] = liked
        context['followed'] = followed
        context['is_period'] = is_period
        context['user_id'] = user_id
        context['obj_id'] = obj.id
        context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=user_id).order_by('sequence')[:20],
            'notification_list': NotificationModel.objects.filter(user_from_id__in=following_id_list, user_to_id=user_id).order_by('-created')[:50],
            'chat_list': ChatModel.objects.filter(publish=True).exclude(id=obj.id).order_by('-created')[:50],
        })
        if 'myusapp.views.ChatThread' in str(model_detail):
            comment_id = self.kwargs['comment_id']
            context['comment_id'] = comment_id
            context['reply_list'] = obj.comments.filter(parent__isnull=False, parent_id=comment_id).select_related('author', 'parent', 'content_type')
        return context


    def todo_context_data(self, model_detail, **kwargs):
        context = super(model_detail, self).get_context_data(**kwargs)
        obj = self.object
        user_id = self.request.user.id
        following_id_list = list(FollowModel.objects.filter(follower_id=user_id).values_list('following_id', flat=True))
        filter_kwargs = {}
        filter_kwargs['id'] = OuterRef('pk')
        filter_kwargs['like'] = user_id
        subquery = CommentModel.objects.filter(**filter_kwargs)
        context['user_id'] = user_id
        context['obj_id'] = obj.id
        context['obj_path'] = self.request.path
        context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).annotate(comment_liked=Exists(subquery)).select_related('author', 'content_type')
        context['reply_list'] = obj.comments.filter(parent__isnull=False).annotate(comment_liked=Exists(subquery)).select_related('author', 'parent', 'content_type')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=user_id).order_by('sequence')[:20],
            'notification_list': NotificationModel.objects.filter(user_from_id__in=following_id_list, user_to_id=user_id).order_by('-created')[:50],
            'advertise_list': AdvertiseModel.objects.filter(publish=True, type=1, author=obj.author.id).order_by('?')[:6],
            'advertise_auto_list': AdvertiseModel.objects.filter(publish=True, type=0).order_by('?')[:1],
            'todo_list': TodoModel.objects.filter(author_id=user_id).exclude(id=obj.id),
        })
        return context
