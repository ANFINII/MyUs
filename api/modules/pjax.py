import datetime
from django.contrib.auth import get_user_model
from django.db.models import F, Count
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from api.forms import BlogForm
from api.models import MyPage, NotificationSetting, Follow
from api.models import Video, Live, Music, Picture, Blog, Chat, Todo, Advertise
from api.modules.contains import models_pjax, models_create_pjax
from api.modules.search import SearchPjax

User = get_user_model()

def pjax_context(request, href):
    context = {}
    user = request.user
    if href == '':
        search = request.GET.get('search')
        if search:
            result = SearchPjax.search_index(search)
            context['html'] = render_to_string('index_list.html', {
                'object_list': result, 'query': search, 'count': len(result)
            }, request=request)
        else:
            context['html'] = render_to_string('index_list.html', {
                'video_list': Video.objects.filter(publish=True).order_by('-created')[:8],
                'live_list': Live.objects.filter(publish=True).order_by('-created')[:8],
                'music_list': Music.objects.filter(publish=True).order_by('-created')[:8],
                'picture_list': Picture.objects.filter(publish=True).order_by('-created')[:8],
                'blog_list': Blog.objects.filter(publish=True).order_by('-created')[:8],
                'chat_list': Chat.objects.filter(publish=True).order_by('-created')[:8],
            }, request=request)
    if href == 'recommend':
        aggregation_date = datetime.datetime.today() - datetime.timedelta(days=200)
        search = request.GET.get('search')
        if search:
            result = SearchPjax.search_recommend(search, aggregation_date)
            context['html'] = render_to_string('index_list.html', {
                'object_list': result, 'query': search, 'count': len(result)
            }, request=request)
        else:
            context['html'] = render_to_string('index_list.html', {
                'Recommend': 'Recommend',
                'video_list': Video.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'live_list': Live.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'music_list': Music.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'picture_list': Picture.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'blog_list': Blog.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
                'chat_list': Chat.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10 + F('read')*Count('like')/F('read')*20).filter(score__gte=50).order_by('-score')[:8],
            }, request=request)
    if 'userpage/post' in href or 'userpage/information' in href or 'userpage/advertise' in href:
        nickname = request.GET.get('nickname')
        author = get_object_or_404(User, nickname=nickname)
        user_list = User.objects.filter(id=author.id)
        follow = Follow.objects.filter(follower=user.id, following=author)
        followed = False
        if follow.exists():
            followed = True
        if 'userpage/post' in href:
            search = request.GET.get('search')
            if search:
                result = SearchPjax.search_userpage(search, author)
                context['html'] = render_to_string('userpage/userpage_list.html', {
                    'followed': followed, 'author_name': nickname, 'user_list': user_list,
                    'object_list': result, 'query': search, 'count': len(result)
                }, request=request)
            else:
                context['html'] = render_to_string('userpage/userpage_list.html', {
                    'followed': followed, 'author_name': nickname, 'user_list': user_list,
                    'video_list': Video.objects.filter(author=author, publish=True).order_by('-created'),
                    'live_list': Live.objects.filter(author=author, publish=True).order_by('-created'),
                    'music_list': Music.objects.filter(author=author, publish=True).order_by('-created'),
                    'picture_list': Picture.objects.filter(author=author, publish=True).order_by('-created'),
                    'blog_list': Blog.objects.filter(author=author, publish=True).order_by('-created'),
                    'chat_list': Chat.objects.filter(author=author, publish=True).order_by('-created'),
                }, request=request)
        if 'userpage/information' in href:
            context['html'] = render_to_string('userpage/userpage_information_content.html', {
                'followed': followed, 'author_name': nickname, 'user_list': user_list
            }, request=request)
        if 'userpage/advertise' in href:
            context['html'] = render_to_string('userpage/userpage_advertise_list.html', {
                'followed': followed, 'author_name': nickname, 'user_list': user_list,
                'advertise_list': Advertise.objects.filter(author=author, publish=True)
            }, request=request)
    if href in models_pjax:
        search = request.GET.get('search')
        if search:
            result = SearchPjax.search_models(models_pjax[href], search)
            context['html'] = render_to_string(f'{href}/{href}_list.html', {
                f'{href}_list': result[:100], 'query': search, 'count': result.count()
            }, request=request)
        else:
            context['html'] = render_to_string(f'{href}/{href}_list.html', {
                f'{href}_list': models_pjax[href].objects.filter(publish=True).order_by('-created')[:100]
            }, request=request)
    if href == 'todo':
        search = request.GET.get('search')
        if search:
            result = SearchPjax.search_todo(Todo, search, user)
            context['html'] = render_to_string('todo/todo_list.html', {
                'todo_list': result[:100], 'query': search, 'count': result.count()
            }, request=request)
        else:
            context['html'] = render_to_string('todo/todo_list.html', {
                'todo_list': Todo.objects.filter(author=user.id).order_by('-created')[:100]
            }, request=request)
    if href in ('follow', 'follower'):
        search = request.GET.get('search')
        if search:
            result = SearchPjax.search_follow(Follow, search, href, user)
            context['html'] = render_to_string(f'follow/{href}_list.html', {
                f'{href}_list': result[:100], 'query': search, 'count': result.count()
            }, request=request)
        elif href == 'follow':
            context['html'] = render_to_string('follow/follow_list.html', {
                'follow_list': Follow.objects.filter(follower=user.id).select_related('following__mypage').order_by('created')[:100],
            }, request=request)
        elif href == 'follower':
            context['html'] = render_to_string('follow/follower_list.html', {
                'follower_list': Follow.objects.filter(following=user.id).select_related('follower__mypage').order_by('created')[:100],
            }, request=request)
    if href in models_create_pjax:
        model = href.replace('/create', '')
        if model == 'blog':
            context['html'] = render_to_string(f'{model}/{model}_create_content.html', {'form': BlogForm()}, request=request)
        else:
            context['html'] = render_to_string(f'{model}/{model}_create_content.html', request=request)
    if href == 'notification':
        context['html'] = render_to_string('common/notification_content.html', {
            'notification_setting_list': NotificationSetting.objects.filter(user=user.id)
        }, request=request)
    if href == 'userpolicy':
        context['html'] = render_to_string('common/userpolicy_content.html', request=request)
    if href == 'knowledge':
        context['html'] = render_to_string('common/knowledge_content.html', request=request)
    if href == 'payment':
        context['html'] = render_to_string('payment/payment_content.html', request=request)
    if href == 'profile':
        context['html'] = render_to_string('registration/profile_content.html', request=request)
    if href == 'mypage':
        context['html'] = render_to_string('registration/mypage_content.html', {'mypage_list': MyPage.objects.filter(user=user.id)}, request=request)
    if href == 'withdrawal':
        context['html'] = render_to_string('registration/withdrawal_content.html', {'expired_seconds': 60}, request=request)
    return context
