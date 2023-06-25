import datetime
import logging
import json
import os
import random
import string
import stripe

from django.db import IntegrityError
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import TimestampSigner,BadSignature, SignatureExpired, loads, dumps
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.template.defaultfilters import linebreaksbr
from django.urls import reverse, reverse_lazy
from django.utils.html import urlize as urlize_impl
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.myus.convert.convert_hls import convert_exe
from apps.myus.models import Profile, MyPage, SearchTag, NotificationSetting
from apps.myus.models import Notification, Follow, Comment, Advertise, ComicPage
from apps.myus.models import Video, Music, Comic, Picture, Blog, Chat, Todo
from apps.myus.modules.contains import NotificationTypeNo, model_like_dict, model_comment_dict
from apps.myus.modules.context_data import ContextData
from apps.myus.modules.get_form import get_detail
from apps.myus.modules.pjax import pjax_context
from apps.myus.modules.notification import notification_data, notification_setting_update
from apps.myus.modules.search import Search
from apps.myus.modules.success_url import success_url
from apps.myus.modules.follow import follow_update_data
from apps.myus.modules.validation import has_username, has_email, has_phone, has_postal_code, has_alphabet, has_number


logger = logging.getLogger(__name__)
User = get_user_model()


# Signup
def signup_form(request):
    """サインアップ処理"""
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        nickname = request.POST['nickname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        gender = request.POST['gender']
        year = request.POST['year']
        month = request.POST['month']
        day = request.POST['day']

        if has_email(email):
            messages.error(request, 'メールアドレスの形式が違います!')
            return render(request, 'registration/signup.html')
        if has_username(username):
            messages.error(request, 'ユーザー名は半角英数字になります!')
            return render(request, 'registration/signup.html')
        if password1 != password2:
            messages.error(request, 'パスワードが一致していません!')
            return render(request, 'registration/signup.html')
        if not has_number(password1) and not has_alphabet(password1):
            messages.error(request, 'パスワードは半角8文字以上で英数字を含む必要があります!')
            return render(request, 'registration/signup.html')
        if has_number(last_name):
            messages.error(request, '姓に数字が含まれています!')
            return render(request, 'registration/signup.html')
        if has_number(first_name):
            messages.error(request, '名に数字が含まれています!')
            return render(request, 'registration/signup.html')
        if not has_number(year):
            messages.error(request, '生年月日の年を入力してください!')
            return render(request, 'registration/signup.html')
        if not has_number(month):
            messages.error(request, '生年月日の月を入力してください!')
            return render(request, 'registration/signup.html')
        if not has_number(day):
            messages.error(request, '生年月日の日を入力してください!')
            return render(request, 'registration/signup.html')
        if year and month and day:
            try:
                birthday = datetime.date(year=int(year), month=int(month), day=int(day)).isoformat()
            except ValueError:
                messages.error(request, f'{year}年{month}月{day}日は存在しない日付です!')
                return render(request, 'registration/signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'メールアドレスは既に登録されています!')
            return render(request, 'registration/signup.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'ユーザー名は既に登録されています!')
            return render(request, 'registration/signup.html')
        if User.objects.filter(nickname=nickname).exists():
            messages.error(request, '投稿者名は既に登録されています!')
            return render(request, 'registration/signup.html')

        try:
            user = User.objects.create_user(email, username, nickname, password1)
            profile = Profile.objects.get(user=user)
            profile.last_name = last_name
            profile.first_name = first_name
            profile.gender = gender
            profile.birthday = birthday
            profile.save()

            current_site = get_current_site(request)
            context = {
                'protocol': request.scheme,
                'domain': current_site.domain,
                'token': dumps(user.pk),
                'user': user
            }
            subject = render_to_string('registration/email/account/subject.txt', context)
            message = render_to_string('registration/email/account/message.txt', context)
            user.email_user(subject, message)
            messages.success(request, '本アカウント登録用のメールを送信しました!')
            return redirect('myus:login')
        except Exception:
            messages.error(request, 'アカウント登録に失敗しました!')
            logger.exception('アカウント登録に失敗しました!')
            return render(request, 'registration/signup.html')
    return render(request, 'registration/signup.html')


class SignupComplete(TemplateView):
    """SignupComplete"""
    template_name = 'registration/signup_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            user_id = loads(token, max_age=self.timeout_seconds)
            user = User.objects.filter(id=user_id).first()
            if user.is_active:
                messages.success(request, '既に本アカウント登録が完了しています!')
                return redirect('myus:login')

        except SignatureExpired:
            messages.error(request, '本登録の期限が切れております!')
            logger.exception('SignatureExpired Exception')
            return redirect('myus:login')
        except BadSignature:
            messages.error(request, '登録用のURLが間違っています!')
            logger.exception('BadSignature Exception')
            return redirect('myus:login')

        user.is_active = True
        user.save()
        return super().get(request, **kwargs)


class PasswordReset(PasswordResetView):
    """PasswordReset"""
    subject_template_name = 'registration/email/reset/subject.txt'
    email_template_name = 'registration/email/reset/message.txt'
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('myus:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """PasswordResetDone"""
    template_name = 'registration/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """PasswordResetConfirm"""
    success_url = reverse_lazy('myus:password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """PasswordResetComplete"""
    template_name = 'registration/password_reset_complete.html'


# Login
def login_form(request):
    """ログイン処理"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect('myus:index')
        else:
            messages.error(request, 'ID又はパスワードが違います!')
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
    template_name = 'setting/withdrawal.html'
    timestamp_signer = TimestampSigner()
    EXPIRED_SECONDS = 60

    def get_random_chars(self, char_num=30):
        return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(char_num)])

    def get(self, request, token=None):
        context = {}
        user = request.user
        if user.id:
            notification = notification_data(user)
            context = {
                'expired_seconds': self.EXPIRED_SECONDS,
                'notification_list': notification['notification_list'],
                'notification_count': notification['notification_count'],
            }
        if token:
            try:
                self.timestamp_signer.unsign(token, max_age=datetime.timedelta(seconds=self.EXPIRED_SECONDS))
                context['message'] = '有効なURLです'
                return render(request, 'setting/withdrawal_confirm.html', context)
            except SignatureExpired:
                context['message'] = 'URLは期限切れです'
            except BadSignature:
                context['message'] = 'URLは正しくありません'
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        if self.request.method == 'POST':
            password = self.request.POST.get('password')
            password2 = self.request.POST.get('password2')
            if check_password(password, user.password):
                token = self.get_random_chars()
                notification = notification_data(user)
                context = {
                    'token_signed': self.timestamp_signer.sign(token),
                    'expired_seconds': self.EXPIRED_SECONDS,
                    'notification_list': notification['notification_list'],
                    'notification_count': notification['notification_count'],
                }
                return render(request, self.template_name, context)
            elif check_password(password2, user.password):
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
    template_name = 'setting/profile.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ProfileView, **kwargs)


class ProfileUpdate(UpdateView):
    """アカウント更新"""
    model = Profile
    fields = ('last_name', 'first_name', 'gender', 'phone', 'postal_code', 'prefecture', 'city', 'address', 'building', 'introduction')
    template_name = 'setting/profile_update.html'
    success_url = reverse_lazy('myus:profile')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ProfileUpdate, **kwargs)

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        """バリデーションに成功した時"""
        try:
            data = self.request.POST
            file = self.request.FILES
            user = self.request.user
            user.email = data['email']
            user.username = data['username']
            user.nickname = data['nickname']

            if file:
                user.avatar = file['avatar']

            if has_email(user.email):
                messages.error(self.request, 'メールアドレスの形式が違います!')
                return super().form_invalid(form)

            if has_username(user.username):
                messages.error(self.request, 'ユーザー名は半角英数字のみ入力できます!')
                return super().form_invalid(form)

            if has_number(data['last_name']):
                messages.error(self.request, '姓に数字が含まれております!')
                return super().form_invalid(form)

            if has_number(data['first_name']):
                messages.error(self.request, '名に数字が含まれております!')
                return super().form_invalid(form)

            if has_phone(data['phone']):
                messages.error(self.request, '電話番号の形式が違います!')
                return super().form_invalid(form)

            if has_postal_code(data['postal_code']):
                messages.error(self.request, '郵便番号の形式が違います!')
                return super().form_invalid(form)

            profile_obj = form.save(commit=False)
            year = data['year']
            month = data['month']
            day = data['day']
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
    """マイページ遷移"""
    model = MyPage
    template_name = 'setting/mypage.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, MyPageView, **kwargs)


class MyPageUpdate(UpdateView):
    """マイページ更新"""
    model = MyPage
    fields = ('banner', 'email', 'content', 'tag_manager_id')
    template_name = 'setting/mypage_update.html'
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
    if request.method == 'POST':
        user = request.user
        is_advertise = request.POST.get('is_advertise')
        myapge = MyPage.objects.get(user=user)
        myapge.is_advertise = True if is_advertise == 'False' else False
        myapge.save(update_fields=['is_advertise'])
        context = {
            'toggle_mypage': render_to_string('setting/mypage_advertise.html', {
                'mypage_list': MyPage.objects.filter(user=user),
            }, request=request)
        }
        return JsonResponse(context)


# 決済システム
class Payment(TemplateView):
    model = User
    template_name = 'setting/payment/payment.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, Payment, **kwargs)


class ChangePlan(TemplateView):
    model = User
    template_name = 'setting/payment/change_plan.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ChangePlan, **kwargs)

class PaymentSuccess(TemplateView):
    template_name = 'setting/payment/success.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, PaymentSuccess, **kwargs)

class PaymentCancel(TemplateView):
    template_name = 'setting/payment/cancel.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, PaymentCancel, **kwargs)

def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
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
        return JsonResponse({'error': str(e)})


def get_subscription(stripe_customer_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    customer = stripe.Customer.retrieve(stripe_customer_id)
    subscription = customer.subscriptions.data[0]
    return subscription.id


# 通知設定
class NotificationSettingView(TemplateView):
    """NotificationSettingView"""
    model = NotificationSetting
    template_name = 'setting/notification.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, NotificationSettingView, **kwargs)


def notification_update(request):
    """notification_update"""
    if request.method == 'POST':
        user = request.user
        is_notification = request.POST['notification']
        notification_type = request.POST['notification_type']
        notification_setting = NotificationSetting.objects.get(user=user)
        notification_setting_update(is_notification, notification_type, notification_setting)
    context = {
        'notification_setting_html': render_to_string('parts/notification_setting.html', {
            'notification_setting': NotificationSetting.objects.filter(user=user).first(),
        }, request=request)
    }
    return JsonResponse(context)


def notification_confirmed(request):
    """notification_confirmed"""
    user = request.user
    notification_id = request.POST.get('notification_id')
    notification = Notification.objects.filter(id=notification_id).first()
    if not notification:
        return JsonResponse()

    notification.confirmed.add(user)
    return JsonResponse()


def notification_deleted(request):
    """notification_deleted"""
    if request.method == 'POST':
        user = request.user
        notification_id = request.POST.get('notification_id')
        notification = Notification.objects.filter(id=notification_id).first()
        if not notification:
            return JsonResponse({})

        notification.confirmed.add(user)
        notification.deleted.add(user)
        following_id_list = list(Follow.objects.filter(follower=user).values_list('following_id', flat=True))
        context = {
            'notification_count': Notification.objects.filter(user_from__in=following_id_list, user_to=user).exclude(confirmed=user).count()
        }
        return JsonResponse(context)


# SearchTag
def searchtag_create(request):
    """searchtag_create"""
    if request.method == 'POST':
        author = request.user
        name = request.POST['name']
        searchtag = SearchTag.objects.filter(author=author, name=name)
        if not searchtag:
            searchtag = SearchTag.objects.create(author=author, name=name)
            return JsonResponse({'searchtag': searchtag.name})


# advertise_read
def advertise_read(request):
    """advertise_read"""
    if request.method == 'POST':
        advertise_id = request.POST.get('advertise_id')
        advertise = Advertise.objects.get(id=advertise_id)
        advertise.read += 1
        advertise.save(update_fields=['read'])
        context = {'read': advertise.read}
        return JsonResponse(context)


# LikeForm
def like_form(request):
    """like_form"""
    if request.method == 'POST':
        user = request.user
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        obj = [models.objects.get(id=obj_id) for detail, models in model_like_dict.items() if detail in obj_path][0]
        is_like = obj.like.filter(id=user.id).exists()
        obj.like.remove(user) if is_like else obj.like.add(user)
        context = {'is_like': obj.like.filter(id=user.id).exists(), 'total_like': obj.total_like()}
        return JsonResponse(context)


def like_form_comment(request):
    """like_form_comment"""
    if request.method == 'POST':
        user = request.user
        comment_id = request.POST['comment_id']
        comment = Comment.objects.get(id=comment_id)
        author = comment.author
        is_comment_like = comment.like.filter(id=user.id).exists()
        if is_comment_like:
            Notification.objects.filter(type_no=NotificationTypeNo.like, object_id=comment.id).delete()
            comment.like.remove(user)
        else:
            comment.like.add(user)
            if user != author and author.notificationsetting.is_like:
                Notification.objects.create(
                    user_from=user,
                    user_to=author,
                    type_no=NotificationTypeNo.like,
                    type_name='like',
                    content_object=comment,
                )
        context = {
            'is_comment_like': comment.like.filter(id=user.id).exists(),
            'total_like': comment.total_like()
        }
        return JsonResponse(context)


# CommentForm & ReplyForm
def comment_form(request):
    """comment_form"""
    if request.method == 'POST':
        user = request.user
        text = request.POST.get('text')
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        obj = [models.objects.get(id=obj_id) for detail, models in model_comment_dict.items() if detail in obj_path][0]
        comment = Comment.objects.create(content_object=obj, text=text, author=user)
        obj = [models.objects.get(id=obj_id) for detail, models in model_comment_dict.items() if detail in obj_path][0]
        context = {
            'comment_count': obj.comment_count(),
            'comment_lists': render_to_string('parts/common/comment/comment.html', {
                'comment_list': obj.comment.filter(id=comment.id),
                'user_id': user.id,
                'obj_id': obj_id,
                'obj_path': obj_path,
            }, request=request)
        }
        return JsonResponse(context)


def reply_form(request):
    """reply_form"""
    if request.method == 'POST':
        user = request.user
        text = request.POST.get('text')
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        comment_id = request.POST.get('comment_id')
        obj = [models.objects.get(id=obj_id) for detail, models in model_comment_dict.items() if detail in obj_path][0]
        comment = Comment.objects.create(
            content_object=obj,
            text=text,
            author=user,
            parent=Comment.objects.get(id=comment_id),
        )
        author = comment.parent.author
        if user != author and author.notificationsetting.is_reply:
            Notification.objects.create(
                user_from=user,
                user_to=author,
                type_no=NotificationTypeNo.reply,
                type_name='reply',
                content_object=comment,
            )
        context = {
            'comment_count': obj.comment_count() + 1,
            'reply_count': Comment.objects.filter(parent=comment_id).count(),
            'reply_lists': render_to_string('parts/common/reply/reply.html', {
                'reply_list': obj.comment.filter(id=comment.id),
                'user_id': user.id,
                'obj_id': obj_id,
                'obj_path': obj_path,
                'comment_id': comment_id,
            }, request=request)
        }
        return JsonResponse(context)


def comment_update(request, comment_id):
    """comment_update"""
    if request.method == 'POST':
        text = request.POST.get('text')
        comment = Comment.objects.get(id=comment_id)
        comment.text = text
        comment.save(update_fields=['text', 'updated'])
        context = {'text': urlize_impl(linebreaksbr(comment.text))}
        return JsonResponse(context)


def comment_delete(request, comment_id):
    """comment_delete"""
    if request.method == 'POST':
        obj_id = request.POST.get('id')
        obj_path = request.POST.get('path')
        comment_id = request.POST.get('comment_id')
        Comment.objects.get(id=comment_id).delete()
        obj = [models.objects.get(id=obj_id) for detail, models in model_comment_dict.items() if detail in obj_path][0]
        context = {'comment_count': obj.comment_count()}
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
        obj = [models.objects.get(id=obj_id) for detail, models in model_comment_dict.items() if detail in obj_path][0]
        context = {
            'parent_id': parent_id,
            'comment_count': obj.comment_count(),
            'reply_count': Comment.objects.filter(parent=parent_id).count(),
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
    template_name = 'menu/follow/follow.html'
    context_object_name = 'follow_list'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, FollowList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_follow(self, Follow)


class FollowerList(ListView):
    """FollowerList"""
    model = Follow
    template_name = 'menu/follow/follower.html'
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
        follow = Follow.objects.filter(follower=follower.user, following=following.user).first()
        follow_data = follow_update_data(follower, following, follow)
        context = {
            'is_follow': follow_data['is_follow'],
            'follower_count': follow_data['follower_count'],
        }
        return JsonResponse(context)


# UserPolicy
class UserPolicy(TemplateView):
    """UserPolicy"""
    model = Notification
    template_name = 'menu/userpolicy.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, UserPolicy, **kwargs)


# Knowledge
class Knowledge(TemplateView):
    """Knowledge"""
    model = Notification
    template_name = 'menu/knowledge.html'

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, Knowledge, **kwargs)


# Video
class VideoCreate(CreateView):
    """VideoCreate"""
    model = Video
    fields = ('title', 'content', 'image', 'convert')
    template_name = 'media/video/video_create.html'

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
    template_name = 'media/video/video.html'
    context_object_name = 'video_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, VideoList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, Video)


class VideoDetail(DetailView):
    """VideoDetail"""
    model = Video
    template_name = 'media/video/video_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self, request)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, VideoDetail, **kwargs)


# Music
class MusicCreate(CreateView):
    """MusicCreate"""
    model = Music
    fields = ('title', 'content', 'lyric', 'music', 'download')
    template_name = 'media/music/music_create.html'

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
    template_name = 'media/music/music.html'
    context_object_name = 'music_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, MusicList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, Music)


class MusicDetail(DetailView):
    """MusicDetail"""
    model = Music
    template_name = 'media/music/music_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self, request)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, MusicDetail, **kwargs)


# Comic
class ComicCreate(CreateView):
    """ComicCreate"""
    model = Comic
    fields = ('title', 'content', 'image')
    template_name = 'media/comic/comic_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        comic_images = self.request.FILES.getlist('comic_image')
        self.object = form.save()

        for sequence, image in enumerate(comic_images):
            ComicPage.objects.create(comic=self.object, image=image, sequence=sequence)
        return super(ComicCreate, self).form_valid(form)

    def get_success_url(self):
        return success_url(self, 'myus:comic_detail', NotificationTypeNo.comic, 'comic')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ComicCreate, **kwargs)


class ComicList(ListView):
    """ComicList"""
    model = Comic
    template_name = 'media/comic/comic.html'
    context_object_name = 'comic_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ComicList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, Comic)


class ComicDetail(DetailView):
    """ComicDetail"""
    model = Comic
    template_name = 'media/comic/comic_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self, request)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, ComicDetail, **kwargs)


# Picture
class PictureCreate(CreateView):
    """PictureCreate"""
    model = Picture
    fields = ('title', 'content', 'image')
    template_name = 'media/picture/picture_create.html'

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
    template_name = 'media/picture/picture.html'
    context_object_name = 'picture_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, PictureList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, Picture)


class PictureDetail(DetailView):
    """PictureDetail"""
    model = Picture
    template_name = 'media/picture/picture_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self, request)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, PictureDetail, **kwargs)


# Blog
def get_delta(delta, html):
    quill = json.dumps({'delta': delta, 'html': html})
    return quill

class BlogCreate(CreateView):
    """BlogCreate"""
    model = Blog
    fields = ('title', 'content', 'image', 'richtext')
    template_name = 'media/blog/blog_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        delta = self.request.POST['delta']
        html = self.request.POST['richtext']
        form.instance.delta = get_delta(delta, html)
        return super(BlogCreate, self).form_valid(form)

    def get_success_url(self):
        return success_url(self, 'myus:blog_detail', NotificationTypeNo.blog, 'blog')

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, BlogCreate, **kwargs)


class BlogList(ListView):
    """BlogList"""
    model = Blog
    template_name = 'media/blog/blog.html'
    context_object_name = 'blog_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, BlogList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, Blog)


class BlogDetail(DetailView):
    """BlogDetail"""
    model = Blog
    template_name = 'media/blog/blog_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self, request)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, BlogDetail, **kwargs)


# Chat
class ChatCreate(CreateView):
    """ChatCreate"""
    model = Chat
    fields = ('title', 'content', 'period')
    template_name = 'media/chat/chat_create.html'

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
    template_name = 'media/chat/chat.html'
    context_object_name = 'chat_list'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, ChatList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_models(self, Chat)


class ChatDetail(DetailView):
    """ChatDetail"""
    model = Chat
    template_name = 'media/chat/chat_detail.html'

    def get(self, request, *args, **kwargs):
        return get_detail(self, request)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, ChatDetail, **kwargs)


class ChatThread(DetailView):
    """ChatDetailThread"""
    model = Chat
    template_name = 'media/chat/chat_thread.html'

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, ChatThread, **kwargs)


def chat_thread_button(request):
    if request.method == 'GET':
        user = request.user
        chat_id = request.GET.get('chat_id')
        message_id = request.GET.get('message_id')
        chat = Chat.objects.get(id=chat_id)
        context = {
            'obj_id': chat_id,
            'message_id': message_id,
            'thread': render_to_string('media/chat/chat_reply/chat_section_thread_area.html', {
                'message_parent': chat.message.filter(id=message_id),
                'reply_list': chat.message.filter(parent_id=message_id).select_related('author'),
                'user_id': user.id,
                'obj_id': chat_id,
                'message_id': message_id,
            }, request=request)
        }
        return JsonResponse(context)


# Todo
class TodoCreate(CreateView):
    """TodoCreate"""
    model = Todo
    fields = ('title', 'content', 'priority', 'duedate')
    template_name = 'media/todo/todo_create.html'

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
    template_name = 'media/todo/todo.html'
    context_object_name = 'todo_list'
    ordering = ['-duedate']

    def get_context_data(self, **kwargs):
        return ContextData.context_data(self, TodoList, **kwargs)

    def get_queryset(self, **kwargs):
        return Search.search_todo(self, Todo)


class TodoDetail(DetailView):
    """TodoDetail"""
    model = Todo
    template_name = 'media/todo/todo_detail.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Todo.objects.all()
        else:
            return Todo.objects.filter(author=user)

    def get_context_data(self, **kwargs):
        return ContextData.models_context_data(self, TodoDetail, **kwargs)


class TodoUpdate(UpdateView):
    """TodoUpdate"""
    model = Todo
    fields = ('title', 'content', 'priority', 'progress', 'duedate')
    template_name = 'media/todo/todo_update.html'

    def get_success_url(self):
        return reverse('myus:todo_detail', kwargs={'pk': self.object.pk, 'title': self.object.title})


class TodoDelete(DeleteView):
    """TodoUpdate"""
    model = Todo
    template_name = 'media/todo/todo_delete.html'
    success_url = reverse_lazy('myus:todo_list')
