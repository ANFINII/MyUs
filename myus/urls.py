from django.urls import path
from .views import Index, Recommend, UserPage, UserPageInfo, UserPageAdvertise
from .views import Profile, ProfileUpdate, MyPage, MyPageUpdate
from .views import Payment, PaymentCheckout, PaymentSuccess, PaymentCancel, create_checkout_session
from .views import Notification, notification_setting, notification_confirmed, notification_deleted
from .views import UserPolicy, Knowledge, FollowerList, FollowList, follow_create
from .views import VideoList, VideoCreate, VideoDetail
from .views import LiveList, LiveCreate, LiveDetail
from .views import MusicList, MusicCreate, MusicDetail
from .views import PictureList, PictureCreate, PictureDetail
from .views import BlogList, BlogCreate, BlogDetail
from .views import ChatList, ChatCreate, ChatDetail, ChatThread
from .views import CollaboList, CollaboCreate, CollaboDetail
from .views import TodoList, TodoDetail, TodoCreate, TodoDelete, TodoUpdate
from .views import searchtag_create, advertise_read, like_form, like_form_comment
from .views import comment_form, reply_form, comment_update, comment_delete, reply_delete
from .views import signup_form, login_form, logout_form, Withdrawal

app_name = 'myus'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('recommend', Recommend.as_view(), name='recommend'),
    path('userpage/<str:nickname>', UserPage.as_view(), name='userpage'),
    path('userpage/information/<str:nickname>', UserPageInfo.as_view(), name='userpage_info'),
    path('userpage/advertise/<str:nickname>', UserPageAdvertise.as_view(), name='userpage_advertise'),

    path('profile', Profile.as_view(), name='profile'),
    path('profile/update', ProfileUpdate.as_view(), name='profile_update'),
    path('mypage', MyPage.as_view(), name='mypage'),
    path('mypage/update', MyPageUpdate.as_view(), name='mypage_update'),

    path('payment', Payment.as_view(), name='payment'),
    path('payment/checkout', PaymentCheckout.as_view(), name='payment_checkout'),
    path('payment/success', PaymentSuccess.as_view(), name='payment_success'),
    path('payment/cancel', PaymentCancel.as_view(), name='payment_cancel'),
    path('create_checkout_session', create_checkout_session, name='create_checkout_session'),

    path('notification', Notification.as_view(), name='notification'),
    path('notification/setting', notification_setting, name='notification_setting'),
    path('notification/confirmed', notification_confirmed, name='notification_confirmed'),
    path('notification/deleted', notification_deleted, name='notification_deleted'),

    path('userpolicy', UserPolicy.as_view(), name='userpolicy'),
    path('knowledge', Knowledge.as_view(), name='knowledge'),
    path('follower', FollowerList.as_view(), name='follower_list'),
    path('follow', FollowList.as_view(), name='follow_list'),
    path('follow/create/<str:nickname>', follow_create, name='follow_create'),

    path('video', VideoList.as_view(), name='video_list'),
    path('video/create', VideoCreate.as_view(), name='video_create'),
    path('video/detail/<int:pk>/<str:title>', VideoDetail.as_view(), name='video_detail'),

    path('live', LiveList.as_view(), name='live_list'),
    path('live/create', LiveCreate.as_view(), name='live_create'),
    path('live/detail/<int:pk>/<str:title>', LiveDetail.as_view(), name='live_detail'),

    path('music', MusicList.as_view(), name='music_list'),
    path('music/create', MusicCreate.as_view(), name='music_create'),
    path('music/detail/<int:pk>/<str:title>', MusicDetail.as_view(), name='music_detail'),

    path('picture', PictureList.as_view(), name='picture_list'),
    path('picture/create', PictureCreate.as_view(), name='picture_create'),
    path('picture/detail/<int:pk>/<str:title>', PictureDetail.as_view(), name='picture_detail'),

    path('blog', BlogList.as_view(), name='blog_list'),
    path('blog/create', BlogCreate.as_view(), name='blog_create'),
    path('blog/detail/<int:pk>/<str:title>', BlogDetail.as_view(), name='blog_detail'),

    path('chat', ChatList.as_view(), name='chat_list'),
    path('chat/create', ChatCreate.as_view(), name='chat_create'),
    path('chat/detail/<int:pk>', ChatDetail.as_view(), name='chat_detail'),
    path('chat/detail/<int:pk>/thread/<int:comment_id>', ChatThread.as_view(), name='chat_thread'),

    path('collabo', CollaboList.as_view(), name='collabo_list'),
    path('collabo/create', CollaboCreate.as_view(), name='collabo_create'),
    path('collabo/detail/<int:pk>/<str:title>', CollaboDetail.as_view(), name='collabo_detail'),

    path('todo', TodoList.as_view(), name='todo_list'),
    path('todo/create', TodoCreate.as_view(), name='todo_create'),
    path('todo/detail/<int:pk>/<str:title>', TodoDetail.as_view(), name='todo_detail'),
    path('todo/update/<int:pk>/<str:title>', TodoUpdate.as_view(), name='todo_update'),
    path('todo/delete/<int:pk>/<str:title>', TodoDelete.as_view(), name='todo_delete'),

    path('searchtag/create', searchtag_create, name='searchtag_create'),
    path('url/read', advertise_read, name='advertise_read'),
    path('like/form', like_form, name='like_form'),
    path('like/form/comment', like_form_comment, name='like_form_comment'),

    path('comment/form', comment_form, name='comment_form'),
    path('reply/form', reply_form, name='reply_form'),
    path('comment/update/<int:comment_id>', comment_update, name='comment_update'),
    path('comment/delete/<int:comment_id>', comment_delete, name='comment_delete'),
    path('reply/delete/<int:comment_id>', reply_delete, name='reply_delete'),

    path('signup', signup_form, name='signup'),
    path('login', login_form, name='login'),
    path('logout', logout_form, name='logout'),
    path('withdrawal', Withdrawal.as_view(), name='withdrawal'),
    path('withdrawal/<str:token>', Withdrawal.as_view(), name='withdrawal'),
]
