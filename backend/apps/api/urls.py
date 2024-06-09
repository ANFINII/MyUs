from django.urls import path
from apps.api.views.auth import AuthAPI, RefreshAPI, SignUpAPI, LoginAPI, LogoutAPI
from apps.api.views.user import ProfileAPI, MyPageAPI, SearchTagAPI, NotificationAPI
from apps.api.views.media import HomeAPI
from apps.api.views.media import VideoListAPI, VideoCreateAPI, VideoAPI
from apps.api.views.media import MusicListAPI, MusicCreateAPI, MusicAPI
from apps.api.views.media import ComicListAPI, ComicCreateAPI, ComicAPI
from apps.api.views.media import PictureListAPI, PictureCreateAPI, PictureAPI
from apps.api.views.media import BlogListAPI, BlogCreateAPI, BlogAPI
from apps.api.views.media import ChatListAPI, ChatCreateAPI, ChatAPI
from apps.api.views.media import TodoListAPI, TodoCreateAPI, TodoAPI


app_name = 'api'

urlpatterns = [
    path('auth', AuthAPI.as_view()),
    path('auth/refresh', RefreshAPI.as_view()),
    path('auth/signup', SignUpAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/logout', LogoutAPI.as_view()),

    path('user/profile', ProfileAPI.as_view()),
    path('user/mypage', MyPageAPI.as_view()),
    path('user/search_tag', SearchTagAPI.as_view()),
    path('user/notification', NotificationAPI.as_view()),

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
