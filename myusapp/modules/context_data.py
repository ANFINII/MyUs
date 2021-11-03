from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef
from myusapp.models import SearchTagModel, CommentModel, FollowModel, AdvertiseModel
from myusapp.models import VideoModel, LiveModel, MusicModel, PictureModel, BlogModel, ChatModel, CollaboModel
import datetime

User = get_user_model()

def models_context_data(self, model_detail, **kwargs):
    context = super(model_detail, self).get_context_data(**kwargs)
    obj = self.object
    user_id = self.request.user.id
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
        'searchtag_list': SearchTagModel.objects.filter(author_id=user_id).order_by('sequence')[:10],
        'advertise_list': AdvertiseModel.objects.filter(publish=True, type=0).order_by('?')[:1],
    })
    if 'myusapp.views.VideoDetail' in str(model_detail):
        context.update(video_list=VideoModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50])

    if 'myusapp.views.LiveDetail' in str(model_detail):
        context.update(live_list=LiveModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50])

    if 'myusapp.views.MusicDetail' in str(model_detail):
        context.update(music_list=MusicModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50])

    if 'myusapp.views.PictureDetail' in str(model_detail):
        context.update(picture_list=PictureModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50])

    if 'myusapp.views.BlogDetail' in str(model_detail):
        context.update(blog_list=BlogModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50])

    if 'myusapp.views.CollaboDetail' in str(model_detail):
        if obj.period < datetime.date.today():
            is_period = True
        else:
            is_period = False
        context['is_period'] = is_period
        context.update(collabo_list=CollaboModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50])
    return context


def chat_context_data(self, model_detail, **kwargs):
    context = super(model_detail, self).get_context_data(**kwargs)
    obj = self.object
    user_id = self.request.user.id
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
    context['obj_title'] = obj.title
    context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
    context.update({
        'searchtag_list': SearchTagModel.objects.filter(author_id=user_id).order_by('sequence')[:10],
        'chat_list': ChatModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50],
    })
    if 'myusapp.views.ChatThread' in str(model_detail):
        comment_id = self.kwargs['comment_id']
        context['comment_id'] = comment_id
        context['reply_list'] = obj.comments.filter(parent__isnull=False, parent_id=comment_id).select_related('author', 'parent', 'content_type')
    return context
