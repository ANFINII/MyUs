import datetime
import logging
import json
import os
import random
import string
import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template.defaultfilters import linebreaksbr
from django.urls import reverse, reverse_lazy
from django.utils.html import urlize as urlize_impl
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.myus.forms import SearchTagForm
from apps.myus.models import Profile, MyPage, SearchTag, NotificationSetting
from apps.myus.models import Notification, Follow, Comment, Advertise
from apps.myus.models import Video, Live, Music, Picture, Blog, Chat, Collabo, Todo
from apps.myus.convert.convert_hls import convert_exe
from apps.myus.modules.contains import NotificationTypeNo, models_like_dict, models_comment_dict
from apps.myus.modules.context_data import ContextData
from apps.myus.modules.get_form import get_detail
from apps.myus.modules.pjax import pjax_context
from apps.myus.modules.notification import notification_data, notification_setting_update
from apps.myus.modules.search import Search
from apps.myus.modules.success_url import success_url
from apps.myus.modules.follow import follow_update_data
from apps.myus.modules.validation import has_username, has_email, has_phone, has_postal_code, has_alphabet, has_number


# Create your views here.

User = get_user_model()

# Signup
def signup_form(request):
    """サインアップ処理"""
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username).count():
            messages.error(request, 'このユーザー名は既に登録されております!')
            return render(request, 'registration/signup.html')

        if has_username(username):
            messages.error(request, 'ユーザー名は半角英数字のみ入力できます!')
            return render(request, 'registration/signup.html')

        nickname = request.POST['nickname']
        if User.objects.filter(nickname=nickname).count():
            messages.error(request, 'この投稿者名は既に登録されております!')
            return render(request, 'registration/signup.html')

        email = request.POST['email']
        if User.objects.filter(email=email).count():
            messages.error(request, 'このメールアドレスは既に登録されております!')
            return render(request, 'registration/signup.html')

        if has_email(email):
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
                messages.error(request, f'{year}年{month}月{day}日は存在しない日付です!')
                return render(request, 'registration/signup.html')
            try:
                User.objects.get(username=username)
                messages.error(request, 'このアカウントは既に登録されております!')
                return render(request, 'registration/signup.html')
            except User.DoesNotExist:
                if password1==password2:
                    user = User.objects.create_user(username, email, password1)
                    user.nickname = nickname
                    user.last_name = last_name
                    user.first_name = first_name
                    user.gender = gender
                    user.birthday = birthday
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


# pjax
def pjax(request):
    if request.method == 'GET':
        href = request.GET.get('href').lstrip('/')
        context = pjax_context(request, href)
        return JsonResponse(context)


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
        user = self.request.user
        context = {}
        notification_list = notification_data(self)
        if user.id is not None:
            context = {
                'expired_seconds': self.EXPIRED_SECONDS,
                'notification_list': notification_list['notification_list'],
                'notification_count': notification_list['notification_count'],
            }
        if token:
            try:
                self.timestamp_signer.unsign(token, max_age=datetime.timedelta(seconds=self.EXPIRED_SECONDS))
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
                token = self.get_random_chars()
                notification_list = notification_data(self)
                context = {
                    'token_signed': self.timestamp_signer.sign(token),
                    'expired_seconds': self.EXPIRED_SECONDS,
                    'notification_list': notification_list['notification_list'],
                    'notification_count': notification_list['notification_count'],
                }
                return render(request, self.template_name, context)
            elif self.request.user.check_password(password2):
                user = self.request.user
                user.is_active = False
                user.save(update_fields=['is_active'])
                logout(self.request)
                messages.error(self.request, '退会しました!')
                return redirect('myus:login')
            else:
                messages.error(self.request, 'パスワードが違います!')
                return redirect('myus:withdrawal')


# Profile
class ProfileView(TemplateView):
    """Profile"""
    model = Profile
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ProfileView, **kwargs)

