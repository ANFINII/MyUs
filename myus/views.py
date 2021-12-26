from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.contenttypes.models import ContentType
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.html import urlize as urlize_impl
from django.db.models import Count, Exists
from django.template.loader import render_to_string
from django.template.defaultfilters import linebreaksbr
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from .forms import SearchTagForm
from .models import SearchTagModel, NotifySettingModel, NotificationModel, CommentModel, FollowModel, TodoModel
from .models import VideoModel, LiveModel, MusicModel, PictureModel, BlogModel, ChatModel, CollaboModel, AdvertiseModel
from .modules.context_data import ContextData
from .modules.get_form import get_detail
from .modules.search import Search
from .modules.success_url import success_url
from .modules.validation import has_username, has_email, has_phone, has_alphabet, has_number
import datetime
import string
import random

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
class Withdrawal(View):
    """退会処理"""
    model = User
    template_name = 'registration/withdrawal.html'
    timestamp_signer = TimestampSigner()
    EXPIRED_SECONDS = 60

    def get_random_chars(self, char_num=30):
        return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(char_num)])

    def get(self, request, token=None, *args, **kwargs):
        context = {}
        context['expired_seconds'] = self.EXPIRED_SECONDS
        if token:
            try:
                unsigned_token = self.timestamp_signer.unsign(token, max_age=datetime.timedelta(seconds=self.EXPIRED_SECONDS))
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
                context['expired_seconds'] = self.EXPIRED_SECONDS
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
class Profile(TemplateView):
    """Profile"""
    model = User
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, Profile, **kwargs)

class ProfileUpdate(UpdateView):
    """アカウント更新"""
    model = User
    fields = ('user_image', 'username', 'email', 'nickname', 'last_name', 'first_name', 'gender', 'phone', 'year', 'month', 'day', 'location', 'introduction')
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('myus:profile')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ProfileUpdate, **kwargs)

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
class MyPage(TemplateView):
    """Myページ遷移"""
    model = User
    template_name = 'registration/mypage.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, MyPage, **kwargs)

class MyPageUpdate(UpdateView):
    """Myページ更新"""
    model = User
    fields = ('mypage_image', 'mypage_email', 'content')
    template_name = 'registration/mypage_update.html'
    success_url = reverse_lazy('myus:mypage')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, MyPageUpdate, **kwargs)

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


# 決済システム
class Payment(TemplateView):
    model = User
    template_name = 'payment/payment.html'

class PaymentCheckout(TemplateView):
    model = User
    template_name = 'payment/checkout.html'

class PaymentSuccess(TemplateView):
    model = User
    template_name = 'payment/success.html'

class PaymentCancel(TemplateView):
    model = User
    template_name = 'payment/cancel.html'

class ChangePlan(TemplateView):
    model = User
    template_name = 'payment/change_plan.html'

def create_checkout_session(request):
    pass


# 通知設定
class Notification(TemplateView):
    """Notification"""
    model = NotifySettingModel
    template_name = 'common/notification.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, Notification, **kwargs)

@csrf_exempt
def notification_setting(request):
    """notification_setting"""
    context = dict()
    if request.method == 'POST':
        user_id = request.user.id
        notify = request.POST.get('notify')
        notify_type = request.POST.get('notify_type')
        notify_obj = NotifySettingModel.objects.get(owner_id=user_id)
        if notify == 'True':
            notify = False
            if notify_type == 'video':
                notify_obj.video = False
            if notify_type == 'live':
                notify_obj.live = False
            if notify_type == 'music':
                notify_obj.music = False
            if notify_type == 'picture':
                notify_obj.picture = False
            if notify_type == 'blog':
                notify_obj.blog = False
            if notify_type == 'chat':
                notify_obj.chat = False
            if notify_type == 'collabo':
                notify_obj.collabo = False
            if notify_type == 'follow':
                notify_obj.follow = False
            if notify_type == 'reply':
                notify_obj.reply = False
            if notify_type == 'like':
                notify_obj.like = False
            if notify_type == 'views':
                notify_obj.views = False
        else:
            notify = True
            if notify_type == 'video':
                notify_obj.video = True
            if notify_type == 'live':
                notify_obj.live = True
            if notify_type == 'music':
                notify_obj.music = True
            if notify_type == 'picture':
                notify_obj.picture = True
            if notify_type == 'blog':
                notify_obj.blog = True
            if notify_type == 'chat':
                notify_obj.chat = True
            if notify_type == 'collabo':
                notify_obj.collabo = True
            if notify_type == 'follow':
                notify_obj.follow = True
            if notify_type == 'reply':
                notify_obj.reply = True
            if notify_type == 'like':
                notify_obj.like = True
            if notify_type == 'views':
                notify_obj.views = True
        notify_obj.save()
        context['notify_setting_lists'] = render_to_string('parts/notify_setting_list.html', {
            'notify_setting_list': NotifySettingModel.objects.filter(owner_id=user_id),
            'notify': notify,
        }, request=request)
        if request.is_ajax():
            return JsonResponse(context)

