from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.db.models import F, Count
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from apps.myus.forms import QuillForm
from apps.myus.models import MyPage, NotificationSetting, Follow, Advertise, Todo
from apps.myus.modules.contains import model_dict, model_pjax, model_create_pjax
from apps.myus.modules.search import SearchData


User = get_user_model()

def pjax_context(request, href):
    template = 'index_list.html'
    context = {}
    user = request.user
    search = request.GET.get('search')
    if href == '':
        if search:
            result = SearchData.search_index(search)
            context = {'object_list': result, 'query': search, 'count': len(result)}
        else:
            context = {f'{value}_list': model.objects.filter(publish=True).order_by('-created')[:8] for model, value in model_dict.items()}
    if href == 'recommend':
        aggregation_date = datetime.today() - timedelta(days=500)
        if search:
            result = SearchData.search_recommend(aggregation_date, search)
            context = {'object_list': result, 'query': search, 'count': len(result)}
        else:
            score = F('read') + Count('like')*10 + F('read')*Count('like')/(F('read')+1)*20
            context = {'Recommend': 'Recommend'}
            context.update({
                f'{value}_list': model.objects.annotate(score=score).filter(publish=True, created__gte=aggregation_date, score__gte=50).order_by('-score')[:8]
                for model, value in model_dict.items()
            })
    if 'userpage/post' in href or 'userpage/information' in href or 'userpage/advertise' in href:
        nickname = request.GET.get('nickname')
        author = get_object_or_404(User, nickname=nickname)
        user_list = User.objects.filter(id=author.id)
        follow = Follow.objects.filter(follower=user.id, following=author)
        is_follow = follow.exists()
        if 'userpage/post' in href:
            template = 'userpage/userpage_list.html'
            if search:
                result = SearchData.search_userpage(author, search)
                context = {
                    'is_follow': is_follow, 'author_name': nickname, 'user_list': user_list,
                    'object_list': result, 'query': search, 'count': len(result)
                }
            else:
                context = {'is_follow': is_follow, 'author_name': nickname, 'user_list': user_list}
                context.update({
                    f'{value}_list': model.objects.filter(author=author, publish=True).order_by('-created')
                    for model, value in model_dict.items()
                })
        if 'userpage/information' in href:
            template = 'userpage/userpage_information_content.html'
            context = {'is_follow': is_follow, 'author_name': nickname, 'user_list': user_list}
        if 'userpage/advertise' in href:
            template = 'userpage/userpage_advertise_list.html'
            if search:
                result = SearchData.search_advertise(Advertise, author, search)
                context = {
                    'is_follow': is_follow, 'author_name': nickname, 'user_list': user_list,
                    'advertise_list': result, 'query': search, 'count': len(result)
                }
            else:
                advertise = Advertise.objects.filter(author=author, publish=True)
                context = {'is_follow': is_follow, 'author_name': nickname, 'user_list': user_list, 'advertise_list': advertise}
    if href in model_pjax:
        template = f'{href}/{href}_list.html'
        if search:
            result = SearchData.search_models(model_pjax[href], search)
            context = {f'{href}_list': result[:100], 'query': search, 'count': result.count()}
        else:
            context = {f'{href}_list': model_pjax[href].objects.filter(publish=True).order_by('-created')[:100]}
    if href == 'todo':
        template = 'todo/todo_list.html'
        if search:
            result = SearchData.search_todo(Todo, user, search)
            context = {'todo_list': result[:100], 'query': search, 'count': result.count()}
        else:
            context = {'todo_list': Todo.objects.filter(author=user.id).order_by('-created')[:100]}
    if href in ('follow', 'follower'):
        if search:
            template = f'follow/{href}_list.html'
            result = SearchData.search_follow(Follow, href, user, search)
            context = {f'{href}_list': result[:100], 'query': search, 'count': result.count()}
        elif href == 'follow':
            template = 'follow/follow_list.html'
            context = {'follow_list': Follow.objects.filter(follower=user.id).select_related('following__mypage').order_by('created')[:100]}
        elif href == 'follower':
            template = 'follow/follower_list.html'
            context = {'follower_list': Follow.objects.filter(following=user.id).select_related('follower__mypage').order_by('created')[:100]}
    if href in model_create_pjax:
        model = href.replace('/create', '')
        template = f'{model}/{model}_create_content.html'
        if model == 'blog':
            context = {'form': QuillForm()}
    if href == 'notification':
        template = 'common/notification_content.html'
        context = {'notification_setting_list': NotificationSetting.objects.filter(user=user.id)}
    if href == 'userpolicy':
        template = 'common/userpolicy_content.html'
    if href == 'knowledge':
        template = 'common/knowledge_content.html'
    if href == 'payment':
        template = 'payment/payment_content.html'
    if href == 'profile':
        template = 'registration/profile_content.html'
    if href == 'mypage':
        template = 'registration/mypage_content.html'
        context = {'mypage_list': MyPage.objects.filter(user=user.id)}
    if href == 'withdrawal':
        template = 'registration/withdrawal_content.html'
        context = {'expired_seconds': 60}
    return {'html': render_to_string(template, context, request)}
