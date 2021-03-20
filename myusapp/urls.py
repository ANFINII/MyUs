from django.urls import path
from .views import Index, Recommend, Signup, Login, Logout, Withdrawal
from .views import Profile, Profile_update, UserPolicy, Knowledge
from .views import FollowList, FollowerList, FollowCreate, UserPage
from .views import VideoList, VideoCreate, VideoDetail, VideoLike
from .views import LiveList, LiveCreate, LiveDetail, LiveLike
from .views import MusicList, MusicCreate, MusicDetail, MusicLike
from .views import PictureList, PictureCreate, PictureDetail, PictureLike
from .views import BlogList, BlogCreate, BlogDetail, BlogLike
from .views import ChatList, ChatCreate, ChatDetail, ChatLike
from .views import CollaboList, CollaboCreate, CollaboDetail, CollaboLike
from .views import TodoList, TodoDetail, TodoCreate, TodoDelete, TodoUpdate

app_name = 'myus'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('recommend/', Recommend.as_view(), name='recommend'),
    path('signup/', Signup, name='signup'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('withdrawal/', Withdrawal.as_view(), name='withdrawal'),
    path('withdrawal/<str:token>', Withdrawal.as_view(), name='withdrawal'),

    path('profile/', Profile, name='profile'),
    path('profile_update/', Profile_update.as_view(), name='profile_update'),
    path('userpolicy/', UserPolicy, name='userpolicy'),
    path('knowledge/', Knowledge, name='knowledge'),

    path('follow/', FollowList.as_view(), name='follow_list'),
    path('follower/', FollowerList.as_view(), name='follower_list'),
    path('follow_create/', FollowCreate.as_view(), name='follow_create'),
    path('userpage/<str:nickname>', UserPage.as_view(), name='userpage'),

    path('video/', VideoList.as_view(), name='video_list'),
    path('video_create/', VideoCreate.as_view(), name='video_create'),
    path('video_detail/<int:pk>', VideoDetail.as_view(), name='video_detail'),
    path('video_like/<int:pk>', VideoLike, name='video_like'),

    path('live/', LiveList.as_view(), name='live_list'),
    path('live_create/', LiveCreate.as_view(), name='live_create'),
    path('live_detail/<int:pk>', LiveDetail.as_view(), name='live_detail'),
    path('live_like/<int:pk>/', LiveLike, name='live_like'),

    path('music/', MusicList.as_view(), name='music_list'),
    path('music_create/', MusicCreate.as_view(), name='music_create'),
    path('music_detail/<int:pk>', MusicDetail.as_view(), name='music_detail'),
    path('music_like/<int:pk>', MusicLike, name='music_like'),

    path('picture/', PictureList.as_view(), name='picture_list'),
    path('picture_create/', PictureCreate.as_view(), name='picture_create'),
    path('picture_detail/<int:pk>', PictureDetail.as_view(), name='picture_detail'),
    path('picture_like/<int:pk>', PictureLike, name='picture_like'),

    path('blog/', BlogList.as_view(), name='blog_list'),
    path('blog_create/', BlogCreate.as_view(), name='blog_create'),
    path('blog_detail/<int:pk>', BlogDetail.as_view(), name='blog_detail'),
    path('blog_like/<int:pk>', BlogLike, name='blog_like'),

    path('chat/', ChatList.as_view(), name='chat_list'),
    path('chat_create/', ChatCreate.as_view(), name='chat_create'),
    path('chat_detail/<int:pk>', ChatDetail.as_view(), name='chat_detail'),
    path('chat_like/<int:pk>', ChatLike, name='chat_like'),
    
    path('collabo/', CollaboList.as_view(), name='collabo_list'),
    path('collabo_create/', CollaboCreate.as_view(), name='collabo_create'),
    path('collabo_detail/<int:pk>', CollaboDetail.as_view(), name='collabo_detail'),
    path('collabo_like/<int:pk>', CollaboLike, name='collabo_like'),
    
    path('todo/', TodoList.as_view(), name='todo_list'),
    path('todo_create/', TodoCreate.as_view(), name='todo_create'),
    path('todo_detail/<int:pk>', TodoDetail.as_view(), name='todo_detail'),
    path('todo_update/<int:pk>', TodoUpdate.as_view(), name='todo_update'),
    path('todo_delete/<int:pk>', TodoDelete.as_view(), name='todo_delete'),
]