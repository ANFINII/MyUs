from django.urls import path
from .views import Index, Recommend, UserPage, TagCreate, LikeForm, CommentForm
from .views import Signup, Login, Logout, Withdrawal
from .views import Profile, Profile_update, MyPage, MyPage_update
from .views import UserPolicy, Knowledge, FollowCreate, FollowList, FollowerList
from .views import VideoList, VideoCreate, VideoDetail
from .views import LiveList, LiveCreate, LiveDetail
from .views import MusicList, MusicCreate, MusicDetail
from .views import PictureList, PictureCreate, PictureDetail
from .views import BlogList, BlogCreate, BlogDetail
from .views import ChatList, ChatCreate, ChatDetail, ChatMessage
from .views import CollaboList, CollaboCreate, CollaboDetail
from .views import TodoList, TodoDetail, TodoCreate, TodoDelete, TodoUpdate

app_name = 'myus'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('recommend/', Recommend.as_view(), name='recommend'),
    path('userpage/<str:nickname>', UserPage.as_view(), name='userpage'),
    path('tag_create/', TagCreate, name='tag_create'),
    path('like_form/', LikeForm, name='like_form'),
    path('comment_form/', CommentForm, name='comment_form'),

    path('signup/', Signup, name='signup'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('withdrawal/', Withdrawal.as_view(), name='withdrawal'),
    path('withdrawal/<str:token>', Withdrawal.as_view(), name='withdrawal'),
    
    path('userpolicy/', UserPolicy, name='userpolicy'),
    path('knowledge/', Knowledge, name='knowledge'),
    path('follow/', FollowList.as_view(), name='follow_list'),
    path('follower/', FollowerList.as_view(), name='follower_list'),
    path('follow_create/<str:nickname>', FollowCreate, name='follow_create'),

    path('profile/', Profile, name='profile'),
    path('profile_update/', Profile_update.as_view(), name='profile_update'),
    path('mypage/', MyPage, name='mypage'),
    path('mypage_update/', MyPage_update.as_view(), name='mypage_update'),

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
    path('chat_detail/message', ChatMessage, name='chat_message'),
    
    path('collabo/', CollaboList.as_view(), name='collabo_list'),
    path('collabo_create/', CollaboCreate.as_view(), name='collabo_create'),
    path('collabo_detail/<int:pk>', CollaboDetail.as_view(), name='collabo_detail'),
    
    path('todo/', TodoList.as_view(), name='todo_list'),
    path('todo_create/', TodoCreate.as_view(), name='todo_create'),
    path('todo_detail/<int:pk>', TodoDetail.as_view(), name='todo_detail'),
    path('todo_update/<int:pk>', TodoUpdate.as_view(), name='todo_update'),
    path('todo_delete/<int:pk>', TodoDelete.as_view(), name='todo_delete'),
]