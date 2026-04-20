from ninja import NinjaAPI
from api.src.adapter.auth import AuthAPI
from api.src.adapter.comment import CommentAPI
from api.src.adapter.manage import ManageComicAPI, ManageMusicAPI, ManageVideoAPI
from api.src.adapter.media import BlogAPI, ChatAPI, ComicAPI, HomeAPI, MusicAPI, PictureAPI, RecommendAPI, VideoAPI
from api.src.adapter.message import MessageAPI
from api.src.adapter.channel import ChannelAPI
from api.src.adapter.setting import SettingMyPageAPI, SettingNotificationAPI, SettingProfileAPI
from api.src.adapter.user import UserAPI


api = NinjaAPI(title="MyUs API")

api.add_router("/auth", AuthAPI().router, tags=["auth"])
api.add_router("/user", UserAPI().router, tags=["user"])

api.add_router("/setting/profile", SettingProfileAPI().router, tags=["Setting"])
api.add_router("/setting/mypage", SettingMyPageAPI().router, tags=["Setting"])
api.add_router("/setting/notification", SettingNotificationAPI().router, tags=["Setting"])

api.add_router("/manage/media/video", ManageVideoAPI().router, tags=["Manage Video"])
api.add_router("/manage/media/music", ManageMusicAPI().router, tags=["Manage Music"])
api.add_router("/manage/media/comic", ManageComicAPI().router, tags=["Manage Comic"])

api.add_router("/channel", ChannelAPI().router, tags=["Channel"])
api.add_router("/media/home", HomeAPI().router, tags=["Media Home"])
api.add_router("/media/recommend", RecommendAPI().router, tags=["Media Recommend"])
api.add_router("/media/video", VideoAPI().router, tags=["Media Video"])
api.add_router("/media/music", MusicAPI().router, tags=["Media Music"])
api.add_router("/media/comic", ComicAPI().router, tags=["Media Comic"])
api.add_router("/media/picture", PictureAPI().router, tags=["Media Picture"])
api.add_router("/media/blog", BlogAPI().router, tags=["Media Blog"])
api.add_router("/media/chat", ChatAPI().router, tags=["Media Chat"])
api.add_router("/media/comment", CommentAPI().router, tags=["Media Comment"])
api.add_router("/media/message", MessageAPI().router, tags=["Media Message"])