@csrf_exempt
def notification_confirmed(request):
    """notification_confirmed"""
    user = request.user
    notification_id = request.POST.get('notification_id')
    notification_obj = get_object_or_404(NotificationModel, id=notification_id)
    notification_obj.confirmed.add(user)
    if request.is_ajax():
        return JsonResponse()

@csrf_exempt
def notification_deleted(request):
    """notification_deleted"""
    if request.method == 'POST':
        user = request.user
        notification_id = request.POST.get('notification_id')
        notification_obj = get_object_or_404(NotificationModel, id=notification_id)
        notification_obj.confirmed.add(user)
        notification_obj.deleted.add(user)
        following_id_list = list(FollowModel.objects.filter(follower_id=user.id).values_list('following_id', flat=True))
        context = {
            'notification_count': NotificationModel.objects.filter(user_from_id__in=following_id_list, user_to_id=user.id).exclude(confirmed=user.id).count(),
        }
        if request.is_ajax():
            return JsonResponse(context)


# SearchTag
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


# advertise_read
@csrf_exempt
def advertise_read(request):
    """advertise_read"""
    if request.method == 'POST':
        advertise_id = request.POST.get('advertise_id')
        advertise_obj = AdvertiseModel.objects.get(id=advertise_id)
        advertise_obj.read += 1
        advertise_obj.save()
        context = {
            'read': advertise_obj.read,
        }
        if request.is_ajax():
            return JsonResponse(context)


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
        comment_id = request.POST.get('comment_id')
        obj = get_object_or_404(CommentModel, id=comment_id)
        comment_liked = False
        if obj.like.filter(id=user.id).exists():
            comment_liked = False
            notification_obj = NotificationModel.objects.filter(type_no=9, object_id=obj.id)
            notification_obj.delete()
            obj.like.remove(user)
        else:
            comment_liked = True
            obj.like.add(user)
            if user.id != obj.author.id:
                NotificationModel.objects.create(
                    user_from_id=user.id,
                    user_to_id=obj.author.id,
                    type_no=9,
                    type_name='like',
                    content_object=obj,
                )
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
    context = dict()
    if request.method == 'POST':
        user_id = request.user.id
        text = request.POST.get('text')
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        for models_detail, models in models_comment_dict.items():
            if models_detail in obj_path:
                obj = models.objects.get(id=obj_id)
        comment_obj = CommentModel(content_object=obj)
        comment_obj.text = text
        comment_obj.author_id = user_id
        comment_obj.save()
        context['comment_count'] = obj.comment_count()
        context['comment_lists'] = render_to_string('parts/common/comment/comment.html', {
            'comment_list': obj.comments.filter(id=comment_obj.id).annotate(reply_count=Count('reply')).select_related('author', 'content_type'),
            'user_id': user_id,
            'obj_id': obj_id,
            'obj_path': obj_path,
        }, request=request)
        if request.is_ajax():
            return JsonResponse(context)

