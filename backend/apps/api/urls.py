from django.urls import path
from apps.api.views import AuthAPI, SignUpAPI, LoginAPI, LogoutAPI, RefreshAPI
from apps.api.views import ProfileAPI, MyPageAPI
from apps.api.views import IndexAPI
from apps.api.views import VideoListAPI, VideoCreateAPI, VideoDetailAPI
from apps.api.views import MusicListAPI, MusicCreateAPI, MusicDetailAPI
from apps.api.views import PictureListAPI, PictureCreateAPI, PictureDetailAPI
from apps.api.views import BlogListAPI, BlogCreateAPI, BlogDetailAPI
from apps.api.views import ChatListAPI, ChatCreateAPI, ChatDetailAPI
from apps.api.views import CollaboListAPI, CollaboCreateAPI, CollaboDetailAPI


app_name = 'api'

urlpatterns = [
    path('auth', AuthAPI.as_view()),
    path('signup', SignUpAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('logout', LogoutAPI.as_view()),
    path('refresh', RefreshAPI.as_view()),

    path('profile', ProfileAPI.as_view()),
    path('mypage', MyPageAPI.as_view()),

    path('index', IndexAPI.as_view()),

    path('video', VideoListAPI.as_view()),
    path('video/create', VideoCreateAPI.as_view()),
    path('video/detail/<int:id>', VideoDetailAPI.as_view()),

    path('music', MusicListAPI.as_view()),
    path('music/create', MusicCreateAPI.as_view()),
    path('music/detail/<int:id>', MusicDetailAPI.as_view()),

    path('picture', PictureListAPI.as_view()),
    path('picture/create', PictureCreateAPI.as_view()),
    path('picture/detail/<int:id>', PictureDetailAPI.as_view()),

    path('blog', BlogListAPI.as_view()),
    path('blog/create', BlogCreateAPI.as_view()),
    path('blog/detail/<int:id>', BlogDetailAPI.as_view()),

    path('chat', ChatListAPI.as_view()),
    path('chat/create', ChatCreateAPI.as_view()),
    path('chat/detail/<int:id>', ChatDetailAPI.as_view()),

    path('collabo', CollaboListAPI.as_view()),
    path('collabo/create', CollaboCreateAPI.as_view()),
    path('collabo/detail/<int:id>', CollaboDetailAPI.as_view()),
]