class ProfileUpdate(UpdateView):
    """アカウント更新"""
    model = Profile
    fields = ('image', 'last_name', 'first_name', 'gender', 'phone', 'postal_code', 'prefecture', 'city', 'address', 'building', 'introduction')
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('myus:profile')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ProfileUpdate, **kwargs)

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        """バリデーションに成功した時"""
        try:
            user = self.request.user
            user.email = self.request.POST['email']
            user.username = self.request.POST['username']
            user.nickname = self.request.POST['nickname']

            if has_email(user.email):
                messages.error(self.request, 'メールアドレスの形式が違います!')
                return super().form_invalid(form)

            if has_username(user.username):
                messages.error(self.request, 'ユーザー名は半角英数字のみ入力できます!')
                return super().form_invalid(form)

            if has_number(self.request.POST['last_name']):
                messages.error(self.request, '姓に数字が含まれております!')
                return super().form_invalid(form)

            if has_number(self.request.POST['first_name']):
                messages.error(self.request, '名に数字が含まれております!')
                return super().form_invalid(form)

            if has_phone(self.request.POST['phone']):
                messages.error(self.request, '電話番号の形式が違います!')
                return super().form_invalid(form)

            if has_postal_code(self.request.POST['postal_code']):
                messages.error(self.request, '郵便番号の形式が違います!')
                return super().form_invalid(form)

            profile_obj = form.save(commit=False)
            year = self.request.POST['year']
            month = self.request.POST['month']
            day = self.request.POST['day']
            birthday = datetime.date(year=int(year), month=int(month), day=int(day))
            profile_obj.birthday = birthday.isoformat()

            user.save()
            return super(ProfileUpdate, self).form_valid(form)
        except ValueError:
            messages.error(self.request, f'{year}年{month}月{day}日は存在しない日付です!')
            return super().form_invalid(form)
        except IntegrityError:
            messages.error(self.request, '更新できませんでした!')
            return super().form_invalid(form)

    def form_invalid(self, form):
        """バリデーションに失敗した時"""
        messages.error(self.request, 'ユーザー名またはメールアドレス、投稿者名は既に登録済みです!')
        return super().form_invalid(form)


# MyPage
class MyPageView(TemplateView):
    """Myページ遷移"""
    model = MyPage
    template_name = 'registration/mypage.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, MyPageView, **kwargs)

class MyPageUpdate(UpdateView):
    """Myページ更新"""
    model = MyPage
    fields = ('banner', 'email', 'content')
    template_name = 'registration/mypage_update.html'
    success_url = reverse_lazy('myus:mypage')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, MyPageUpdate, **kwargs)

    def get_object(self):
        return MyPage.objects.get(user=self.request.user)

    def form_valid(self, form):
        """バリデーションに成功した時"""
        try:
            if has_email(self.request.POST['email']):
                messages.error(self.request, 'メールアドレスの形式が違います!')
                return super().form_invalid(form)
            return super(MyPageUpdate, self).form_valid(form)
        except (ValueError, TypeError, IntegrityError) as e:
            messages.error(self.request, '更新できませんでした!')
            return super().form_invalid(form)

    def form_invalid(self, form):
        """バリデーションに失敗した時"""
        messages.error(self.request, 'メールアドレスの形式が違います!')
        return super().form_invalid(form)

def mypage_toggle(request):
    """mypage_toggle"""
    context = {}
    if request.method == 'POST':
        user = request.user
        is_advertise = request.POST.get('is_advertise')
        myapge_obj = MyPage.objects.get(user=user)
        myapge_obj.is_advertise = True if is_advertise == 'False' else False
        myapge_obj.save(update_fields=['is_advertise'])
        context['toggle_mypage'] = render_to_string('registration/mypage_advertise.html', {
            'mypage_list': MyPage.objects.filter(user=user),
        }, request=request)
        return JsonResponse(context)


# 決済システム
class Payment(TemplateView):
    model = User
    template_name = 'payment/payment.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, Payment, **kwargs)

class PaymentSuccess(TemplateView):
    template_name = 'payment/success.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, PaymentSuccess, **kwargs)

class PaymentCancel(TemplateView):
    template_name = 'payment/cancel.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, PaymentCancel, **kwargs)

class ChangePlan(TemplateView):
    model = User
    template_name = 'payment/change_plan.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ChangePlan, **kwargs)

def create_checkout_session(request):
    stripe.myus_key = settings.STRIPE_SECRET_KEY
    post_data = json.loads(request.body.decode('utf-8'))
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price': post_data['priceId'], 'quantity': 1}],
            mode='subscription',
            success_url=request.build_absolute_uri(reverse('myus:payment_success')),
            cancel_url=request.build_absolute_uri(reverse('myus:payment_cancel')),
        )
        return JsonResponse({'id': checkout_session.id, 'publicKey': settings.STRIPE_PUBLIC_KEY})
    except Exception as e:
        return JsonResponse({'error':str(e)})


# 通知設定
class NotificationSettingView(TemplateView):
    """NotificationSettingView"""
    model = NotificationSetting
    template_name = 'common/notification.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, NotificationSettingView, **kwargs)

