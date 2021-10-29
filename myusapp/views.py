from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.contenttypes.models import ContentType
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.html import urlize as urlize_impl
from django.db.models import Q, F, Count, Max, Min, Avg, Value, Exists, OuterRef, Subquery
from django.template.loader import render_to_string
from django.template.defaultfilters import linebreaksbr, linebreaks
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView, FormView, CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import SearchTagForm, ChatCommentForm
from .models import SearchTagModel, TagModel, CommentModel, FollowModel, TodoModel, AdvertiseModel
from .models import VideoModel, LiveModel, MusicModel, PictureModel, BlogModel, ChatModel, CollaboModel
from .modules.search import Search
from .modules.validation import has_username, has_email, has_phone, has_alphabet, has_number
import datetime
import string
import random
import json

# Create your views here.

User = get_user_model()

# Signup
def signup_form(request):
    """サインアップ処理"""
    if request.method == 'POST':
        username_form = request.POST['username']
        if User.objects.filter(username=username_form).count():
            messages.error(request, 'このユーザー名は既に登録されております!')
            return render(request, 'registration/signup.html')

        if has_username(username_form):
            messages.error(request, 'ユーザー名は半角英数字のみ入力できます!')
            return render(request, 'registration/signup.html')

        nickname_form = request.POST['nickname']
        if User.objects.filter(nickname=nickname_form).count():
            messages.error(request, 'この投稿者名は既に登録されております!')
            return render(request, 'registration/signup.html')

        email_form = request.POST['email']
        if User.objects.filter(email=email_form).count():
            messages.error(request, 'このメールアドレスは既に登録されております!')
            return render(request, 'registration/signup.html')

        if has_email(email_form):
            messages.error(request, 'メールアドレスの形式が違います!')
            return render(request, 'registration/signup.html')

        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if not has_alphabet(password1):
            messages.error(request, 'パスワードは8文字以上で数字とアルファベットが含まれる必要があります!')
            return render(request, 'registration/signup.html')

        elif not has_number(password1):
            messages.error(request, 'パスワードは8文字以上で数字とアルファベットが含まれる必要があります!')
            return render(request, 'registration/signup.html')

        last_name = request.POST['last_name']
        if has_number(last_name):
            messages.error(request, '姓に数字が含まれております!')
            return render(request, 'registration/signup.html')

        first_name = request.POST['first_name']
        if has_number(first_name):
            messages.error(request, '名に数字が含まれております!')
            return render(request, 'registration/signup.html')

        gender = request.POST['gender']

        year = request.POST['year']
        if not has_number(year):
            messages.error(request, '生年月日の年を入力してください!')
            return render(request, 'registration/signup.html')

        month = request.POST['month']
        if not has_number(month):
            messages.error(request, '生年月日の月を入力してください!')
            return render(request, 'registration/signup.html')

        day = request.POST['day']
        if not has_number(day):
            messages.error(request, '生年月日の日を入力してください!')
            return render(request, 'registration/signup.html')

        if year and month and day:
            try:
                birthday = datetime.date(year=int(year), month=int(month), day=int(day)).isoformat()
            except ValueError:
                messages.error(request, str(year)+'年'+str(month)+'月'+str(day)+'日'+'は存在しない日付です!')
                return render(request, 'registration/signup.html')
            try:
                User.objects.get(username=username_form)
                messages.error(request, 'このアカウントは既に登録されております!')
                return render(request, 'registration/signup.html')
            except User.DoesNotExist:
                if password1==password2:
                    user = User.objects.create_user(username_form, email_form, password1)
                    user.nickname = nickname_form
                    user.full_name = last_name + ' ' + first_name
                    user.last_name = last_name
                    user.first_name = first_name
                    user.gender = gender

                    user.year = year
                    user.month = month
                    user.day = day
                    days_in_year = 365.2425
                    birthday = datetime.date(year=int(year), month=int(month), day=int(day))
                    user.birthday = birthday.isoformat()
                    user.age = int((datetime.date.today() - birthday).days / days_in_year)

                    user.save()
                    messages.success(request, '登録が完了しました!')
                    return redirect('myus:login')
                else:
                    messages.error(request, 'パスワードが一致していません!')
                    return render(request, 'registration/signup.html')
    return render(request, 'registration/signup.html')


