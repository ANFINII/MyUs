from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import Index, Recommend, UserPage
from .views import profile, ProfileUpdate, mypage, MyPageUpdate
from .views import FollowerList, FollowList, follow_create, userpolicy, knowledge
from .views import VideoList, VideoCreate, VideoDetail
from .views import LiveList, LiveCreate, LiveDetail
from .views import MusicList, MusicCreate, MusicDetail
from .views import PictureList, PictureCreate, PictureDetail
from .views import BlogList, BlogCreate, BlogDetail
from .views import ChatList, ChatCreate, ChatDetail, ChatThread, chat_message, chat_reply
from .views import CollaboList, CollaboCreate, CollaboDetail
from .views import TodoList, TodoDetail, TodoCreate, TodoDelete, TodoUpdate
from .views import searchtag_create, like_form, comment_form, reply_form
from .views import signup_form, login_form, logout_form, Withdrawal

app_name = 'myus'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('recommend/', Recommend.as_view(), name='recommend'),
    path('userpage/<str:nickname>', UserPage.as_view(), name='userpage'),

    path('profile/', profile, name='profile'),
    path('profile/update/', ProfileUpdate.as_view(), name='profile_update'),
    path('mypage/', mypage, name='mypage'),
    path('mypage/update/', MyPageUpdate.as_view(), name='mypage_update'),

    path('follower/', FollowerList.as_view(), name='follower_list'),
    path('follow/', FollowList.as_view(), name='follow_list'),
    path('follow/create/<str:nickname>', follow_create, name='follow_create'),
    path('userpolicy/', userpolicy, name='userpolicy'),
    path('knowledge/', knowledge, name='knowledge'),

    path('video/', VideoList.as_view(), name='video_list'),
    path('video/create/', VideoCreate.as_view(), name='video_create'),
    path('video/detail/<int:pk>', VideoDetail.as_view(), name='video_detail'),

    path('live/', LiveList.as_view(), name='live_list'),
    path('live/create/', LiveCreate.as_view(), name='live_create'),
    path('live/detail/<int:pk>', LiveDetail.as_view(), name='live_detail'),

    path('music/', MusicList.as_view(), name='music_list'),
    path('music/create/', MusicCreate.as_view(), name='music_create'),
    path('music/detail/<int:pk>', MusicDetail.as_view(), name='music_detail'),

    path('picture/', PictureList.as_view(), name='picture_list'),
    path('picture/create/', PictureCreate.as_view(), name='picture_create'),
    path('picture/detail/<int:pk>', PictureDetail.as_view(), name='picture_detail'),

    path('blog/', BlogList.as_view(), name='blog_list'),
    path('blog/create/', BlogCreate.as_view(), name='blog_create'),
    path('blog/detail/<int:pk>', BlogDetail.as_view(), name='blog_detail'),

    path('chat/', ChatList.as_view(), name='chat_list'),
    path('chat/create/', ChatCreate.as_view(), name='chat_create'),
    path('chat/detail/<int:pk>', ChatDetail.as_view(), name='chat_detail'),
    path('chat/detail/<int:pk>/thread/<int:comment_id>', ChatThread.as_view(), name='chat_thread'),
    path('chat/detail/message', chat_message, name='chat_message'),
    path('chat/detail/reply', chat_reply, name='chat_reply'),

    path('collabo/', CollaboList.as_view(), name='collabo_list'),
    path('collabo/create/', CollaboCreate.as_view(), name='collabo_create'),
    path('collabo/detail/<int:pk>', CollaboDetail.as_view(), name='collabo_detail'),

    path('todo/', TodoList.as_view(), name='todo_list'),
    path('todo/create/', TodoCreate.as_view(), name='todo_create'),
    path('todo/detail/<int:pk>', TodoDetail.as_view(), name='todo_detail'),
    path('todo/update/<int:pk>', TodoUpdate.as_view(), name='todo_update'),
    path('todo/delete/<int:pk>', TodoDelete.as_view(), name='todo_delete'),

    path('searchtag/create/', searchtag_create, name='searchtag_create'),
    path('like/form/', like_form, name='like_form'),
    path('comment/form/', comment_form, name='comment_form'),
    path('reply/form/', reply_form, name='reply_form'),

    path('signup/', signup_form, name='signup'),
    path('login/', login_form, name='login'),
    path('logout/', logout_form, name='logout'),
    path('withdrawal/', Withdrawal.as_view(), name='withdrawal'),
    path('withdrawal/<str:token>', Withdrawal.as_view(), name='withdrawal'),
]
