from django.urls import path
from api.views.auth import AuthAPI, RefreshAPI, SignUpAPI, LoginAPI, LogoutAPI
from api.views.user import UserAPI, SearchTagAPI, FollowAPI, FollowerAPI, NotificationAPI
from api.views.setting import SettingProfileAPI, SettingMyPageAPI, SettingNotificationAPI
from api.views.media import HomeAPI
from api.views.media import VideoListAPI, VideoAPI
from api.views.media import MusicListAPI, MusicAPI
from api.views.media import ComicListAPI, ComicAPI
from api.views.media import PictureListAPI, PictureAPI
from api.views.media import BlogListAPI, BlogAPI
from api.views.media import ChatListAPI, ChatAPI
from api.views.comment import CommentAPI


app_name = "myus"

urlpatterns = [
    path("auth", AuthAPI.as_view()),
    path("auth/refresh", RefreshAPI.as_view()),
    path("auth/signup", SignUpAPI.as_view()),
    path("auth/login", LoginAPI.as_view()),
    path("auth/logout", LogoutAPI.as_view()),

    path("user/me", UserAPI.as_view()),
    path("user/search_tag", SearchTagAPI.as_view()),
    path("user/follow", FollowAPI.as_view()),
    path("user/follower", FollowerAPI.as_view()),
    path("user/notification", NotificationAPI.as_view()),

    path("setting/profile", SettingProfileAPI.as_view()),
    path("setting/mypage", SettingMyPageAPI.as_view()),
    path("setting/notification", SettingNotificationAPI.as_view()),

    path("home", HomeAPI.as_view()),

    path("media/video", VideoListAPI.as_view()),
    path("media/video/<int:id>", VideoAPI.as_view()),
    path("media/video/create", VideoAPI.as_view()),

    path("media/music", MusicListAPI.as_view()),
    path("media/music/<int:id>", MusicAPI.as_view()),
    path("media/music/create", MusicAPI.as_view()),

    path("media/comic", ComicListAPI.as_view()),
    path("media/comic/<int:id>", ComicAPI.as_view()),
    path("media/comic/create", ComicAPI.as_view()),

    path("media/picture", PictureListAPI.as_view()),
    path("media/picture/<int:id>", PictureAPI.as_view()),
    path("media/picture/create", PictureAPI.as_view()),

    path("media/blog", BlogListAPI.as_view()),
    path("media/blog/<int:id>", BlogAPI.as_view()),
    path("media/blog/create", BlogAPI.as_view()),

    path("media/chat", ChatListAPI.as_view()),
    path("media/chat/<int:id>", ChatAPI.as_view()),
    path("media/chat/create", ChatAPI.as_view()),

    path("media/comment", CommentAPI.as_view()),
    path("media/comment/<int:id>", CommentAPI.as_view()),
]
