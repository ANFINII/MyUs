from django.urls import path
from apps.api.views.auth import AuthAPI, RefreshAPI, SignUpAPI, LoginAPI, LogoutAPI
from apps.api.views.user import UserAPI, SearchTagAPI, FollowAPI, FollowerAPI, NotificationAPI
from apps.api.views.setting import SettingProfileAPI, SettingMyPageAPI, SettingNotificationAPI
from apps.api.views.media import HomeAPI
from apps.api.views.media import VideoListAPI, VideoAPI
from apps.api.views.media import MusicListAPI, MusicAPI
from apps.api.views.media import ComicListAPI, ComicAPI
from apps.api.views.media import PictureListAPI, PictureAPI
from apps.api.views.media import BlogListAPI, BlogAPI
from apps.api.views.media import ChatListAPI, ChatAPI
from apps.api.views.media import TodoListAPI, TodoAPI


app_name = 'api'

urlpatterns = [
    path('auth', AuthAPI.as_view()),
    path('auth/refresh', RefreshAPI.as_view()),
    path('auth/signup', SignUpAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/logout', LogoutAPI.as_view()),

    path('user/me', UserAPI.as_view()),
    path('user/search_tag', SearchTagAPI.as_view()),
    path('user/follow', FollowAPI.as_view()),
    path('user/follower', FollowerAPI.as_view()),
    path('user/notification', NotificationAPI.as_view()),

    path('setting/profile', SettingProfileAPI.as_view()),
    path('setting/mypage', SettingMyPageAPI.as_view()),
    path('setting/notification', SettingNotificationAPI.as_view()),

    path('home', HomeAPI.as_view()),

    path('media/video', VideoListAPI.as_view()),
    path('media/video/<int:id>', VideoAPI.as_view()),
    path('media/video/create', VideoAPI.as_view()),

    path('media/music', MusicListAPI.as_view()),
    path('media/music/<int:id>', MusicAPI.as_view()),
    path('media/music/create', MusicAPI.as_view()),

    path('media/comic', ComicListAPI.as_view()),
    path('media/comic/<int:id>', ComicAPI.as_view()),
    path('media/comic/create', ComicAPI.as_view()),

    path('media/picture', PictureListAPI.as_view()),
    path('media/picture/<int:id>', PictureAPI.as_view()),
    path('media/picture/create', PictureAPI.as_view()),

    path('media/blog', BlogListAPI.as_view()),
    path('media/blog/<int:id>', BlogAPI.as_view()),
    path('media/blog/create', BlogAPI.as_view()),

    path('media/chat', ChatListAPI.as_view()),
    path('media/chat/<int:id>', ChatAPI.as_view()),
    path('media/chat/create', ChatAPI.as_view()),

    path('media/todo', TodoListAPI.as_view()),
    path('media/todo/<int:id>', TodoAPI.as_view()),
    path('media/todo/create', TodoAPI.as_view()),
]
