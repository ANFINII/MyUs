from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import Index, Recommend, UserPage
from .views import profile, ProfileUpdate, mypage, MyPageUpdate
from .views import FollowList, FollowerList, follow_create, userpolicy, knowledge
from .views import VideoList, VideoCreate, VideoDetail
from .views import LiveList, LiveCreate, LiveDetail
from .views import MusicList, MusicCreate, MusicDetail
from .views import PictureList, PictureCreate, PictureDetail
from .views import BlogList, BlogCreate, BlogDetail
from .views import ChatList, ChatCreate, ChatDetail, chat_message, chat_reply
from .views import CollaboList, CollaboCreate, CollaboDetail
from .views import TodoList, TodoDetail, TodoCreate, TodoDelete, TodoUpdate
from .views import searchtag_create, like_form, comment_form, reply_form, CommentView
from .views import signup_form, login_form, logout_form, Withdrawal

app_name = 'myus'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('recommend/', Recommend.as_view(), name='recommend'),
    path('userpage/<str:nickname>', UserPage.as_view(), name='userpage'),
    
    path('profile/', profile, name='profile'),
    path('profile_update/', ProfileUpdate.as_view(), name='profile_update'),
    path('mypage/', mypage, name='mypage'),
    path('mypage_update/', MyPageUpdate.as_view(), name='mypage_update'),
    
    path('follow/', FollowList.as_view(), name='follow_list'),
    path('follower/', FollowerList.as_view(), name='follower_list'),
    path('follow_create/<str:nickname>', follow_create, name='follow_create'),
    path('userpolicy/', userpolicy, name='userpolicy'),
    path('knowledge/', knowledge, name='knowledge'),
    
    path('video/', VideoList.as_view(), name='video_list'),
    path('video_create/', VideoCreate.as_view(), name='video_create'),
    path('video_detail/<int:pk>', VideoDetail.as_view(), name='video_detail'),
    
    path('live/', LiveList.as_view(), name='live_list'),
    path('live_create/', LiveCreate.as_view(), name='live_create'),
    path('live_detail/<int:pk>', LiveDetail.as_view(), name='live_detail'),
    
    path('music/', MusicList.as_view(), name='music_list'),
    path('music_create/', MusicCreate.as_view(), name='music_create'),
    path('music_detail/<int:pk>', MusicDetail.as_view(), name='music_detail'),
    
    path('picture/', PictureList.as_view(), name='picture_list'),
    path('picture_create/', PictureCreate.as_view(), name='picture_create'),
    path('picture_detail/<int:pk>', PictureDetail.as_view(), name='picture_detail'),
    
    path('blog/', BlogList.as_view(), name='blog_list'),
    path('blog_create/', BlogCreate.as_view(), name='blog_create'),
    path('blog_detail/<int:pk>', BlogDetail.as_view(), name='blog_detail'),
    
    path('chat/', ChatList.as_view(), name='chat_list'),
    path('chat_create/', ChatCreate.as_view(), name='chat_create'),
    path('chat_detail/<int:pk>', ChatDetail.as_view(), name='chat_detail'),
    path('chat_detail/<int:pk>/<int:form_id>', csrf_exempt(ChatDetail.as_view()), name='chat_detail'),
    path('chat_detail/message', chat_message, name='chat_message'),
    path('chat_detail/reply', chat_reply, name='chat_reply'),
    # path('chat_detail/thread/<int:id>', chat_thread, name='chat_thread'),
    path('comment_view/<int:form_id>', csrf_exempt(CommentView.as_view()), name='comment_view'),
    
    path('collabo/', CollaboList.as_view(), name='collabo_list'),
    path('collabo_create/', CollaboCreate.as_view(), name='collabo_create'),
    path('collabo_detail/<int:pk>', CollaboDetail.as_view(), name='collabo_detail'),
    
    path('todo/', TodoList.as_view(), name='todo_list'),
    path('todo_create/', TodoCreate.as_view(), name='todo_create'),
    path('todo_detail/<int:pk>', TodoDetail.as_view(), name='todo_detail'),
    path('todo_update/<int:pk>', TodoUpdate.as_view(), name='todo_update'),
    path('todo_delete/<int:pk>', TodoDelete.as_view(), name='todo_delete'),
    
    path('searchtag_create/', searchtag_create, name='searchtag_create'),
    path('like_form/', like_form, name='like_form'),
    path('comment_form/', comment_form, name='comment_form'),
    path('reply_form/', reply_form, name='reply_form'),
    
    path('signup/', signup_form, name='signup'),
    path('login/', login_form, name='login'),
    path('logout/', logout_form, name='logout'),
    path('withdrawal/', Withdrawal.as_view(), name='withdrawal'),
    path('withdrawal/<str:token>', Withdrawal.as_view(), name='withdrawal'),
]
