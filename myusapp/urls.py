from django.urls import path
from .views import Index, Recommend, UserPage, TagCreate
from .views import Signup, Login, Logout, Withdrawal
from .views import Profile, Profile_update, MyPage, MyPage_update
from .views import UserPolicy, Knowledge, FollowCreate, FollowList, FollowerList
from .views import VideoList, VideoCreate, VideoDetail, VideoLike, VideoComment
from .views import LiveList, LiveCreate, LiveDetail, LiveLike, LiveComment
from .views import MusicList, MusicCreate, MusicDetail, MusicLike, MusicComment
from .views import PictureList, PictureCreate, PictureDetail, PictureLike, PictureComment
from .views import BlogList, BlogCreate, BlogDetail, BlogLike, BlogComment
from .views import ChatList, ChatCreate, ChatDetail, ChatLike, ChatComment
from .views import CollaboList, CollaboCreate, CollaboDetail, CollaboLike, CollaboComment
from .views import TodoList, TodoDetail, TodoCreate, TodoDelete, TodoUpdate, TodoComment

app_name = 'myus'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('recommend/', Recommend.as_view(), name='recommend'),
    path('userpage/<str:nickname>', UserPage.as_view(), name='userpage'),
    path('tag_create/', TagCreate, name='tag_create'),

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
    path('video_detail/like', VideoLike, name='video_like'),
    path('video_detail/comment', VideoComment, name='video_comment'),
    
    path('live/', LiveList.as_view(), name='live_list'),
    path('live_create/', LiveCreate.as_view(), name='live_create'),
    path('live_detail/<int:pk>', LiveDetail.as_view(), name='live_detail'),
    path('live_detail/like', LiveLike, name='live_like'),
    # path('live_detail/comment', LiveComment, name='live_comment'),
    
    path('music/', MusicList.as_view(), name='music_list'),
    path('music_create/', MusicCreate.as_view(), name='music_create'),
    path('music_detail/<int:pk>', MusicDetail.as_view(), name='music_detail'),
    path('music_detail/like', MusicLike, name='music_like'),
    # path('music_detail/comment', MusicComment, name='music_comment'),
    
    path('picture/', PictureList.as_view(), name='picture_list'),
    path('picture_create/', PictureCreate.as_view(), name='picture_create'),
    path('picture_detail/<int:pk>', PictureDetail.as_view(), name='picture_detail'),
    path('picture_detail/like', PictureLike, name='picture_like'),
    # path('picture_detail/comment', PictureComment, name='picture_comment'),
    
    path('blog/', BlogList.as_view(), name='blog_list'),
    path('blog_create/', BlogCreate.as_view(), name='blog_create'),
    path('blog_detail/<int:pk>', BlogDetail.as_view(), name='blog_detail'),
    path('blog_detail/like', BlogLike, name='blog_like'),
    # path('blog_detail/comment', BlogComment, name='blog_comment'),
    
    path('chat/', ChatList.as_view(), name='chat_list'),
    path('chat_create/', ChatCreate.as_view(), name='chat_create'),
    path('chat_detail/<int:pk>', ChatDetail.as_view(), name='chat_detail'),
    path('chat_detail/like', ChatLike, name='chat_like'),
    # path('chat_detail/comment', ChatComment, name='chat_comment'),
    
    path('collabo/', CollaboList.as_view(), name='collabo_list'),
    path('collabo_create/', CollaboCreate.as_view(), name='collabo_create'),
    path('collabo_detail/<int:pk>', CollaboDetail.as_view(), name='collabo_detail'),
    path('collabo_detail/like', CollaboLike, name='collabo_like'),
    # path('collabo_detail/comment', CollaboComment, name='collabo_comment'),
    
    path('todo/', TodoList.as_view(), name='todo_list'),
    path('todo_create/', TodoCreate.as_view(), name='todo_create'),
    path('todo_detail/<int:pk>', TodoDetail.as_view(), name='todo_detail'),
    path('todo_update/<int:pk>', TodoUpdate.as_view(), name='todo_update'),
    path('todo_delete/<int:pk>', TodoDelete.as_view(), name='todo_delete'),
    # path('todo_delete/comment', TodoComment, name='todo_comment'),
]