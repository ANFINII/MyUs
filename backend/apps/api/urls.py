from django.urls import path
from apps.api.views import AuthAPI, SignUpAPI, LoginAPI, LogoutAPI, RefreshAPI
from apps.api.views import UserAPI, ProfileAPI, MyPageAPI, NotificationAPI
from apps.api.views import HomeAPI
from apps.api.views import VideoListAPI, VideoCreateAPI, VideoAPI
from apps.api.views import MusicListAPI, MusicCreateAPI, MusicAPI
from apps.api.views import ComicListAPI, ComicCreateAPI, ComicAPI
from apps.api.views import PictureListAPI, PictureCreateAPI, PictureAPI
from apps.api.views import BlogListAPI, BlogCreateAPI, BlogAPI
from apps.api.views import ChatListAPI, ChatCreateAPI, ChatAPI
from apps.api.views import TodoListAPI, TodoCreateAPI, TodoAPI


app_name = 'api'

urlpatterns = [
    path('auth', AuthAPI.as_view()),
    path('signup', SignUpAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('logout', LogoutAPI.as_view()),
    path('refresh', RefreshAPI.as_view()),

    path('user', UserAPI.as_view()),
    path('profile', ProfileAPI.as_view()),
    path('mypage', MyPageAPI.as_view()),
    path('notification', NotificationAPI.as_view()),

    path('home', HomeAPI.as_view()),

    path('media/video', VideoListAPI.as_view()),
    path('media/video/<int:id>', VideoAPI.as_view()),
    path('media/video/create', VideoCreateAPI.as_view()),

    path('media/music', MusicListAPI.as_view()),
    path('media/music/<int:id>', MusicAPI.as_view()),
    path('media/music/create', MusicCreateAPI.as_view()),

    path('media/comic', ComicListAPI.as_view()),
    path('media/comic/<int:id>', ComicAPI.as_view()),
    path('media/comic/create', ComicCreateAPI.as_view()),

    path('media/picture', PictureListAPI.as_view()),
    path('media/picture/<int:id>', PictureAPI.as_view()),
    path('media/picture/create', PictureCreateAPI.as_view()),

    path('media/blog', BlogListAPI.as_view()),
    path('media/blog/<int:id>', BlogAPI.as_view()),
    path('media/blog/create', BlogCreateAPI.as_view()),

    path('media/chat', ChatListAPI.as_view()),
    path('media/chat/<int:id>', ChatAPI.as_view()),
    path('media/chat/create', ChatCreateAPI.as_view()),

    path('media/todo', TodoListAPI.as_view()),
    path('media/todo/<int:id>', TodoAPI.as_view()),
    path('media/todo/create', TodoCreateAPI.as_view()),
]
