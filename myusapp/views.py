from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.db.models import Q, Max, Min, Avg, Count, F, Value
from django.views.generic import View, TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from datetime import date, datetime, timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from itertools import islice, chain
from functools import reduce
from operator import and_
from .models import Tag, SearchTag, Comment, FollowModel, TodoModel
from .models import VideoModel, LiveModel, MusicModel, PictureModel, BlogModel, ChatModel, CollaboModel
from .forms import SearchTagForm, CommentForm
import re, string, random

# Create your views here.

User = get_user_model()

# バリデーション関数定義
def has_username(text):
    if re.fullmatch('^[a-zA-Z0-9_]+$', text) != None:
        return False
    return True

def has_email(text):
    if re.fullmatch('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z.]+$', text) != None:
        return False
    return True

def has_phone(text):
    if re.fullmatch('\d{2,4}-?\d{2,4}-?\d{3,4}', text) != None:
        return False
    return True

def has_alphabet(text):
    if re.search('[a-zA-Z]', text) != None:
        return True
    return False

def has_number(text):
    if re.search('[0-9０-９]', text) != None:
        return True
    return False

def has_tag(text):
    if re.search('.{1,12}', text) != None:
        return True
    return False

def Signup(request):
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
                birthday = date(year=int(year), month=int(month), day=int(day)).isoformat()
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
                    birthday = date(year=int(year), month=int(month), day=int(day))
                    user.birthday = birthday.isoformat()
                    user.age = int((date.today() - birthday).days / days_in_year)
                    
                    user.save()
                    messages.success(request, '登録が完了しました!')
                    return redirect('myus:login')
                else:
                    messages.error(request, 'パスワードが一致していません!')
                    return render(request, 'registration/signup.html')
    return render(request, 'registration/signup.html')