@csrf_exempt
def reply_form(request):
    """reply_form"""
    context = dict()
    if request.method == 'POST':
        user_id = request.user.id
        text = request.POST.get('text')
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        comment_id = request.POST.get('comment_id')
        for models_detail, models in models_comment_dict.items():
            if models_detail in obj_path:
                obj = models.objects.get(id=obj_id)
        comment_obj = CommentModel(content_object=obj)
        comment_obj.text = text
        comment_obj.author_id = user_id
        comment_obj.parent = CommentModel.objects.get(id=comment_id)
        comment_obj.save()
        if user_id != comment_obj.parent.author.id:
            NotificationModel.objects.create(
                user_from_id=user_id,
                user_to_id=comment_obj.parent.author.id,
                type_no=10,
                type_name='reply',
                content_object=comment_obj,
            )
        context['comment_count'] = obj.comment_count()
        context['reply_count'] = comment_obj.parent.replies_count()
        context['reply_lists'] = render_to_string('parts/common/reply/reply.html', {
            'reply_list': obj.comments.filter(id=comment_obj.id).select_related('author', 'parent', 'content_type'),
            'user_id': user_id,
            'obj_id': obj_id,
            'comment_id': comment_id,
        }, request=request)
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
        obj_path = request.POST.get('path')
        comment_id = request.POST.get('comment_id')
        for models_detail, models in models_comment_dict.items():
            if models_detail in obj_path:
                obj = models.objects.get(id=obj_id)
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
        notification_obj = NotificationModel.objects.filter(type_no=10, object_id=comment_obj.id)
        notification_obj.delete()
        comment_obj.delete()
        context = {
            'parent_id': comment_obj.parent.id,
            'reply_count': comment_obj.parent.replies_count(),
        }
        if request.is_ajax():
            return JsonResponse(context)


# Index
class Index(ListView):
    """Index処理、すべてのメディアmodelを表示"""
    model = SearchTagModel
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, Index, **kwargs)

    def get_queryset(self):
        return Search.search_index(self)

class Recommend(ListView):
    """急上昇機能、すべてのメディアmodelを表示"""
    model = SearchTagModel
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, Recommend, **kwargs)

    def get_queryset(self):
        return Search.search_recommend(self)


# UserPage
class UserPage(ListView):
    """UserPage"""
    model = User
    template_name = 'userpage/userpage.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, UserPage, **kwargs)

    def get_queryset(self):
        return Search.search_userpage(self)

class UserPageInfo(ListView):
    """UserPageInfo"""
    model = User
    template_name = 'userpage/userpage_information.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, UserPageInfo, **kwargs)

class UserPageAdvertise(ListView):
    """UserPageAdvertise"""
    model = User
    template_name = 'userpage/userpage_advertise.html'
    context_object_name = 'advertise_list'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, UserPageAdvertise, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_advertise(self, AdvertiseModel)


# Follow
class FollowerList(ListView):
    """FollowerList"""
    model = FollowModel
    template_name = 'follow/follower.html'
    context_object_name = 'follower_list'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, FollowerList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_follow(self, FollowModel)

class FollowList(ListView):
    """FollowList"""
    model = FollowModel
    template_name = 'follow/follow.html'
    context_object_name = 'follow_list'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, FollowList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_follow(self, FollowModel)

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
            notification_obj = NotificationModel.objects.filter(type_no=8, object_id=unfollow.id)
            notification_obj.delete()
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
            follow_obj = FollowModel.objects.create(follower=follower, following=following)
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
            NotificationModel.objects.create(
                user_from_id=follower.id,
                user_to_id=following.id,
                type_no=8,
                type_name='follow',
                content_object=follow_obj,
            )
        context = {
            'followed': followed,
            'follower_count': follower_count,
        }
        if request.is_ajax():
            return JsonResponse(context)


# UserPolicy
class UserPolicy(TemplateView):
    """UserPolicy"""
    model = NotificationModel
    template_name = 'common/userpolicy.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, UserPolicy, **kwargs)


# Knowledge
class Knowledge(TemplateView):
    """Knowledge"""
    model = NotificationModel
    template_name = 'common/knowledge.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, Knowledge, **kwargs)


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
        return success_url(self, 'myus:video_detail', 1, 'video')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, VideoCreate, **kwargs)

class VideoList(ListView):
    """VideoList"""
    model = VideoModel
    template_name = 'video/video.html'
    context_object_name = 'video_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, VideoList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, VideoModel)

class VideoDetail(DetailView):
    """VideoDetail"""
    model = VideoModel
    template_name = 'video/video_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, VideoDetail, **kwargs)


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
        return success_url(self, 'myus:live_detail', 2, 'live')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, LiveCreate, **kwargs)

