import datetime
from functools import reduce
from itertools import chain
from operator import and_
from django.contrib.auth import get_user_model
from django.db.models import Q, F, Count
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from api.forms import BlogForm
from api.models import MyPage, NotificationSetting, Follow
from api.models import Video, Live, Music, Picture, Blog, Chat, Collabo, Todo, Advertise
from api.modules.search import get_q_list

User = get_user_model()

def pjax_context(request, href):
    context = dict()
    user = request.user
    if '/' == href:
        context['html'] = render_to_string('index_list.html', {
            'video_list': Video.objects.filter(publish=True).order_by('-created')[:8],
            'live_list': Live.objects.filter(publish=True).order_by('-created')[:8],
            'music_list': Music.objects.filter(publish=True).order_by('-created')[:8],
            'picture_list': Picture.objects.filter(publish=True).order_by('-created')[:8],
            'blog_list': Blog.objects.filter(publish=True).order_by('-created')[:8],
            'chat_list': Chat.objects.filter(publish=True).order_by('-created')[:8],
        }, request=request)
    if '/recommend' == href:
        aggregation_date = datetime.datetime.today() - datetime.timedelta(days=200)
        context['html'] = render_to_string('index_list.html', {
            'Recommend': 'Recommend',
            'video_list': Video.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
            'live_list': Live.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
            'music_list': Music.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
            'picture_list': Picture.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
            'blog_list': Blog.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
            'chat_list': Chat.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
        }, request=request)
    if '/userpage/post' in href:
        nickname = request.GET.get('nickname')
        author = get_object_or_404(User, nickname=nickname)
        follow = Follow.objects.filter(follower=user.id, following=author)
        followed = False
        if follow.exists():
            followed = True
        context['html'] = render_to_string('userpage/userpage_list.html', {
            'followed': followed,
            'author_name': author.nickname,
            'user_list': User.objects.filter(id=author.id),
            'video_list': Video.objects.filter(author=author, publish=True).order_by('-created'),
            'live_list': Live.objects.filter(author=author, publish=True).order_by('-created'),
            'music_list': Music.objects.filter(author=author, publish=True).order_by('-created'),
            'picture_list': Picture.objects.filter(author=author, publish=True).order_by('-created'),
            'blog_list': Blog.objects.filter(author=author, publish=True).order_by('-created'),
            'chat_list': Chat.objects.filter(author=author, publish=True).order_by('-created'),
        }, request=request)
    if '/userpage/information' in href:
        nickname = request.GET.get('nickname')
        author = get_object_or_404(User, nickname=nickname)
        follow = Follow.objects.filter(follower=user.id, following=author)
        followed = False
        if follow.exists():
            followed = True
        context['html'] = render_to_string('userpage/userpage_information_content.html', {
            'followed': followed,
            'author_name': author.nickname,
            'user_list': User.objects.filter(id=author.id),
        }, request=request)
    if '/userpage/advertise' in href:
        nickname = request.GET.get('nickname')
        author = get_object_or_404(User, nickname=nickname)
        follow = Follow.objects.filter(follower=user.id, following=author)
        followed = False
        if follow.exists():
            followed = True
        context['html'] = render_to_string('userpage/userpage_advertise_list.html', {
            'followed': followed,
            'author_name': author.nickname,
            'user_list': User.objects.filter(id=author.id),
            'advertise_list': Advertise.objects.filter(author=author, publish=True),
        }, request=request)
    if '/video' == href:
        context['html'] = render_to_string('video/video_list.html', {
            'video_list': Video.objects.filter(publish=True).select_related('author').prefetch_related('like').order_by('-created')[:50],
        }, request=request)
    if '/live' == href:
        context['html'] = render_to_string('live/live_list.html', {
            'live_list': Live.objects.filter(publish=True).select_related('author').prefetch_related('like').order_by('-created')[:50],
        }, request=request)
    if '/music' == href:
        context['html'] = render_to_string('music/music_list.html', {
            'music_list': Music.objects.filter(publish=True).select_related('author').prefetch_related('like').order_by('-created')[:50],
        }, request=request)
    if '/picture' == href:
        context['html'] = render_to_string('picture/picture_list.html', {
            'picture_list': Picture.objects.filter(publish=True).select_related('author').prefetch_related('like').order_by('-created')[:100],
        }, request=request)
    if '/blog' == href:
        result = Blog.objects.filter(publish=True).order_by('-created')
        search = request.GET.get('search')
        context = {}
        if search:
            print('test')
            q_list = get_q_list(search)
            query = reduce(and_, [
                Q(title__icontains=q) |
                Q(hashtag__jp_name__icontains=q) |
                Q(author__nickname__icontains=q) |
                Q(content__icontains=q) |
                Q(richtext__icontains=q) for q in q_list]
            )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).order_by('-score').distinct()
            context['count'] = len(result)
            context['html'] = render_to_string('blog/blog_list.html', {
                'blog_list': result[:100],
                'count': len(result),
            }, request=request)
        else:
            context['html'] = render_to_string('blog/blog_list.html', {
                'blog_list': Blog.objects.filter(publish=True).select_related('author').prefetch_related('like').order_by('-created')[:100],
            }, request=request)
    if '/chat' == href:
        context['html'] = render_to_string('chat/chat_list.html', {
            'chat_list': Chat.objects.filter(publish=True).select_related('author').prefetch_related('like').order_by('-created')[:100],
        }, request=request)
    if '/collabo' == href:
        context['html'] = render_to_string('collabo/collabo_list.html', {
            'collabo_list': Collabo.objects.filter(publish=True).select_related('author').prefetch_related('like').order_by('-created')[:100],
        }, request=request)
    if '/todo' == href:
        context['html'] = render_to_string('todo/todo_list.html', {
            'todo_list': Todo.objects.filter(author=user.id).order_by('-created')[:100],
        }, request=request)
    if '/follow' == href:
        context['html'] = render_to_string('follow/follow_list.html', {
            'follow_list': Follow.objects.filter(follower=user.id).select_related('following__mypage').order_by('created')[:100],
        }, request=request)
    if '/follower' == href:
        context['html'] = render_to_string('follow/follower_list.html', {
            'follower_list': Follow.objects.filter(following=user.id).select_related('follower__mypage').order_by('created')[:100],
        }, request=request)
    if '/notification' == href:
        context['html'] = render_to_string('common/notification_content.html', {
            'notification_setting_list': NotificationSetting.objects.filter(user=user.id),
        }, request=request)
    if '/userpolicy' == href:
        context['html'] = render_to_string('common/userpolicy_content.html', request=request)
    if '/knowledge' == href:
        context['html'] = render_to_string('common/knowledge_content.html', request=request)
    if '/payment' == href:
        context['html'] = render_to_string('payment/payment_content.html', request=request)
    if '/profile' == href:
        context['html'] = render_to_string('registration/profile_content.html', request=request)
    if '/mypage' == href:
        context['html'] = render_to_string('registration/mypage_content.html', {
            'mypage_list': MyPage.objects.filter(user=user.id)
        }, request=request)
    if '/withdrawal' == href:
        EXPIRED_SECONDS = 60
        context['html'] = render_to_string('registration/withdrawal_content.html', {
            'expired_seconds': EXPIRED_SECONDS,
        }, request=request)
    if '/video/create' == href:
        context['html'] = render_to_string('video/video_create_content.html', request=request)
    if '/live/create' == href:
        context['html'] = render_to_string('live/live_create_content.html', request=request)
    if '/music/create' == href:
        context['html'] = render_to_string('music/music_create_content.html', request=request)
    if '/picture/create' == href:
        context['html'] = render_to_string('picture/picture_create_content.html', request=request)
    if '/blog/create' == href:
        context['html'] = render_to_string('blog/blog_create_content.html', {'form' :BlogForm(),}, request=request)
    if '/chat/create' == href:
        context['html'] = render_to_string('chat/chat_create_content.html', request=request)
    if '/collabo/create' == href:
        context['html'] = render_to_string('collabo/collabo_create_content.html', request=request)
    if '/todo/create' == href:
        context['html'] = render_to_string('todo/todo_create_content.html', request=request)
    return context