def notification_setting(request):
    """notification_setting"""
    context = {}
    if request.method == 'POST':
        user = request.user
        is_notification = request.POST.get('notification')
        notification_type = request.POST.get('notification_type')
        notification_obj = NotificationSetting.objects.get(user=user)
        notification_setting_update(is_notification, notification_type, notification_obj)
    context['notification_setting_lists'] = render_to_string('parts/notification_setting.html', {
        'notification_setting_list': NotificationSetting.objects.filter(user=user),
    }, request=request)
    return JsonResponse(context)

def notification_confirmed(request):
    """notification_confirmed"""
    user = request.user
    notification_id = request.POST.get('notification_id')
    notification_obj = get_object_or_404(Notification, id=notification_id)
    notification_obj.confirmed.add(user)
    return JsonResponse()

def notification_deleted(request):
    """notification_deleted"""
    if request.method == 'POST':
        user = request.user
        notification_id = request.POST.get('notification_id')
        notification_obj = get_object_or_404(Notification, id=notification_id)
        notification_obj.confirmed.add(user)
        notification_obj.deleted.add(user)
        following_id_list = list(Follow.objects.filter(follower=user).values_list('following_id', flat=True))
        context = {
            'notification_count': Notification.objects.filter(user_from__in=following_id_list, user_to=user).exclude(confirmed=user).count(),
        }
        return JsonResponse(context)


# SearchTag
def searchtag_create(request):
    """searchtag_create"""
    if request.method == 'POST':
        form = SearchTagForm(request.POST)
        try:
            if form.is_valid():
                form = form.save(commit=False)
                form.author = request.user
                form.save()
                context = {'searchtag': form.name}
                return JsonResponse(context)
            else:
                form = SearchTagForm()
            logging.info({'info': str(e)})
        except Exception as e:
            return logging.error({'error': str(e)})


# advertise_read
def advertise_read(request):
    """advertise_read"""
    if request.method == 'POST':
        advertise_id = request.POST.get('advertise_id')
        advertise_obj = Advertise.objects.get(id=advertise_id)
        advertise_obj.read += 1
        advertise_obj.save(update_fields=['read'])
        context = {'read': advertise_obj.read}
        return JsonResponse(context)


# LikeForm
def like_form(request):
    """like_form"""
    if request.method == 'POST':
        user = request.user
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        obj = [get_object_or_404(models, id=obj_id) for detail, models in models_like_dict.items() if detail in obj_path][0]
        if obj.like.filter(id=user.id).exists():
            obj.like.remove(user)
        else:
            obj.like.add(user)
        context = {
            'liked': obj.like.filter(id=user.id).exists(),
            'total_like': obj.total_like(),
        }
        return JsonResponse(context)

def like_form_comment(request):
    """like_form_comment"""
    if request.method == 'POST':
        user = request.user
        comment_id = request.POST.get('comment_id')
        obj = get_object_or_404(Comment, id=comment_id)
        author = obj.author
        if obj.like.filter(id=user.id).exists():
            Notification.objects.filter(type_no=NotificationTypeNo.like, object_id=obj.id).delete()
            obj.like.remove(user)
        else:
            obj.like.add(user)
            if user != author and author.notificationsetting.is_like:
                Notification.objects.create(
                    user_from=user,
                    user_to=author,
                    type_no=NotificationTypeNo.like,
                    type_name='like',
                    content_object=obj,
                )
        context = {
            'comment_liked': obj.like.filter(id=user.id).exists(),
            'total_like': obj.total_like(),
        }
        return JsonResponse(context)


# CommentForm & ReplyForm
def comment_form(request):
    """comment_form"""
    context = {}
    if request.method == 'POST':
        user = request.user
        text = request.POST.get('text')
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        obj = [models.objects.get(id=obj_id) for detail, models in models_comment_dict.items() if detail in obj_path][0]
        comment_obj = Comment.objects.create(content_object=obj, text=text, author=user)
        obj.comment_num = obj.comment.all().count()
        obj.save(update_fields=['comment_num'])
        context['comment_num'] = obj.comment_num
        context['comment_lists'] = render_to_string('parts/common/comment/comment.html', {
            'comment_list': obj.comment.filter(id=comment_obj.id).select_related('author').prefetch_related('like'),
            'user_id': user.id,
            'obj_id': obj_id,
            'obj_path': obj_path,
        }, request=request)
        return JsonResponse(context)

