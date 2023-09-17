from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.db.models import F, Count
from django.template.loader import render_to_string
from apps.myus.models import PlanMaster, MyPage, NotificationSetting, Follow, Advertise, Todo
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
        author = User.objects.get(nickname=nickname)
        follow = Follow.objects.filter(follower=user.id, following=author)
        is_follow = follow.exists()
        if 'userpage/post' in href:
            template = 'userpage/userpage_list.html'
            if search:
                result = SearchData.search_userpage(author, search)
                context = {
                    'is_follow': is_follow, 'author': author, 'object_list': result,
                    'query': search, 'count': len(result)
                }
            else:
                context = {'is_follow': is_follow, 'author': author}
                context.update({
                    f'{value}_list': model.objects.filter(author=author, publish=True).order_by('-created')
                    for model, value in model_dict.items()
                })
        if 'userpage/information' in href:
            template = 'userpage/userpage_information_content.html'
            context = {'is_follow': is_follow, 'author': author}
        if 'userpage/advertise' in href:
            template = 'userpage/userpage_advertise_list.html'
            if search:
                result = SearchData.search_advertise(Advertise, author, search)
                context = {
                    'is_follow': is_follow, 'author': author, 'advertise_list': result,
                    'query': search, 'count': len(result)
                }
            else:
                advertise = Advertise.objects.filter(author=author, publish=True)
                context = {'is_follow': is_follow, 'author': author, 'advertise_list': advertise}
    if href in model_pjax:
        model = href.replace('media/', '')
        template = f'media/{model}/{model}_list.html'
        if search:
            result = SearchData.search_models(model_pjax[href], search)
            context = {f'{model}_list': result[:100], 'query': search, 'count': result.count()}
        else:
            context = {f'{model}_list': model_pjax[href].objects.filter(publish=True).order_by('-created')[:100]}
    if href == 'media/todo':
        template = 'media/todo/todo_list.html'
        if search:
            result = SearchData.search_todo(Todo, user, search)
            context = {'todo_list': result[:100], 'query': search, 'count': result.count()}
        else:
            context = {'todo_list': Todo.objects.filter(author=user.id).order_by('-created')[:100]}
    if href in ('menu/follow', 'menu/follower'):
        if search:
            template = f'menu/follow/{href}_list.html'
            result = SearchData.search_follow(Follow, href, user, search)
            context = {f'{href}_list': result[:100], 'query': search, 'count': result.count()}
        elif href == 'menu/follow':
            template = 'menu/follow/follow_list.html'
            context = {'follow_list': Follow.objects.filter(follower=user.id).select_related('following__mypage').order_by('created')[:100]}
        elif href == 'menu/follower':
            template = 'menu/follow/follower_list.html'
            context = {'follower_list': Follow.objects.filter(following=user.id).select_related('follower__mypage').order_by('created')[:100]}
    if href in model_create_pjax:
        model = href.replace('media/', '').replace('/create', '')
        template = f'media/{model}/{model}_create_content.html'
    if href == 'menu/userpolicy':
        template = 'menu/userpolicy_content.html'
    if href == 'menu/knowledge':
        template = 'menu/knowledge_content.html'
    if href == 'setting/payment':
        template = 'setting/payment/payment_content.html'
        context = {'payment_list': PlanMaster.objects.all().order_by('-id')}
    if href == 'setting/profile':
        template = 'setting/profile_content.html'
    if href == 'setting/mypage':
        template = 'setting/mypage_content.html'
        context = {'mypage_list': MyPage.objects.filter(user=user.id)}
    if href == 'setting/withdrawal':
        template = 'setting/withdrawal_content.html'
        context = {'expired_seconds': 60}
    if href == 'setting/notification':
        template = 'setting/notification_content.html'
        context = {'notification_setting': NotificationSetting.objects.filter(user=user.id).first()}
    return {'html': render_to_string(template, context, request)}