def Login(request):
    """ログイン処理"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('myus:index')
                if user.is_admin:
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

@login_required
def Logout(request):
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
                unsigned_token = self.timestamp_signer.unsign(token, max_age=timedelta(seconds=EXPIRED_SECONDS))
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

def Profile(request):
    """アカウント設定"""
    object_profile = User.objects.all()
    return render(request, 'registration/profile.html', {'object_profile':object_profile})

class Profile_update(UpdateView):
    """アカウント更新"""
    model = User
    fields = ('user_image', 'username', 'email', 'nickname', 'last_name', 'first_name', 'gender', 'phone', 'year', 'month', 'day', 'location', 'profession', 'introduction')
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('myus:profile')
    
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
            birthday = date(year=int(profile.year), month=int(profile.month), day=int(profile.day))
            profile.birthday = birthday.isoformat()
            days_in_year = 365.2425
            profile.age = int((date.today() - birthday).days / days_in_year)

            profile.save()
            return super(Profile_update, self).form_valid(form)
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
    
def MyPage(request):
    """Myページ遷移"""
    object_profile = User.objects.all()
    return render(request, 'registration/mypage.html', {'object_profile':object_profile})
    
class MyPage_update(UpdateView):
    """Myページ更新"""
    model = User
    fields = ('mypage_image', 'mypage_email', 'content')
    template_name = 'registration/mypage_update.html'
    success_url = reverse_lazy('myus:mypage')
    
    def form_valid(self, form):
        """バリデーションに成功した時"""
        try:
            userpage = form.save(commit=False)
            userpage.mypage_image = self.request.user.mypage_image
            userpage.content = self.request.user.content
            
            userpage.mypage_email = self.request.user.mypage_email
            if has_email(self.request.user.mypage_email):
                messages.error(self.request, 'メールアドレスの形式が違います!')
                return super().form_invalid(form)
            userpage.save()
            return super(MyPage_update, self).form_valid(form)
        except ValueError:
            messages.error(self.request, '更新できませんでした!')
            return super().form_invalid(form)

    def form_invalid(self, form):
        """バリデーションに失敗した時"""
        if has_email(self.request.user.mypage_email):
            messages.error(self.request, 'メールアドレスの形式が違います!')
            return super().form_invalid(form)
        
    def get_object(self):
        return self.request.user
    
class UserPage(ListView):
    """UserPageを表示"""
    model = User
    template_name = 'registration/userpage.html'
    form_class = SearchTagForm

    def get_context_data(self, **kwargs):
        context = super(UserPage, self).get_context_data(**kwargs)
        author = get_object_or_404(User, nickname=self.kwargs['nickname'])
        context['author_name'] = author
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'user_list': User.objects.filter(nickname=author),
            'video_list': VideoModel.objects.filter(author_id=author, publish=True),
            'live_list': LiveModel.objects.filter(author_id=author, publish=True),
            'music_list': MusicModel.objects.filter(author_id=author, publish=True),
            'picture_list': PictureModel.objects.filter(author_id=author, publish=True),
            'blog_list': BlogModel.objects.filter(author_id=author, publish=True),
            'chat_list': ChatModel.objects.filter(author_id=author, publish=True),
        })
        return context

# SearchTag追加
class TagCreate(CreateView):
    model = SearchTag
    fields = ('searchtag',)
    template_name = 'base2.html'
    success_url = reverse_lazy('myus:tag_list')

class TagList(ListView):
    model = SearchTag
    template_name = 'base2.html'

class Index(ListView):
    """Index処理、すべてのメディアmodelを表示"""
    model = SearchTag
    template_name = 'index.html'
    form_class = SearchTagForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            form.instance.author_id = self.request.user.id
            form.save()
        return redirect('myus:index')

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'video_list': VideoModel.objects.filter(publish=True).order_by('-created')[:8],
            'live_list': LiveModel.objects.filter(publish=True).order_by('-created')[:8],
            'music_list': MusicModel.objects.filter(publish=True).order_by('-created')[:8],
            'picture_list': PictureModel.objects.filter(publish=True).order_by('-created')[:8],
            'blog_list': BlogModel.objects.filter(publish=True).order_by('-created')[:8],
            'chat_list': ChatModel.objects.filter(publish=True).order_by('-created')[:8],
        })
        return context

    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search')
    #     # result_list = []
    #     video_list = VideoModel.objects.filter(
    #                 Q(title__icontains=search) |
    #                 Q(content__icontains=search) |
    #                 Q(author__nickname__icontains=search) |
    #                 Q(tags__tag__icontains=search)
    #             )
    #     live_list = LiveModel.objects.filter(
    #                 Q(title__icontains=search) |
    #                 Q(content__icontains=search) |
    #                 Q(author__nickname__icontains=search) |
    #                 Q(tags__tag__icontains=search)
    #             )
    #     music_list = MusicModel.objects.filter(publish=True)
    #     picture_list = PictureModel.objects.filter(publish=True)
    #     blog_list = BlogModel.objects.filter(publish=True)
    #     chat_list = ChatModel.objects.filter(publish=True)
    #     # result_list.append(video_list)
    #     result_list = list(chain(video_list, live_list, music_list, picture_list, blog_list, chat_list))
    #     return result_list

class Recommend(ListView):
    """急上昇機能、すべてのメディアmodelを表示"""
    model = SearchTag
    template_name = 'index.html'
    form_class = SearchTagForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            form.instance.author_id = self.request.user.id
            form.save()
        return redirect('myus:recommend')

    def get_context_data(self, **kwargs):
        context = super(Recommend, self).get_context_data(**kwargs)    
        # 急上昇はcreatedが1日以内かつscoreが10000以上の上位8レコード
        # テストはcreatedが50日以内かつscoreが50以上の上位8レコード
        # socreはread + like*10
        aggregation_date = datetime.today() - timedelta(days=50)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'video_list': VideoModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10).filter(score__gte=50).order_by('-score')[:8],
            'live_list': LiveModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10).filter(score__gte=50).order_by('-score')[:8],
            'music_list': MusicModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10).filter(score__gte=50).order_by('-score')[:8],
            'picture_list': PictureModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10).filter(score__gte=50).order_by('-score')[:8],
            'blog_list': BlogModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10).filter(score__gte=50).order_by('-score')[:8],
            'chat_list': ChatModel.objects.filter(publish=True).filter(created__gte=aggregation_date).annotate(score=F('read') + Count('like')*10).filter(score__gte=50).order_by('-score')[:8],
        })
        return context
    
# Follow
class FollowCreate(CreateView):
    """ここにメソッドの説明を記述する"""
    model = FollowModel
    fields = ('follower', 'following')
    template_name = 'follow/follow_create.html'
    success_url = reverse_lazy('myus:follow_list')
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(FollowCreate, self).form_valid(form)

class FollowList(ListView):
    """FollowListを表示"""
    model = FollowModel
    template_name = 'follow/follow.html'
    context_object_name = 'follow_list'
    form_class = SearchTagForm
    
    def get_context_data(self, **kwargs):
        context = super(FollowList, self).get_context_data(**kwargs)
        # follower__username = user.username フォロー数
        # following__username = user.username フォロワー数
        context['follower_count'] = FollowModel.objects.filter(following_id=self.request.user.id).count()
        context['following_count'] = FollowModel.objects.filter(follower_id=self.request.user.id).count()
        context['follower_counts'] = FollowModel.objects.filter(follower__isnull=False, follower__username__exact=self.kwargs.get('username'))
        context['following_counts'] = FollowModel.objects.filter(following__isnull=False, following__username__exact=self.kwargs.get('username'))
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context

    def get_queryset(self, **kwargs):
        result = FollowModel.objects.filter(follower_id=self.request.user.id)
        search = self.request.GET.get('search')

        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(following__nickname__icontains=q) |
                        Q(following__introduction__icontains=q) for q in q_list]
                    )
            result = result.filter(query).distinct()
            if not result:
                messages.success(self.request, '「{}」の検索結果なし'.format(search))
            else:
                messages.success(self.request, '「{}」の検索結果'.format(search))
        return result

class FollowerList(ListView):   
    """FollowerListを表示"""
    model = FollowModel
    template_name = 'follow/follower.html'
    context_object_name = 'follower_list'
    form_class = SearchTagForm
    
    def get_context_data(self, **kwargs):
        context = super(FollowerList, self).get_context_data(**kwargs)
        # follower__username = user.username フォロー数
        # following__username = user.username フォロワー数
        # user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['follower_count'] = FollowModel.objects.filter(following_id=self.request.user.id).count()
        context['following_count'] = FollowModel.objects.filter(follower_id=self.request.user.id).count()
        context['follower_counts'] = FollowModel.objects.filter(follower__isnull=False, follower__username__exact=self.kwargs.get('username'))
        context['following_counts'] = FollowModel.objects.filter(following__isnull=False, following__username__exact=self.kwargs.get('username'))
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context

    def get_queryset(self, **kwargs):
        result = FollowModel.objects.filter(following_id=self.request.user.id)
        search = self.request.GET.get('search')

        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(follower__nickname__icontains=q) |
                        Q(follower__introduction__icontains=q) for q in q_list]
                    )
            result = result.filter(query).distinct()
            if not result:
                messages.success(self.request, '「{}」の検索結果なし'.format(search))
            else:
                messages.success(self.request, '「{}」の検索結果'.format(search))
        return result

# 利用規約
def UserPolicy(request):
    """ここにメソッドの説明を記述する"""
    object_UserPolicy = User.objects.all()
    return render(request, 'common/userpolicy.html', {'object_UserPolicy':object_UserPolicy})

# Knowledge Base
def Knowledge(request):
    """ここにメソッドの説明を記述する"""
    object_knowledge = User.objects.all()
    return render(request, 'common/knowledge.html', {'object_knowledge':object_knowledge})

# Video
class VideoCreate(CreateView):
    """ここにメソッドの説明を記述する"""
    model = VideoModel
    fields = ('title', 'content', 'images', 'videos')
    template_name = 'video/video_create.html'
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(VideoCreate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('myus:video_detail', kwargs={'pk': self.object.pk})

class VideoList(ListView):
    """ここにメソッドの説明を記述する"""
    model = VideoModel
    template_name = 'video/video.html'
    context_object_name = 'video_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(VideoList, self).get_context_data(**kwargs)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context
    
    def get_queryset(self, **kwargs):
        result = VideoModel.objects.filter(publish=True)
        search = self.request.GET.get('search')

        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(title__icontains=q) |
                        Q(tags__tag__icontains=q) |
                        Q(author__nickname__icontains=q) |
                        Q(content__icontains=q) for q in q_list]
                    )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10).order_by('-score').distinct()
            if not result:
                messages.success(self.request, '「{}」の検索結果なし'.format(search))
            else:
                messages.success(self.request, '「{}」の検索結果'.format(search))
        return result

class VideoDetail(DetailView, FormView):
    model = VideoModel
    template_name = 'video/video_detail.html'
    ordering = ['-created']
    form_class = CommentForm
    success_url = 'video_detail'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.read += 1
        self.object.save() 
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        video_pk = self.kwargs['pk']
        target = get_object_or_404(VideoModel, pk=video_pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.content_object = target
            form.author_id = self.request.user.id
            form.save()
            return redirect('myus:video_detail', pk=video_pk)
        return FormView.post(self, request, *args, **kwargs)
    
    # def post(self, request, comment_pk, *args, **kwargs):
    #     form = self.form_class(self.request.POST)
    #     comment = self.request.POST.get('text')
    #     reply = self.request.POST.get('text2')
    #     video_pk = self.kwargs['pk']
    #     video = get_object_or_404(VideoModel, pk=video_pk)
    #     comments = get_object_or_404(VideoModel, pk=video_pk, parent=comment_pk)
    #     if comment:
    #         if form.is_valid():
    #             if request.is_ajax():
    #                 # Ajax 処理を別メソッドに切り離す
    #                 form = form.save(commit=False)
    #                 form.author_id = self.request.user.id
    #                 form.content_object = video
    #                 form.save()
    #                 return self.ajax_response(form)
    #             return super().form_valid(form)
    #     elif reply:
    #         if form.is_valid():
    #             if request.is_ajax():
    #                 # Ajax 処理を別メソッドに切り離す
    #                 form = form.save(commit=False)
    #                 form.author_id = self.request.user.id
    #                 form.content_object = comments
    #                 # form.parent = self.object.comments.parent_id
    #                 form.save()
    #                 return self.ajax_response(form)
    #                 # return HttpResponse(form)
    #             return super().form_valid(form)
    #     return super().form_invalid(form)
    
    # def ajax_response(self, form):
    #     # jQueryに対してレスポンスを返すメソッド
    #     text = form.cleaned_data.get('text')
    #     return HttpResponse(text)

    def get_context_data(self, **kwargs):
        context = super(VideoDetail, self).get_context_data(**kwargs)
        video = get_object_or_404(VideoModel, id=self.kwargs['pk'])
        total_like = video.total_like()
        liked = False
        if video.like.filter(id=self.request.user.id).exists():
            liked = True
        context['total_like'] = total_like
        context['liked'] = liked
        context['comment_list'] = self.object.comments.filter(parent__isnull=True)
        context['reply_list'] = self.object.comments.filter(parent__isnull=False)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'video_list': VideoModel.objects.filter(publish=True)[:50],
        })
        return context

def VideoLike(request, content_type, pk):
    video = get_object_or_404(VideoModel, id=request.POST.get('video_id'))
    liked = False
    if video.like.filter(id=request.user.id).exists():
        video.like.remove(request.user)
        liked = False
    else:
        video.like.add(request.user)
        liked = True

    context={
       'video': video,
       'liked': liked,
    }    
    if request.is_ajax():
        html = render_to_string('video/video_detail.html', context, request=request)
        return JsonResponse({'form': html})
    # return HttpResponseRedirect(reverse('myus:video_detail', args=[str(pk)]))

# Live
class LiveCreate(CreateView):
    """ここにメソッドの説明を記述する"""
    model = LiveModel
    fields = ('title', 'content', 'images', 'lives')
    template_name = 'live/live_create.html'
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(LiveCreate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('myus:live_detail', kwargs={'pk': self.object.pk})

class LiveList(ListView):
    """ここにメソッドの説明を記述する"""
    model = LiveModel
    template_name = 'live/live.html'
    context_object_name = 'live_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(LiveList, self).get_context_data(**kwargs)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context
    
    def get_queryset(self, **kwargs):
        result = LiveModel.objects.filter(publish=True)
        search = self.request.GET.get('search')
        
        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(title__icontains=q) |
                        Q(tags__tag__icontains=q) |
                        Q(author__nickname__icontains=q) |
                        Q(content__icontains=q) for q in q_list]
                    )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10).order_by('-score').distinct()
            if not result:
                messages.success(self.request, '「{}」の検索結果なし'.format(search))
            else:
                messages.success(self.request, '「{}」の検索結果'.format(search))
        return result

class LiveDetail(DetailView):
    model = LiveModel
    template_name = 'live/live_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LiveDetail, self).get_context_data(**kwargs)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'live_list': LiveModel.objects.filter(publish=True)[:50],
        })
        return context

def LiveLike(request, pk):
    """ここにメソッドの説明を記述する"""
    post = LiveModel.objects.get(pk=pk)
    post.like = post.like + 1
    post.save()
    return redirect('myus:live_detail', pk=post.pk)
    
def LiveRead(request, pk):
    """ここにメソッドの説明を記述する"""
    post = LiveModel.objects.get(pk=pk)
    post2 = request.user.get_username()
    if post2 in post.readtext:
        return redirect('myus:live_detail', pk=post.pk)
    else:
        post.read += 1
        post.readtext = post.readtext + ' ' + post2
        post.save()
        return redirect('myus:live_detail', pk=post.pk)

# Music
class MusicCreate(CreateView):
    """ここにメソッドの説明を記述する"""
    model = MusicModel
    fields = ('title', 'content', 'musics', 'lyrics')
    template_name = 'music/music_create.html'
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(MusicCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:music_detail', kwargs={'pk': self.object.pk})

class MusicList(ListView):
    """ここにメソッドの説明を記述する"""
    model = MusicModel
    template_name = 'music/music.html'
    context_object_name = 'music_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(MusicList, self).get_context_data(**kwargs)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context
    
    def get_queryset(self, **kwargs):
        result = MusicModel.objects.filter(publish=True)
        search = self.request.GET.get('search')
        
        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(title__icontains=q) |
                        Q(tags__tag__icontains=q) |
                        Q(author__nickname__icontains=q) |
                        Q(content__icontains=q) |
                        Q(lyrics__icontains=q) for q in q_list]
                    )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10).order_by('-score').distinct()
            if not result:
                messages.success(self.request, '「{}」の検索結果なし'.format(search))
            else:
                messages.success(self.request, '「{}」の検索結果'.format(search))
        return result

class MusicDetail(DetailView):
    model = MusicModel
    template_name = 'music/music_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MusicDetail, self).get_context_data(**kwargs)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'music_list': MusicModel.objects.filter(publish=True)[:50],
        })
        return context

def MusicLike(request, pk):
    """ここにメソッドの説明を記述する"""
    post = MusicModel.objects.get(pk=pk)
    post.like = post.like + 1
    post.save()
    return redirect('myus:music_detail', pk=post.pk)
    
def MusicRead(request, pk):
    """ここにメソッドの説明を記述する"""
    post = MusicModel.objects.get(pk=pk)
    post2 = request.user.get_username()
    if post2 in post.readtext:
        return redirect('myus:music_detail', pk=post.pk)
    else:
        post.read += 1
        post.readtext = post.readtext + ' ' + post2
        post.save()
        return redirect('myus:music_detail', pk=post.pk)

# Picture
class PictureCreate(CreateView):
    """ここにメソッドの説明を記述する"""
    model = PictureModel
    fields = ('title', 'content', 'images')
    template_name = 'picture/picture_create.html'
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(PictureCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:picture_detail', kwargs={'pk': self.object.pk})

class PictureList(ListView):
    """ここにメソッドの説明を記述する"""
    model = PictureModel
    template_name = 'picture/picture.html'
    context_object_name = 'picture_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(PictureList, self).get_context_data(**kwargs)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context
    
    def get_queryset(self, **kwargs):
        result = PictureModel.objects.filter(publish=True)
        search = self.request.GET.get('search')
        
        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(title__icontains=q) |
                        Q(tags__tag__icontains=q) |
                        Q(author__nickname__icontains=q) |
                        Q(content__icontains=q) for q in q_list]
                    )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10).order_by('-score').distinct()
            if not result:
                messages.success(self.request, '「{}」の検索結果なし'.format(search))
            else:
                messages.success(self.request, '「{}」の検索結果'.format(search))
        return result

class PictureDetail(DetailView):
    model = PictureModel
    template_name = 'picture/picture_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PictureDetail, self).get_context_data(**kwargs)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'picture_list': PictureModel.objects.filter(publish=True)[:50],
        })
        return context

def PictureLike(request, pk):
    """ここにメソッドの説明を記述する"""
    post = PictureModel.objects.get(pk=pk)
    post.like = post.like + 1
    post.save()
    return redirect('myus:picture_detail', pk=post.pk)
    
def PictureRead(request, pk):
    """ここにメソッドの説明を記述する"""
    post = PictureModel.objects.get(pk=pk)
    post2 = request.user.get_username()
    if post2 in post.read:
        return redirect('myus:picture_detail', pk=post.pk)
    else:
        post.read += 1
        post.read = post.read + ' ' + post2
        post.save()
        return redirect('myus:picture_detail', pk=post.pk)

# Blog
class BlogCreate(CreateView):
    """ここにメソッドの説明を記述する"""
    model = BlogModel
    fields = ('title', 'content', 'images', 'richtext')
    template_name = 'blog/blog_create.html'
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(BlogCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:blog_detail', kwargs={'pk': self.object.pk})

class BlogList(ListView):
    """ここにメソッドの説明を記述する"""
    model = BlogModel
    template_name = 'blog/blog.html'
    context_object_name = 'blog_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context
    
    def get_queryset(self, **kwargs):
        result = BlogModel.objects.filter(publish=True)
        search = self.request.GET.get('search')
        
        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(title__icontains=q) |
                        Q(tags__tag__icontains=q) |
                        Q(author__nickname__icontains=q) |
                        Q(content__icontains=q) |
                        Q(richtext__icontains=q) for q in q_list]
                    )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10).order_by('-score').distinct()
            if not result:
                messages.success(self.request, '「{}」の検索結果なし'.format(search))
            else:
                messages.success(self.request, '「{}」の検索結果'.format(search))
        return result

class BlogDetail(DetailView):
    model = BlogModel
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'blog_list': BlogModel.objects.filter(publish=True)[:50],
        })
        return context

def BlogLike(request, pk):
    """ここにメソッドの説明を記述する"""
    post = BlogModel.objects.get(pk=pk)
    post.like = post.like + 1
    post.save()
    return redirect('myus:blog_detail', pk=post.pk)
    
def BlogRead(request, pk):
    """ここにメソッドの説明を記述する"""
    post = BlogModel.objects.get(pk=pk)
    post2 = request.user.get_username()
    if post2 in post.readtext:
        return redirect('myus:blog_detail', pk=post.pk)
    else:
        post.read += 1
        post.readtext = post.readtext + ' ' + post2
        post.save()
        return redirect('myus:blog_detail', pk=post.pk)

# Chat
class ChatCreate(CreateView):
    """ここにメソッドの説明を記述する"""
    model = ChatModel
    fields = ('title', 'content')
    template_name = 'chat/chat_create.html'
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(ChatCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:chat_detail', kwargs={'pk': self.object.pk})

class ChatList(ListView):
    """ここにメソッドの説明を記述する"""
    model = ChatModel
    template_name = 'chat/chat.html'
    context_object_name = 'chat_list'
    ordering = ['-created']
    
    def get_context_data(self, **kwargs):
        context = super(ChatList, self).get_context_data(**kwargs)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context
    
    def get_queryset(self, **kwargs):
        result = ChatModel.objects.filter(publish=True)
        search = self.request.GET.get('search')
        
        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(title__icontains=q) |
                        Q(tags__tag__icontains=q) |
                        Q(author__nickname__icontains=q) |
                        Q(content__icontains=q) for q in q_list]
                    )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10).order_by('-score').distinct()
            if not result:
                messages.success(self.request, '「{}」の検索結果なし'.format(search))
            else:
                messages.success(self.request, '「{}」の検索結果'.format(search))
        return result

class ChatDetail(DetailView):
    model = ChatModel
    template_name = 'chat/chat_detail.html'
    ordering = ['-created']
    form_class = CommentForm
    success_url = 'chat_detail'
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        chat_pk = self.kwargs['pk']
        target = get_object_or_404(ChatModel, pk=chat_pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.content_object = target
            form.author_id = self.request.user.id
            form.save()
            return redirect('myus:chat_detail', pk=chat_pk)
        return FormView.post(self, request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ChatDetail, self).get_context_data(**kwargs)
        chat = get_object_or_404(ChatModel, id=self.kwargs['pk'])
        total_like = chat.total_like()
        liked = False
        if chat.like.filter(id=self.request.user.id).exists():
            liked = True
        context['total_like'] = total_like
        context['liked'] = liked
        context['comment_list'] = self.object.comments.filter(parent__isnull=True)
        context['reply_list'] = self.object.comments.filter(parent__isnull=False)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'chat_list': ChatModel.objects.filter(publish=True)[:50],
        })
        return context

def ChatLike(request, pk):
    """ここにメソッドの説明を記述する"""
    post = ChatModel.objects.get(pk=pk)
    post.like = post.like + 1
    post.save()
    return redirect('myus:chat_detail', pk=post.pk)

# Collabo
class CollaboCreate(CreateView):
    """ここにメソッドの説明を記述する"""
    model = CollaboModel
    fields = ('title', 'content')
    template_name = 'collabo/collabo_create.html'
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(CollaboCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:collabo_detail', kwargs={'pk': self.object.pk})

class CollaboList(ListView):
    """ここにメソッドの説明を記述する"""
    model = CollaboModel
    template_name = 'collabo/collabo.html'
    context_object_name = 'collabo_list'
    ordering = ['-created']
    
    def get_context_data(self, **kwargs):
        context = super(CollaboList, self).get_context_data(**kwargs)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
        })
        return context
    
    def get_queryset(self, **kwargs):
        result = CollaboModel.objects.filter(publish=True)
        search = self.request.GET.get('search')
        
        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(title__icontains=q) |
                        Q(tags__tag__icontains=q) |
                        Q(author__nickname__icontains=q) |
                        Q(content__icontains=q) for q in q_list]
                    )
            result = result.filter(query).annotate(score=F('read') + Count('like')*10).order_by('-score').distinct()
            if not result:
                messages.success(self.request, '「{}」の検索結果なし'.format(search))
            else:
                messages.success(self.request, '「{}」の検索結果'.format(search))
        return result

class CollaboDetail(DetailView):
    model = CollaboModel
    template_name = 'collabo/collabo_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CollaboDetail, self).get_context_data(**kwargs)
        context.update({
            'searchtag_list': SearchTag.objects.filter(author_id=self.request.user.id).order_by('sequence')[:10],
            'collabo_list': CollaboModel.objects.filter(publish=True)[:50],
        })
        return context

def CollaboLike(request, pk):
    """ここにメソッドの説明を記述する"""
    post = CollaboModel.objects.get(pk=pk)
    post.like = post.like + 1
    post.save()
    return redirect('myus:collabo_detail', pk=post.pk)
    
def CollaboRead(request, pk):
    """ここにメソッドの説明を記述する"""
    post = CollaboModel.objects.get(pk=pk)
    post2 = request.user.get_username()
    if post2 in post.readtext:
        return redirect('myus:collabo_detail', pk=post.pk)
    else:
        post.read += 1
        post.readtext = post.readtext + ' ' + post2
        post.save()
        return redirect('myus:collabo_detail', pk=post.pk)

# Todo
class TodoCreate(CreateView):
    model = TodoModel
    fields = ('title', 'content', 'priority', 'duedate')    
    template_name = 'todo/todo_create.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(TodoCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:todo_detail', kwargs={'pk': self.object.pk})

class TodoList(ListView):
    model = TodoModel
    template_name = 'todo/todo.html'
    context_object_name = 'todo_list'
    ordering = ['-duedate']

    def get_queryset(self, **kwargs):
        result = TodoModel.objects.filter(author_id=self.request.user.id)
        search = self.request.GET.get('search')
        
        if search:
            """除外リストを作成"""
            exclusion_list = set([' ', '　'])
            q_list = ''
            for i in search:
                """全角半角の空文字が含まれたら無視"""
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [
                        Q(title__icontains=q) |
                        Q(content__icontains=q) |
                        Q(duedate__icontains=q) for q in q_list]
                    )
            result = result.filter(query).order_by('-duedate').distinct()
            if not result:
                messages.success(self.request, '「{}」の検索結果なし'.format(search))
            else:
                messages.success(self.request, '「{}」の検索結果'.format(search))
        return result

class TodoDetail(DetailView):
    model = TodoModel
    template_name = 'todo/todo_detail.html'
    
    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_superuser: # スーパーユーザの場合、リストにすべてを表示する。
            return TodoModel.objects.all()
        else: # 一般ユーザは自分のレコードのみ表示する。
            return TodoModel.objects.filter(author=current_user.id)
    
    def get_context_data(self, **kwargs):
        context = super(TodoDetail, self).get_context_data(**kwargs)
        context.update({
            'todo_list': TodoModel.objects.filter(author_id=self.request.user.id),
        })
        return context

class TodoUpdate(UpdateView):
    model = TodoModel
    fields = ('title', 'content', 'priority', 'duedate')
    template_name = 'todo/todo_update.html'

    def get_success_url(self):
        return reverse('myus:todo_detail', kwargs={'pk': self.object.pk})
    
class TodoDelete(DeleteView):
    model = TodoModel
    template_name = 'todo/todo_delete.html'
    success_url = reverse_lazy('myus:todo_list')