def reply_form(request):
    """reply_form"""
    context = {}
    if request.method == 'POST':
        user = request.user
        text = request.POST.get('text')
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        comment_id = request.POST.get('comment_id')
        obj = [models.objects.get(id=obj_id) for detail, models in models_comment_dict.items() if detail in obj_path][0]
        comment_obj = Comment.objects.create(
            content_object=obj,
            text=text,
            author=user,
            parent=Comment.objects.get(id=comment_id),
        )
        obj.comment_num = obj.comment.all().count()
        obj.save(update_fields=['comment_num'])
        parent_obj = Comment.objects.get(id=comment_id)
        parent_obj.reply_num = Comment.objects.filter(parent=comment_id).count()
        parent_obj.save(update_fields=['reply_num'])
        author = comment_obj.parent.author
        if user != author and author.notificationsetting.is_reply:
            Notification.objects.create(
                user_from=user,
                user_to=author,
                type_no=NotificationTypeNo.reply,
                type_name='reply',
                content_object=comment_obj,
            )
        context['comment_num'] = obj.comment_num
        context['reply_num'] = parent_obj.reply_num
        context['reply_lists'] = render_to_string('parts/common/reply/reply.html', {
            'reply_list': obj.comment.filter(id=comment_obj.id).select_related('author', 'parent').prefetch_related('like'),
            'user_id': user.id,
            'obj_id': obj_id,
            'obj_path': obj_path,
            'comment_id': comment_id,
        }, request=request)
        return JsonResponse(context)

def comment_update(request, comment_id):
    """comment_update"""
    if request.method == 'POST':
        text = request.POST.get('text')
        comment_obj = Comment.objects.get(id=comment_id)
        comment_obj.text = text
        comment_obj.save(update_fields=['text', 'updated'])
        context = {'text': urlize_impl(linebreaksbr(comment_obj.text))}
        return JsonResponse(context)

def comment_delete(request, comment_id):
    """comment_delete"""
    if request.method == 'POST':
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        comment_id = request.POST.get('comment_id')
        obj = [models.objects.get(id=obj_id) for detail, models in models_comment_dict.items() if detail in obj_path][0]
        Comment.objects.get(id=comment_id).delete()
        obj.comment_num = obj.comment.all().count()
        obj.save(update_fields=['comment_num'])
        context = {'comment_num': obj.comment_num}
        return JsonResponse(context)

def reply_delete(request, comment_id):
    """reply_delete"""
    if request.method == 'POST':
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        comment_id = request.POST.get('comment_id')
        parent_id = request.POST.get('parent_id')
        Notification.objects.filter(type_no=NotificationTypeNo.reply, object_id=comment_id).delete()
        Comment.objects.get(id=comment_id).delete()
        parent_obj = Comment.objects.get(id=parent_id)
        parent_obj.reply_num = Comment.objects.filter(parent=parent_id).count()
        parent_obj.save(update_fields=['reply_num'])
        obj = [models.objects.get(id=obj_id) for detail, models in models_comment_dict.items() if detail in obj_path][0]
        obj.comment_num = obj.comment.all().count()
        obj.save(update_fields=['comment_num'])
        context = {
            'comment_num': obj.comment_num,
            'parent_id': parent_id,
            'reply_num': parent_obj.reply_num,
        }
        return JsonResponse(context)


# Index
class Index(ListView):
    """Index処理、すべてのメディアmodelを表示"""
    model = SearchTag
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, Index, **kwargs)

    def get_queryset(self):
        return Search.search_index(self)

class Recommend(ListView):
    """急上昇機能、すべてのメディアmodelを表示"""
    model = SearchTag
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
        return Search.search_advertise(self, Advertise)


# Follow
class FollowList(ListView):
    """FollowList"""
    model = Follow
    template_name = 'follow/follow.html'
    context_object_name = 'follow_list'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, FollowList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_follow(self, Follow)

class FollowerList(ListView):
    """FollowerList"""
    model = Follow
    template_name = 'follow/follower.html'
    context_object_name = 'follower_list'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, FollowerList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_follow(self, Follow)

def follow_create(request, nickname):
    """follow_create"""
    if request.method == 'POST':
        follower = MyPage.objects.get(user=request.user)
        following = MyPage.objects.get(user__nickname=nickname)
        follow_obj = Follow.objects.filter(follower=follower.user, following=following.user)
        follow_data = follow_update_data(follower, following, follow_obj)
        context = {
            'followed': follow_data['followed'],
            'follower_count': follow_data['follower_count'],
        }
        return JsonResponse(context)