class LiveList(ListView):
    """LiveList"""
    model = LiveModel
    template_name = 'live/live.html'
    context_object_name = 'live_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, LiveList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, LiveModel)

class LiveDetail(DetailView):
    """LiveDetail"""
    model = LiveModel
    template_name = 'live/live_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, LiveDetail, **kwargs)


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
        return success_url(self, 'myus:music_detail', 3, 'music')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, MusicCreate, **kwargs)

class MusicList(ListView):
    """MusicList"""
    model = MusicModel
    template_name = 'music/music.html'
    context_object_name = 'music_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, MusicList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_music(self, MusicModel)

class MusicDetail(DetailView):
    """MusicDetail"""
    model = MusicModel
    template_name = 'music/music_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, MusicDetail, **kwargs)


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
        return success_url(self, 'myus:picture_detail', 4, 'picture')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, PictureCreate, **kwargs)

class PictureList(ListView):
    """PictureList"""
    model = PictureModel
    template_name = 'picture/picture.html'
    context_object_name = 'picture_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, PictureList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, PictureModel)

class PictureDetail(DetailView):
    """PictureDetail"""
    model = PictureModel
    template_name = 'picture/picture_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, PictureDetail, **kwargs)


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
        return success_url(self, 'myus:blog_detail', 5, 'blog')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, BlogCreate, **kwargs)

class BlogList(ListView):
    """BlogList"""
    model = BlogModel
    template_name = 'blog/blog.html'
    context_object_name = 'blog_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, BlogList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_blog(self, BlogModel)

class BlogDetail(DetailView):
    """BlogDetail"""
    model = BlogModel
    template_name = 'blog/blog_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, BlogDetail, **kwargs)


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
        return success_url(self, 'myus:chat_detail', 6, 'chat')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ChatCreate, **kwargs)

class ChatList(ListView):
    """ChatList"""
    model = ChatModel
    template_name = 'chat/chat.html'
    context_object_name = 'chat_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ChatList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, ChatModel)

class ChatDetail(DetailView):
    """ChatDetail"""
    model = ChatModel
    template_name = 'chat/chat_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self)

    def get_context_data(self, **kwargs):
        return ContextData.chat_context_data(self, ChatDetail, **kwargs)

    def get_new_message(self, comment_obj):
        obj = get_object_or_404(ChatModel, id=comment_obj.object_id)
        context = dict()
        context['user_count'] = obj.user_count()
        context['comment_count'] = obj.comment_count()
        context['comment_list'] = obj.comments.filter(id=comment_obj.id).annotate(reply_count=Count('reply')).select_related('author', 'content_type')
        return context

class ChatThread(DetailView):
    """ChatDetailThread"""
    model = ChatModel
    template_name = 'chat/chat_thread.html'

    def get_context_data(self, **kwargs):
        return ContextData.chat_context_data(self, ChatThread, **kwargs)

    def get_new_reply(self, comment_obj):
        obj = get_object_or_404(ChatModel, id=comment_obj.object_id)
        context = dict()
        context['user_count'] = obj.user_count()
        context['reply_count'] = comment_obj.parent.replies_count()
        context['reply_list'] = obj.comments.filter(id=comment_obj.id).select_related('author', 'parent', 'content_type')
        return context


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
        return success_url(self, 'myus:collabo_detail', 7, 'collabo')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, CollaboCreate, **kwargs)

class CollaboList(ListView):
    """CollaboList"""
    model = CollaboModel
    template_name = 'collabo/collabo.html'
    context_object_name = 'collabo_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, CollaboList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, CollaboModel)

class CollaboDetail(DetailView):
    """CollaboDetail"""
    model = CollaboModel
    template_name = 'collabo/collabo_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, CollaboDetail, **kwargs)


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

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, TodoCreate, **kwargs)

class TodoList(ListView):
    """TodoList"""
    model = TodoModel
    template_name = 'todo/todo.html'
    context_object_name = 'todo_list'
    ordering = ['-duedate']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, TodoList, **kwargs)

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
        return ContextData.models_context_data(self, TodoDetail, **kwargs)

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
