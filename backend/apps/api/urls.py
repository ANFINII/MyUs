from django.urls import path
from apps.api.views import AuthAPI, SignUpAPI, LoginAPI, LogoutAPI, RefreshAPI
from apps.api.views import UserAPI, ProfileAPI, MyPageAPI
from apps.api.views import IndexAPI
from apps.api.views import VideoListAPI, VideoCreateAPI, VideoDetailAPI
from apps.api.views import MusicListAPI, MusicCreateAPI, MusicDetailAPI
from apps.api.views import ComicListAPI, ComicCreateAPI, ComicDetailAPI
from apps.api.views import PictureListAPI, PictureCreateAPI, PictureDetailAPI
from apps.api.views import BlogListAPI, BlogCreateAPI, BlogDetailAPI
from apps.api.views import ChatListAPI, ChatCreateAPI, ChatDetailAPI
from apps.api.views import TodoListAPI, TodoCreateAPI, TodoDetailAPI


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

    path('index', IndexAPI.as_view()),

    path('media/video', VideoListAPI.as_view()),
    path('media/video/create', VideoCreateAPI.as_view()),
    path('media/video/detail/<int:id>', VideoDetailAPI.as_view()),

    path('media/music', MusicListAPI.as_view()),
    path('media/music/create', MusicCreateAPI.as_view()),
    path('media/music/detail/<int:id>', MusicDetailAPI.as_view()),

    path('media/comic', ComicListAPI.as_view()),
    path('media/comic/create', ComicCreateAPI.as_view()),
    path('media/comic/detail/<int:id>', ComicDetailAPI.as_view()),

    path('media/picture', PictureListAPI.as_view()),
    path('media/picture/create', PictureCreateAPI.as_view()),
    path('media/picture/detail/<int:id>', PictureDetailAPI.as_view()),

    path('media/blog', BlogListAPI.as_view()),
    path('media/blog/create', BlogCreateAPI.as_view()),
    path('media/blog/detail/<int:id>', BlogDetailAPI.as_view()),

    path('media/chat', ChatListAPI.as_view()),
    path('media/chat/create', ChatCreateAPI.as_view()),
    path('media/chat/detail/<int:id>', ChatDetailAPI.as_view()),

    path('media/todo', TodoListAPI.as_view()),
    path('media/todo/create', TodoCreateAPI.as_view()),
    path('media/todo/detail/<int:id>', TodoDetailAPI.as_view()),
]