# UserPolicy
class UserPolicy(TemplateView):
    """UserPolicy"""
    model = Notification
    template_name = 'common/userpolicy.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, UserPolicy, **kwargs)


# Knowledge
class Knowledge(TemplateView):
    """Knowledge"""
    model = Notification
    template_name = 'common/knowledge.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, Knowledge, **kwargs)


# Video
class VideoCreate(CreateView):
    """VideoCreate"""
    model = Video
    fields = ('title', 'content', 'image', 'convert')
    template_name = 'video/video_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()

        obj_id = f'object_{form.instance.id}'
        user_id = f'user_{form.instance.author.id}'
        media_root = settings.MEDIA_ROOT
        video_path = os.path.join(media_root, 'videos', 'videos_video', user_id, obj_id)
        video_file = os.path.join(video_path, os.path.basename(f'{form.instance.convert}'))

        file_path = convert_exe(video_file, video_path, media_root)
        form.instance.convert = file_path['mp4_path']
        form.instance.video = file_path['hls_path']
        return super(VideoCreate, self).form_valid(form)

    def get_success_url(self):
        return success_url(self, 'myus:video_detail', NotificationTypeNo.video, 'video')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, VideoCreate, **kwargs)

class VideoList(ListView):
    """VideoList"""
    model = Video
    template_name = 'video/video.html'
    context_object_name = 'video_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, VideoList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, Video)

class VideoDetail(DetailView):
    """VideoDetail"""
    model = Video
    template_name = 'video/video_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self, request)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, VideoDetail, **kwargs)


# Live
class LiveCreate(CreateView):
    """LiveCreate"""
    model = Live
    fields = ('title', 'content', 'image', 'convert')
    template_name = 'live/live_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(LiveCreate, self).form_valid(form)

    def get_success_url(self):
        return success_url(self, 'myus:live_detail', NotificationTypeNo.live, 'live')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, LiveCreate, **kwargs)

class LiveList(ListView):
    """LiveList"""
    model = Live
    template_name = 'live/live.html'
    context_object_name = 'live_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, LiveList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, Live)

class LiveDetail(DetailView):
    """LiveDetail"""
    model = Live
    template_name = 'live/live_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self, request)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, LiveDetail, **kwargs)


# Music
class MusicCreate(CreateView):
    """MusicCreate"""
    model = Music
    fields = ('title', 'content', 'lyric', 'music', 'download')
    template_name = 'music/music_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(MusicCreate, self).form_valid(form)

    def get_success_url(self):
        return success_url(self, 'myus:music_detail', NotificationTypeNo.music, 'music')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, MusicCreate, **kwargs)

class MusicList(ListView):
    """MusicList"""
    model = Music
    template_name = 'music/music.html'
    context_object_name = 'music_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, MusicList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, Music)

class MusicDetail(DetailView):
    """MusicDetail"""
    model = Music
    template_name = 'music/music_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self, request)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, MusicDetail, **kwargs)


# Picture
class PictureCreate(CreateView):
    """PictureCreate"""
    model = Picture
    fields = ('title', 'content', 'image')
    template_name = 'picture/picture_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PictureCreate, self).form_valid(form)

    def get_success_url(self):
        return success_url(self, 'myus:picture_detail', NotificationTypeNo.picture, 'picture')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, PictureCreate, **kwargs)

class PictureList(ListView):
    """PictureList"""
    model = Picture
    template_name = 'picture/picture.html'
    context_object_name = 'picture_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, PictureList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, Picture)

class PictureDetail(DetailView):
    """PictureDetail"""
    model = Picture
    template_name = 'picture/picture_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self, request)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, PictureDetail, **kwargs)


# Blog
class BlogCreate(CreateView):
    """BlogCreate"""
    model = Blog
    fields = ('title', 'content', 'image', 'richtext')
    template_name = 'blog/blog_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(BlogCreate, self).form_valid(form)

    def get_success_url(self):
        return success_url(self, 'myus:blog_detail', NotificationTypeNo.blog, 'blog')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, BlogCreate, **kwargs)

class BlogList(ListView):
    """BlogList"""
    model = Blog
    template_name = 'blog/blog.html'
    context_object_name = 'blog_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, BlogList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, Blog)

class BlogDetail(DetailView):
    """BlogDetail"""
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self, request)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, BlogDetail, **kwargs)