# Login
def login_form(request):
    """ログイン処理"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active or user.is_admin:
                    login(request, user)
                    return redirect('myus:index')
                else:
                    messages.error(request, 'ID又はパスワードが違います!')
                    # messages.error(request, '無効なユーザーです!')
                    return redirect('myus:login')
            else:
                messages.error(request, 'ID又はパスワードが違います!')
                # messages.error(request, 'パスワードが違います!')
                return redirect('myus:login')
        except User.DoesNotExist:
            messages.error(request, 'ID又はパスワードが違います!')
            # messages.error(request, '存在しないアカウントです!')
            return redirect('myus:login')
    return render(request, 'registration/login.html')


# Logout
@login_required
def logout_form(request):
    """ログアウト処理"""
    logout(request)
    return redirect('myus:login')


# Withdrawal
EXPIRED_SECONDS = 60

class Withdrawal(View):
    """退会処理"""
    model = User
    template_name = 'registration/withdrawal.html'
    timestamp_signer = TimestampSigner()

    def get_random_chars(self, char_num=30):
        return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(char_num)])

    def get(self, request, token=None, *args, **kwargs):
        context = {}
        context['expired_seconds'] = EXPIRED_SECONDS
        if token:
            try:
                unsigned_token = self.timestamp_signer.unsign(token, max_age=datetime.timedelta(seconds=EXPIRED_SECONDS))
                context['message'] = '有効なURLです'
                return render(request, 'registration/withdrawal_confirm.html', context)
            except SignatureExpired:
                context['message'] = 'URLは期限切れです'
            except BadSignature:
                context['message'] = 'URLは正しくありません'
        return render(request, self.template_name, context)

    def post(self, request):
        if self.request.method == 'POST':
            password = self.request.POST.get('password')
            password2 = self.request.POST.get('password2')
            if self.request.user.check_password(password):
                context = {}
                context['expired_seconds'] = EXPIRED_SECONDS
                token = self.get_random_chars()
                token_signed = self.timestamp_signer.sign(token)
                context['token_signed'] = token_signed
                return render(request, self.template_name, context)
            elif self.request.user.check_password(password2):
                user = self.request.user
                user.is_active = False
                user.save()
                logout(self.request)
                messages.error(self.request, '退会しました!')
                return redirect('myus:login')
            else:
                messages.error(self.request, 'パスワードが違います!')
                return redirect('myus:withdrawal')


# Profile
def profile(request):
    """アカウント設定"""
    object_profile = User.objects.filter(id=request.user.id)
    return render(request, 'registration/profile.html', {'object_profile':object_profile})

class ProfileUpdate(UpdateView):
    """アカウント更新"""
    model = User
    fields = ('user_image', 'username', 'email', 'nickname', 'last_name', 'first_name', 'gender', 'phone', 'year', 'month', 'day', 'location', 'profession', 'introduction')
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('myus:profile')

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdate, self).get_context_data(**kwargs)
        context['usergender'] = {'gender':{'0':'男性', '1':'女性', '2':'秘密'}}
        return context

    def form_valid(self, form):
        """バリデーションに成功した時"""
        try:
            profile = form.save(commit=False)
            profile.user = self.request.user
            if has_username(self.request.user.username):
                messages.error(self.request, 'ユーザー名は半角英数字のみ入力できます!')
                return super().form_invalid(form)

            if has_email(self.request.user.email):
                messages.error(self.request, 'メールアドレスの形式が違います!')
                return super().form_invalid(form)

            profile.full_name = self.request.user.last_name + ' ' + self.request.user.first_name
            if has_number(self.request.user.last_name):
                messages.error(self.request, '姓に数字が含まれております!')
                return super().form_invalid(form)

            if has_number(self.request.user.first_name):
                messages.error(self.request, '名に数字が含まれております!')
                return super().form_invalid(form)

            if has_phone(self.request.user.phone):
                messages.error(self.request, '電話番号の形式が違います!')
                return super().form_invalid(form)

            profile.year = self.request.user.year
            profile.month = self.request.user.month
            profile.day = self.request.user.day
            birthday = datetime.date(year=int(profile.year), month=int(profile.month), day=int(profile.day))
            profile.birthday = birthday.isoformat()
            days_in_year = 365.2425
            profile.age = int((datetime.date.today() - birthday).days / days_in_year)

            profile.save()
            return super(ProfileUpdate, self).form_valid(form)
        except ValueError:
            messages.error(self.request, str(self.request.user.year)+'年'+str(self.request.user.month)+'月'+str(self.request.user.day)+'日'+'は存在しない日付です!')
            return super().form_invalid(form)

    def form_invalid(self, form):
        """バリデーションに失敗した時"""
        if has_phone(self.request.user.phone):
            messages.error(self.request, '電話番号の形式が違います!!')
            return super().form_invalid(form)
        if has_username(self.request.user.username):
            messages.error(self.request, 'ユーザー名は半角英数字のみ入力できます!')
            return super().form_invalid(form)
        if has_email(self.request.user.email):
            messages.error(self.request, 'メールアドレスの形式が違います!')
            return super().form_invalid(form)
        else:
            messages.error(self.request, 'ユーザー名またはメールアドレス、投稿者名は既に登録済みです!')
            return super().form_invalid(form)

    def get_object(self):
        return self.request.user


# MyPage
def mypage(request):
    """Myページ遷移"""
    object_profile = User.objects.filter(id=request.user.id)
    return render(request, 'registration/mypage.html', {'object_profile':object_profile})

class MyPageUpdate(UpdateView):
    """Myページ更新"""
    model = User
    fields = ('mypage_image', 'mypage_email', 'content')
    template_name = 'registration/mypage_update.html'
    success_url = reverse_lazy('myus:mypage')

    def form_valid(self, form):
        """バリデーションに成功した時"""
        try:
            userpage = form.save(commit=False)
            userpage.user = self.request.user

            if has_email(self.request.user.mypage_email):
                messages.error(self.request, 'メールアドレスの形式が違います!')
                return super().form_invalid(form)

            userpage.save()
            return super(MyPageUpdate, self).form_valid(form)
        except ValueError:
            messages.error(self.request, '更新できませんでした!')
            return super().form_invalid(form)
        except TypeError:
            messages.error(self.request, '更新できませんでした!')
            return super().form_invalid(form)

    def form_invalid(self, form):
        """バリデーションに失敗した時"""
        if has_email(self.request.user.mypage_email):
            messages.error(self.request, 'メールアドレスの形式が違います!')
            return super().form_invalid(form)
        else:
            messages.error(self.request, 'メールアドレスの形式が違います!')
            return super().form_invalid(form)

    def get_object(self):
        return self.request.user


# SearchTag
class SearchTagList(ListView):
    """SearchTagList"""
    model = SearchTagModel
    template_name = 'base2.html'

@csrf_exempt
def searchtag_create(request):
    """searchtag_create"""
    if request.method == 'POST':
        form = SearchTagForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author_id = request.user.id
            form.save()
            context = {
                'searchtag': form.searchtag,
            }
            return JsonResponse(context)
        else:
            form = SearchTagForm()


# LikeForm
models_like_dict = {
    'video/detail': VideoModel,
    'live/detail': LiveModel,
    'music/detail': MusicModel,
    'picture/detail': PictureModel,
    'blog/detail': BlogModel,
    'chat/detail': ChatModel,
    'collabo/detail': CollaboModel,
}

@csrf_exempt
def like_form(request):
    """like_form"""
    if request.method == 'POST':
        user = request.user
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        for models_detail, models in models_like_dict.items():
            if models_detail in obj_path:
                obj = get_object_or_404(models, id=obj_id)
        liked = False
        if obj.like.filter(id=user.id).exists():
            liked = False
            obj.like.remove(user)
        else:
            liked = True
            obj.like.add(user)
        context = {
            'liked': liked,
            'total_like': obj.total_like(),
        }
        if request.is_ajax():
            return JsonResponse(context)

@csrf_exempt
def like_form_comment(request):
    """like_form_comment"""
    if request.method == 'POST':
        user = request.user
        obj_id = request.POST.get('id')
        obj = get_object_or_404(CommentModel, id=obj_id)
        comment_liked = False
        if obj.like.filter(id=user.id).exists():
            comment_liked = False
            obj.like.remove(user)
        else:
            comment_liked = True
            obj.like.add(user)
        context = {
            'comment_liked': comment_liked,
            'total_like': obj.total_like(),
        }
        if request.is_ajax():
            return JsonResponse(context)


# CommentForm & ReplyForm
models_comment_dict = {
    'video/detail': VideoModel,
    'live/detail': LiveModel,
    'music/detail': MusicModel,
    'picture/detail': PictureModel,
    'blog/detail': BlogModel,
    'collabo/detail': CollaboModel,
    'todo/detail': TodoModel,
}

@csrf_exempt
def comment_form(request):
    """comment_form"""
    if request.method == 'POST':
        text = request.POST.get('text')
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        for models_detail, models in models_comment_dict.items():
            if models_detail in obj_path:
                obj = models.objects.get(id=obj_id)
        comment_obj = CommentModel(content_object=obj)
        comment_obj.text = text
        comment_obj.author_id = request.user.id
        comment_obj.save()
        context = {
            'text': urlize_impl(linebreaksbr(comment_obj.text)),
            'nickname': comment_obj.author.nickname,
            'user_image': comment_obj.author.user_image.url,
            'created': naturaltime(comment_obj.created),
            'comment_count': obj.comments.filter(parent__isnull=True).count()
        }
        if request.is_ajax():
            return JsonResponse(context)

@csrf_exempt
def reply_form(request):
    """reply_form"""
    if request.method == 'POST':
        text = request.POST.get('text')
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        comment_id = request.POST.get('comment_id')
        for models_detail, models in models_comment_dict.items():
            if models_detail in obj_path:
                obj = models.objects.get(id=obj_id)
        comment_obj = CommentModel(content_object=obj)
        comment_obj.text = text
        comment_obj.author_id = request.user.id
        comment_obj.parent = CommentModel.objects.get(id=comment_id)
        comment_obj.save()
        context = {
            'text': urlize_impl(linebreaksbr(comment_obj.text)),
            'nickname': comment_obj.author.nickname,
            'user_image': comment_obj.author.user_image.url,
            'created': naturaltime(comment_obj.created),
            'comment_count': obj.comments.filter(parent__isnull=True).count(),
            'reply_count': comment_obj.parent.replies_count(),
        }
        if request.is_ajax():
            return JsonResponse(context)

@csrf_exempt
def comment_update(request, comment_id):
    """comment_update"""
    if request.method == 'POST':
        text = request.POST.get('text')
        comment_obj = CommentModel.objects.get(id=comment_id)
        comment_obj.text = text
        comment_obj.save()
        context = {
            'text': urlize_impl(linebreaksbr(comment_obj.text)),
        }
        if request.is_ajax():
            return JsonResponse(context)

@csrf_exempt
def comment_delete(request, comment_id):
    """comment_delete"""
    if request.method == 'POST':
        obj_id = request.POST.get('id')
        obj = VideoModel.objects.get(id=obj_id)
        comment_id = request.POST.get('comment_id')
        comment_obj = CommentModel.objects.get(id=comment_id)
        comment_obj.delete()
        context = {
            'comment_count': obj.comment_count(),
        }
        if request.is_ajax():
            return JsonResponse(context)

@csrf_exempt
def reply_delete(request, comment_id):
    """reply_delete"""
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment_obj = CommentModel.objects.get(id=comment_id)
        comment_obj.delete()
        context = {
            'reply_count': comment_obj.parent.replies_count(),
        }
        if request.is_ajax():
            return JsonResponse(context)


# Index
class Index(ListView):
    """Index処理、すべてのメディアmodelを表示"""
    model = SearchTagModel
    template_name = 'index.html'
    count = 0

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'video_list': VideoModel.objects.filter(publish=True).order_by('-created')[:8],
            'live_list': LiveModel.objects.filter(publish=True).order_by('-created')[:8],
            'music_list': MusicModel.objects.filter(publish=True).order_by('-created')[:8],
            'picture_list': PictureModel.objects.filter(publish=True).order_by('-created')[:8],
            'blog_list': BlogModel.objects.filter(publish=True).order_by('-created')[:8],
            'chat_list': ChatModel.objects.filter(publish=True).order_by('-created')[:8],
        })
        return context

    def get_queryset(self):
        return Search.search_index(self)

class Recommend(ListView):
    """急上昇機能、すべてのメディアmodelを表示"""
    model = SearchTagModel
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Recommend, self).get_context_data(**kwargs)
        context['Recommend'] = 'Recommend'
        # 急上昇はcreatedが1日以内かつscoreが10000以上の上位8レコード
        # テストはcreatedが100日以内かつscoreが100以上の上位8レコード
        # socreはread + like*10
        aggregation_date = datetime.datetime.today() - datetime.timedelta(days=100)
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'video_list': VideoModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10).filter(score__gte=100).order_by('-score')[:8],
            'live_list': LiveModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10).filter(score__gte=100).order_by('-score')[:8],
            'music_list': MusicModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10).filter(score__gte=100).order_by('-score')[:8],
            'picture_list': PictureModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10).filter(score__gte=100).order_by('-score')[:8],
            'blog_list': BlogModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10).filter(score__gte=100).order_by('-score')[:8],
            'chat_list': ChatModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10).filter(score__gte=100).order_by('-score')[:8],
        })
        return context


# UserPage
class UserPage(ListView):
    """UserPage"""
    model = User
    template_name = 'userpage/userpage.html'
    count = 0

    def get_context_data(self, **kwargs):
        context = super(UserPage, self).get_context_data(**kwargs)
        author = get_object_or_404(User, nickname=self.kwargs['nickname'])
        follow = FollowModel.objects.filter(follower=self.request.user.id).filter(following=author)
        followed = False
        if follow.exists():
            followed = True
        context['followed'] = followed
        context['author_name'] = author
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'user_list': User.objects.filter(nickname=author),
            'video_list': VideoModel.objects.filter(author_id=author, publish=True),
            'live_list': LiveModel.objects.filter(author_id=author, publish=True),
            'music_list': MusicModel.objects.filter(author_id=author, publish=True),
            'picture_list': PictureModel.objects.filter(author_id=author, publish=True),
            'blog_list': BlogModel.objects.filter(author_id=author, publish=True),
            'chat_list': ChatModel.objects.filter(author_id=author, publish=True),
        })
        return context

    def get_queryset(self):
        return Search.search_userpage(self)

class UserPageInfo(ListView):
    """UserPageInfo"""
    model = User
    template_name = 'userpage/userpage_information.html'

    def get_context_data(self, **kwargs):
        context = super(UserPageInfo, self).get_context_data(**kwargs)
        author = get_object_or_404(User, nickname=self.kwargs['nickname'])
        follow = FollowModel.objects.filter(follower=self.request.user.id).filter(following=author)
        followed = False
        if follow.exists():
            followed = True
        context['followed'] = followed
        context['author_name'] = author
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'user_list': User.objects.filter(nickname=author),
        })
        return context

class UserPageAdvertise(ListView):
    """UserPageAdvertise"""
    model = User
    template_name = 'userpage/userpage_advertise.html'
    context_object_name = 'advertise_list'
    count = 0

    def get_context_data(self, **kwargs):
        context = super(UserPageAdvertise, self).get_context_data(**kwargs)
        author = get_object_or_404(User, nickname=self.kwargs['nickname'])
        follow = FollowModel.objects.filter(follower=self.request.user.id).filter(following=author)
        followed = False
        if follow.exists():
            followed = True
        context['followed'] = followed
        context['author_name'] = author
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'user_list': User.objects.filter(nickname=author),
        })
        return context

    def get_queryset(self, **kwargs):
        return Search.search_advertise(self, AdvertiseModel)

# Follow
class FollowerList(ListView):
    """FollowerList"""
    model = FollowModel
    template_name = 'follow/follower.html'
    context_object_name = 'follower_list'
    count = 0

    def get_context_data(self, **kwargs):
        context = super(FollowerList, self).get_context_data(**kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context

    def get_queryset(self, **kwargs):
        return Search.search_follower(self, FollowModel)

class FollowList(ListView):
    """FollowList"""
    model = FollowModel
    template_name = 'follow/follow.html'
    context_object_name = 'follow_list'
    count = 0

    def get_context_data(self, **kwargs):
        context = super(FollowList, self).get_context_data(**kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context

    def get_queryset(self, **kwargs):
        return Search.search_following(self, FollowModel)

@csrf_exempt
def follow_create(request, nickname):
    """follow_create"""
    if request.method == 'POST':
        follower = User.objects.get(nickname=request.user.nickname)
        following = User.objects.get(nickname=nickname)
        if follower == following:
            # '自分はフォローできません'
            pass
        elif FollowModel.objects.filter(follower=follower, following=following).exists():
            unfollow = FollowModel.objects.get(follower=follower, following=following)
            unfollow.delete()
            followed = False
            #ログインユーザーのフォロー数
            following_count = FollowModel.objects.filter(follower=follower).count()
            follower.following_count = following_count
            follower.save()
            #フォローユーザーのフォロワー数
            follower_count = FollowModel.objects.filter(following=following).count()
            following.follower_count = follower_count
            following.save()
            # 'フォローを外しました'
        else:
            FollowModel.objects.get_or_create(follower=follower, following=following)
            followed = True
            #ログインユーザーのフォロー数
            following_count = FollowModel.objects.filter(follower=follower).count()
            follower.following_count = following_count
            follower.save()
            #フォローユーザーのフォロワー数
            follower_count = FollowModel.objects.filter(following=following).count()
            following.follower_count = follower_count
            following.save()
            # 'フォローしました'
        context = {
            'followed': followed,
            'follower_count': follower_count,
        }
        if request.is_ajax():
            return JsonResponse(context)


# UserPolicy
def userpolicy(request):
    """userpolicy"""
    return render(request, 'common/userpolicy.html')


# KnowledgeBase
def knowledge(request):
    """knowledge"""
    return render(request, 'common/knowledge.html')


# Video
class VideoCreate(CreateView):
    """VideoCreate"""
    model = VideoModel
    fields = ('title', 'content', 'images', 'videos')
    template_name = 'video/video_create.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(VideoCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:video_detail', kwargs={'pk': self.object.pk, 'title': self.object.title})

class VideoList(ListView):
    """VideoList"""
    model = VideoModel
    template_name = 'video/video.html'
    context_object_name = 'video_list'
    ordering = ['-created']
    count = 0

    def get_context_data(self, **kwargs):
        context = super(VideoList, self).get_context_data(**kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context

    def get_queryset(self, **kwargs):
        return Search.search_models(self, VideoModel)

class VideoDetail(DetailView):
    """VideoDetail"""
    model = VideoModel
    template_name = 'video/video_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.read += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(VideoDetail, self).get_context_data(**kwargs)
        obj = self.object
        follow = FollowModel.objects.filter(follower=self.request.user.id).filter(following=obj.author.id)
        liked = False
        followed = False
        if obj.like.filter(id=self.request.user.id).exists():
            liked = True
        if follow.exists():
            followed = True
        context['liked'] = liked
        context['followed'] = followed
        context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        context['reply_list'] = obj.comments.filter(parent__isnull=False).select_related('author', 'parent', 'content_type')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'advertise_list': AdvertiseModel.objects.filter(publish=True, type=0).order_by('?')[:1],
            'video_list': VideoModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50],
        })
        return context


# Live
class LiveCreate(CreateView):
    """LiveCreate"""
    model = LiveModel
    fields = ('title', 'content', 'images', 'lives')
    template_name = 'live/live_create.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(LiveCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:live_detail', kwargs={'pk': self.object.pk, 'title': self.object.title})

class LiveList(ListView):
    """LiveList"""
    model = LiveModel
    template_name = 'live/live.html'
    context_object_name = 'live_list'
    ordering = ['-created']
    count = 0

    def get_context_data(self, **kwargs):
        context = super(LiveList, self).get_context_data(**kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context

    def get_queryset(self, **kwargs):
        return Search.search_models(self, LiveModel)

class LiveDetail(DetailView):
    """LiveDetail"""
    model = LiveModel
    template_name = 'live/live_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.read += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(LiveDetail, self).get_context_data(**kwargs)
        obj = self.object
        follow = FollowModel.objects.filter(follower=self.request.user.id).filter(following=obj.author.id)
        liked = False
        followed = False
        if obj.like.filter(id=self.request.user.id).exists():
            liked = True
        if follow.exists():
            followed = True
        context['liked'] = liked
        context['followed'] = followed
        context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        context['reply_list'] = obj.comments.filter(parent__isnull=False).select_related('author', 'parent', 'content_type')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'advertise_list': AdvertiseModel.objects.filter(publish=True, type=0).order_by('?')[:1],
            'live_list': LiveModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50],
        })
        return context


# Music
class MusicCreate(CreateView):
    """MusicCreate"""
    model = MusicModel
    fields = ('title', 'content', 'musics', 'lyrics')
    template_name = 'music/music_create.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(MusicCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:music_detail', kwargs={'pk': self.object.pk, 'title': self.object.title})

class MusicList(ListView):
    """MusicList"""
    model = MusicModel
    template_name = 'music/music.html'
    context_object_name = 'music_list'
    ordering = ['-created']
    count = 0

    def get_context_data(self, **kwargs):
        context = super(MusicList, self).get_context_data(**kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context

    def get_queryset(self, **kwargs):
        return Search.search_music(self, MusicModel)

class MusicDetail(DetailView):
    """MusicDetail"""
    model = MusicModel
    template_name = 'music/music_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.read += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(MusicDetail, self).get_context_data(**kwargs)
        obj = self.object
        follow = FollowModel.objects.filter(follower=self.request.user.id).filter(following=obj.author.id)
        liked = False
        followed = False
        if obj.like.filter(id=self.request.user.id).exists():
            liked = True
        if follow.exists():
            followed = True
        context['liked'] = liked
        context['followed'] = followed
        context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        context['reply_list'] = obj.comments.filter(parent__isnull=False).select_related('author', 'parent', 'content_type')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'advertise_list': AdvertiseModel.objects.filter(publish=True, type=0).order_by('?')[:1],
            'music_list': MusicModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50],
        })
        return context


# Picture
class PictureCreate(CreateView):
    """PictureCreate"""
    model = PictureModel
    fields = ('title', 'content', 'images')
    template_name = 'picture/picture_create.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(PictureCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:picture_detail', kwargs={'pk': self.object.pk, 'title': self.object.title})

class PictureList(ListView):
    """PictureList"""
    model = PictureModel
    template_name = 'picture/picture.html'
    context_object_name = 'picture_list'
    ordering = ['-created']
    count = 0

    def get_context_data(self, **kwargs):
        context = super(PictureList, self).get_context_data(**kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context

    def get_queryset(self, **kwargs):
        return Search.search_models(self, PictureModel)

class PictureDetail(DetailView):
    """PictureDetail"""
    model = PictureModel
    template_name = 'picture/picture_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.read += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PictureDetail, self).get_context_data(**kwargs)
        obj = self.object
        follow = FollowModel.objects.filter(follower=self.request.user.id).filter(following=obj.author.id)
        liked = False
        followed = False
        if obj.like.filter(id=self.request.user.id).exists():
            liked = True
        if follow.exists():
            followed = True
        context['liked'] = liked
        context['followed'] = followed
        context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        context['reply_list'] = obj.comments.filter(parent__isnull=False).select_related('author', 'parent', 'content_type')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'advertise_list': AdvertiseModel.objects.filter(publish=True, type=0).order_by('?')[:1],
            'picture_list': PictureModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50],
        })
        return context


# Blog
class BlogCreate(CreateView):
    """BlogCreate"""
    model = BlogModel
    fields = ('title', 'content', 'images', 'richtext')
    template_name = 'blog/blog_create.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(BlogCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:blog_detail', kwargs={'pk': self.object.pk, 'title': self.object.title})

class BlogList(ListView):
    """BlogList"""
    model = BlogModel
    template_name = 'blog/blog.html'
    context_object_name = 'blog_list'
    ordering = ['-created']
    count = 0

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context

    def get_queryset(self, **kwargs):
        return Search.search_blog(self, BlogModel)

class BlogDetail(DetailView):
    """BlogDetail"""
    model = BlogModel
    template_name = 'blog/blog_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.read += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        obj = self.object
        follow = FollowModel.objects.filter(follower=self.request.user.id).filter(following=obj.author.id)
        liked = False
        followed = False
        if obj.like.filter(id=self.request.user.id).exists():
            liked = True
        if follow.exists():
            followed = True
        context['liked'] = liked
        context['followed'] = followed
        context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        context['reply_list'] = obj.comments.filter(parent__isnull=False).select_related('author', 'parent', 'content_type')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'advertise_list': AdvertiseModel.objects.filter(publish=True, type=0).order_by('?')[:1],
            'blog_list': BlogModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50],
        })
        return context


# Chat
class ChatCreate(CreateView):
    """ChatCreate"""
    model = ChatModel
    fields = ('title', 'content', 'period')
    template_name = 'chat/chat_create.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(ChatCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:chat_detail', kwargs={'pk': self.object.pk, 'title': self.object.title})

class ChatList(ListView):
    """ChatList"""
    model = ChatModel
    template_name = 'chat/chat.html'
    context_object_name = 'chat_list'
    ordering = ['-created']
    count = 0

    def get_context_data(self, **kwargs):
        context = super(ChatList, self).get_context_data(**kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context

    def get_queryset(self, **kwargs):
        return Search.search_models(self, ChatModel)

class ChatDetail(DetailView):
    """ChatDetail"""
    model = ChatModel
    template_name = 'chat/chat_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.read += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ChatDetail, self).get_context_data(**kwargs)
        obj = self.object
        follow = FollowModel.objects.filter(follower=self.request.user.id).filter(following=obj.author.id)
        liked = False
        followed = False
        if obj.like.filter(id=self.request.user.id).exists():
            liked = True
        if follow.exists():
            followed = True
        if obj.period < datetime.date.today():
            is_period = True
        else:
            is_period = False
        context['liked'] = liked
        context['followed'] = followed
        context['is_period'] = is_period
        context['obj_id'] = obj.id
        context['obj_title'] = obj.title
        context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'chat_list': ChatModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50],
        })
        return context

class ChatThread(DetailView):
    """ChatDetailThread"""
    model = ChatModel
    template_name = 'chat/chat_thread.html'

    def get_context_data(self, **kwargs):
        context = super(ChatThread, self).get_context_data(**kwargs)
        obj = self.object
        comment_id = self.kwargs['comment_id']
        follow = FollowModel.objects.filter(follower=self.request.user.id).filter(following=obj.author.id)
        liked = False
        followed = False
        if obj.like.filter(id=self.request.user.id).exists():
            liked = True
        if follow.exists():
            followed = True
        if obj.period < datetime.date.today():
            is_period = True
        else:
            is_period = False
        context['liked'] = liked
        context['followed'] = followed
        context['is_period'] = is_period
        context['obj_id'] = obj.id
        context['obj_title'] = obj.title
        context['comment_id'] = comment_id
        context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        context['reply_list'] = obj.comments.filter(parent__isnull=False, parent_id=comment_id).select_related('author', 'parent', 'content_type')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'chat_list': ChatModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50],
        })
        return context

@csrf_exempt
def chat_message(request):
    """chat_message"""
    context = dict()
    if request.method == 'POST':
        text = request.POST.get('text')
        obj_id = request.POST.get('id')
        obj = ChatModel.objects.get(id=obj_id)
        comment_obj = CommentModel(content_object=obj)
        comment_obj.content_object = obj
        comment_obj.text = text
        comment_obj.author_id = request.user.id
        comment_obj.save()
        comment_list = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        context['user_count'] = obj.user_count()
        context['comment_count'] = obj.comment_count()
        context['comment_lists'] = render_to_string('chat/chat_comment/chat_comment.html', {
            'comment_list': comment_list,
            'user_id': request.user.id,
            'obj_id': obj_id,
            'obj_title': obj.title,
            'comment_id': comment_obj.id,
        })
        if request.is_ajax():
            return JsonResponse(context)

@csrf_exempt
def chat_reply(request):
    """chat_reply"""
    context = dict()
    if request.method == 'POST':
        text = request.POST.get('reply')
        obj_id = request.POST.get('id')
        comment_id = request.POST.get('comment_id')
        obj = ChatModel.objects.get(id=obj_id)
        comment_obj = CommentModel(content_object=obj)
        comment_obj.text = text
        comment_obj.author_id = request.user.id
        comment_obj.parent = CommentModel.objects.get(id=comment_id)
        comment_obj.save()
        reply_list = obj.comments.filter(parent__isnull=False, parent_id=comment_id).select_related('author', 'parent', 'content_type')
        context['user_count'] = obj.user_count()
        context['comment_count'] = obj.comment_count()
        context['reply_count'] = comment_obj.parent.replies_count()
        context['reply_lists'] = render_to_string('chat/chat_reply/chat_reply.html', {
            'reply_list': reply_list,
            'user_id': request.user.id,
            'obj_id': obj_id,
        })
        if request.is_ajax():
            return JsonResponse(context, safe=False)

@csrf_exempt
def chat_message_update(request, comment_id):
    """chat_message_update"""
    if request.method == 'POST':
        text = request.POST.get('text')
        comment_obj = CommentModel.objects.get(id=comment_id)
        comment_obj.text = text
        comment_obj.save()
        context = {
            'text': urlize_impl(linebreaksbr(text)),
        }
        if request.is_ajax():
            return JsonResponse(context)

@csrf_exempt
def chat_message_delete(request, comment_id):
    """chat_message_delete"""
    if request.method == 'POST':
        obj_id = request.POST.get('id')
        obj = ChatModel.objects.get(id=obj_id)
        comment_obj = CommentModel.objects.get(id=comment_id)
        comment_obj.delete()
        context = {
            'user_count': obj.user_count(),
            'comment_count': obj.comment_count(),
        }
        if request.is_ajax():
            return JsonResponse(context)

@csrf_exempt
def chat_reply_delete(request, comment_id):
    """chat_reply_delete"""
    if request.method == 'POST':
        obj_id = request.POST.get('id')
        obj = ChatModel.objects.get(id=obj_id)
        comment_obj = CommentModel.objects.get(id=comment_id)
        comment_obj.delete()
        context = {
            'user_count': obj.user_count(),
            'reply_count': comment_obj.parent.replies_count(),
        }
        if request.is_ajax():
            return JsonResponse(context)


# Collabo
class CollaboCreate(CreateView):
    """CollaboCreate"""
    model = CollaboModel
    fields = ('title', 'content', 'period')
    template_name = 'collabo/collabo_create.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(CollaboCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:collabo_detail', kwargs={'pk': self.object.pk, 'title': self.object.title})

class CollaboList(ListView):
    """CollaboList"""
    model = CollaboModel
    template_name = 'collabo/collabo.html'
    context_object_name = 'collabo_list'
    ordering = ['-created']
    count = 0

    def get_context_data(self, **kwargs):
        context = super(CollaboList, self).get_context_data(**kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context

    def get_queryset(self, **kwargs):
        return Search.search_models(self, CollaboModel)

class CollaboDetail(DetailView):
    """CollaboDetail"""
    model = CollaboModel
    template_name = 'collabo/collabo_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.read += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(CollaboDetail, self).get_context_data(**kwargs)
        obj = self.object
        follow = FollowModel.objects.filter(follower=self.request.user.id).filter(following=obj.author.id)
        liked = False
        followed = False
        if obj.like.filter(id=self.request.user.id).exists():
            liked = True
        if follow.exists():
            followed = True
        if obj.period < datetime.date.today():
            is_period = True
        else:
            is_period = False
        context['liked'] = liked
        context['followed'] = followed
        context['is_period'] = is_period
        context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        context['reply_list'] = obj.comments.filter(parent__isnull=False).select_related('author', 'parent', 'content_type')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'advertise_list': AdvertiseModel.objects.filter(publish=True, type=0).order_by('?')[:1],
            'collabo_list': CollaboModel.objects.filter(publish=True).exclude(title=obj.title).order_by('-created')[:50],
        })
        return context


# Todo
class TodoCreate(CreateView):
    """TodoCreate"""
    model = TodoModel
    fields = ('title', 'content', 'priority', 'duedate')
    template_name = 'todo/todo_create.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(TodoCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:todo_detail', kwargs={'pk': self.object.pk, 'title': self.object.title})

class TodoList(ListView):
    """TodoList"""
    model = TodoModel
    template_name = 'todo/todo.html'
    context_object_name = 'todo_list'
    ordering = ['-duedate']
    count = 0

    def get_context_data(self, **kwargs):
        context = super(TodoList, self).get_context_data(**kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context

    def get_queryset(self, **kwargs):
        return Search.search_todo(self, TodoModel)

class TodoDetail(DetailView):
    """TodoDetail"""
    model = TodoModel
    template_name = 'todo/todo_detail.html'

    def get_queryset(self):
        current_user = self.request.user
        # スーパーユーザの場合、リストにすべてを表示する。
        if current_user.is_superuser:
            return TodoModel.objects.all()
        else:
            # 一般ユーザは自分のレコードのみ表示する。
            return TodoModel.objects.filter(author=current_user.id)

    def get_context_data(self, **kwargs):
        context = super(TodoDetail, self).get_context_data(**kwargs)
        obj = self.object
        context['comment_list'] = obj.comments.filter(parent__isnull=True).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        context.update({
            'searchtag_list': SearchTagModel.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'advertise_list': AdvertiseModel.objects.filter(publish=True, type=0).order_by('?')[:1],
            'todo_list': TodoModel.objects.filter(author_id=self.request.user.id).exclude(title=obj.title),
        })
        return context

class TodoUpdate(UpdateView):
    """TodoUpdate"""
    model = TodoModel
    fields = ('title', 'content', 'priority', 'duedate')
    template_name = 'todo/todo_update.html'

    def get_success_url(self):
        return reverse('myus:todo_detail', kwargs={'pk': self.object.pk, 'title': self.object.title})

class TodoDelete(DeleteView):
    """TodoUpdate"""
    model = TodoModel
    template_name = 'todo/todo_delete.html'
    success_url = reverse_lazy('myus:todo_list')
