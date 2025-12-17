from ninja import NinjaAPI
from api.src.adapter.auth import AuthAPI
from api.src.adapter.user import UserAPI
from api.src.adapter.media import HomeAPI, VideoAPI, MusicAPI, ComicAPI, PictureAPI, BlogAPI, ChatAPI
from api.src.adapter.setting import SettingProfileAPI, SettingMyPageAPI, SettingNotificationAPI
from api.src.adapter.comment import CommentAPI


api = NinjaAPI(title="MyUs API")

api.add_router("/auth", AuthAPI().router, tags=["auth"])
api.add_router("/user", UserAPI().router, tags=["user"])

api.add_router("/setting/profile", SettingProfileAPI().router, tags=["Setting"])
api.add_router("/setting/mypage", SettingMyPageAPI().router, tags=["Setting"])
api.add_router("/setting/notification", SettingNotificationAPI().router, tags=["Setting"])

api.add_router("/media/home", HomeAPI().router, tags=["Media Home"])
api.add_router("/media/video", VideoAPI().router, tags=["Media Video"])
api.add_router("/media/music", MusicAPI().router, tags=["Media Music"])
api.add_router("/media/comic", ComicAPI().router, tags=["Media Comic"])
api.add_router("/media/picture", PictureAPI().router, tags=["Media Picture"])
api.add_router("/media/blog", BlogAPI().router, tags=["Media Blog"])
api.add_router("/media/chat", ChatAPI().router, tags=["Media Chat"])
api.add_router("/media/comment", CommentAPI().router, tags=["Media Comment"])