# Chat
class ChatCreate(CreateView):
    """ChatCreate"""
    model = Chat
    fields = ('title', 'content', 'period')
    template_name = 'chat/chat_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ChatCreate, self).form_valid(form)

    def get_success_url(self):
        return success_url(self, 'myus:chat_detail', NotificationTypeNo.chat, 'chat')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ChatCreate, **kwargs)

class ChatList(ListView):
    """ChatList"""
    model = Chat
    template_name = 'chat/chat.html'
    context_object_name = 'chat_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ChatList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, Chat)

class ChatDetail(DetailView):
    """ChatDetail"""
    model = Chat
    template_name = 'chat/chat_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self, request)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, ChatDetail, **kwargs)

    def get_message_data(self, comment_obj):
        obj = get_object_or_404(Chat, id=comment_obj.object_id)
        context = {
            'joined': obj.joined,
            'thread': obj.thread,
            'comment_obj': obj.comment.filter(id=comment_obj.id).select_related('author'),
        }
        return context

class ChatThread(DetailView):
    """ChatDetailThread"""
    model = Chat
    template_name = 'chat/chat_thread.html'

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, ChatThread, **kwargs)

    def get_reply_data(self, comment_obj):
        obj = get_object_or_404(Chat, id=comment_obj.object_id)
        context = {
            'joined': obj.joined,
            'reply_num': comment_obj.parent.reply_num,
            'reply_obj': obj.comment.filter(id=comment_obj.id).select_related('author'),
        }
        return context

def chat_thread_button(request):
    context = {}
    if request.method == 'GET':
        user = request.user
        obj_id = request.GET.get('obj_id')
        comment_id = request.GET.get('comment_id')
        obj = Chat.objects.get(id=obj_id)
        context['obj_id'] = obj_id
        context['comment_id'] = comment_id
        context['thread'] = render_to_string('chat/chat_reply/chat_section_thread_area.html', {
            'comment_parent': obj.comment.filter(id=comment_id),
            'reply_list': obj.comment.filter(parent_id=comment_id).select_related('author'),
            'user_id': user.id,
            'obj_id': obj_id,
            'comment_id': comment_id,
        }, request=request)
        return JsonResponse(context)


# Collabo
class CollaboCreate(CreateView):
    """CollaboCreate"""
    model = Collabo
    fields = ('title', 'content', 'period')
    template_name = 'collabo/collabo_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CollaboCreate, self).form_valid(form)

    def get_success_url(self):
        return success_url(self, 'myus:collabo_detail', NotificationTypeNo.collabo, 'collabo')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, CollaboCreate, **kwargs)

class CollaboList(ListView):
    """CollaboList"""
    model = Collabo
    template_name = 'collabo/collabo.html'
    context_object_name = 'collabo_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, CollaboList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, Collabo)

class CollaboDetail(DetailView):
    """CollaboDetail"""
    model = Collabo
    template_name = 'collabo/collabo_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self, request)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, CollaboDetail, **kwargs)


# Todo
class TodoCreate(CreateView):
    """TodoCreate"""
    model = Todo
    fields = ('title', 'content', 'priority', 'duedate')
    template_name = 'todo/todo_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(TodoCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('myus:todo_detail', kwargs={'pk': self.object.pk, 'title': self.object.title})

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, TodoCreate, **kwargs)

class TodoList(ListView):
    """TodoList"""
    model = Todo
    template_name = 'todo/todo.html'
    context_object_name = 'todo_list'
    ordering = ['-duedate']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, TodoList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_todo(self, Todo)

class TodoDetail(DetailView):
    """TodoDetail"""
    model = Todo
    template_name = 'todo/todo_detail.html'

    def get_queryset(self):
        user = self.request.user
        # スーパーユーザの場合、リストにすべてを表示する。
        if user.is_superuser:
            return Todo.objects.all()
        else:
            # 一般ユーザは自分のレコードのみ表示する。
            return Todo.objects.filter(author=user)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, TodoDetail, **kwargs)

class TodoUpdate(UpdateView):
    """TodoUpdate"""
    model = Todo
    fields = ('title', 'content', 'priority', 'progress', 'duedate')
    template_name = 'todo/todo_update.html'

    def get_success_url(self):
        return reverse('myus:todo_detail', kwargs={'pk': self.object.pk, 'title': self.object.title})

class TodoDelete(DeleteView):
    """TodoUpdate"""
    model = Todo
    template_name = 'todo/todo_delete.html'
    success_url = reverse_lazy('myus:todo_list')
