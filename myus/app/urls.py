from django.urls import path
from app.views import pjax, login_form, logout_form, signup_form, SignupComplete
from app.views import PasswordReset, PasswordResetDone, PasswordResetConfirm, PasswordResetComplete
from app.views import Index, Recommend, UserPage, UserPageInfo, UserPageAdvertise
from app.views import ProfileView, ProfileUpdate, MyPageView, MyPageUpdate, mypage_toggle, Withdrawal
from app.views import Payment, PaymentSuccess, PaymentCancel, ChangePlan, create_checkout_session
from app.views import UserNotificationView, notification_update, notification_confirmed, notification_deleted
from app.views import UserPolicy, Knowledge, FollowerList, FollowList, follow_create
from app.views import VideoList, VideoCreate, VideoDetail
from app.views import MusicList, MusicCreate, MusicDetail
from app.views import ComicList, ComicCreate, ComicDetail
from app.views import PictureList, PictureCreate, PictureDetail
from app.views import BlogList, BlogCreate, BlogDetail
from app.views import ChatList, ChatCreate, ChatDetail, ChatThread, chat_thread_button
from app.views import searchtag_create, advertise_read, like_form, like_form_comment
from app.views import comment_form, comment_update, comment_delete, reply_form, reply_delete

app_name = "app"

urlpatterns = [
    path("pjax", pjax, name="pjax"),
    path("login", login_form, name="login"),
    path("logout", logout_form, name="logout"),
    path("signup", signup_form, name="signup"),
    path("signup/complete/<token>/", SignupComplete.as_view(), name="signup_complete"),

    path("password_reset/", PasswordReset.as_view(), name="password_reset"),
    path("password_reset/done/", PasswordResetDone.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path("reset/done/", PasswordResetComplete.as_view(), name="password_reset_complete"),

    path("", Index.as_view(), name="index"),
    path("recommend", Recommend.as_view(), name="recommend"),
    path("userpage/post/<str:nickname>", UserPage.as_view(), name="userpage"),
    path("userpage/information/<str:nickname>", UserPageInfo.as_view(), name="userpage_info"),
    path("userpage/advertise/<str:nickname>", UserPageAdvertise.as_view(), name="userpage_advertise"),

    path("setting/profile", ProfileView.as_view(), name="profile"),
    path("setting/profile/update", ProfileUpdate.as_view(), name="profile_update"),
    path("setting/mypage", MyPageView.as_view(), name="mypage"),
    path("setting/mypage/update", MyPageUpdate.as_view(), name="mypage_update"),
    path("setting/mypage/toggle", mypage_toggle, name="mypage_toggle"),
    path("setting/withdrawal", Withdrawal.as_view(), name="withdrawal"),
    path("setting/withdrawal/<str:token>", Withdrawal.as_view(), name="withdrawal"),

    path("setting/payment", Payment.as_view(), name="payment"),
    path("setting/payment/success", PaymentSuccess.as_view(), name="payment_success"),
    path("setting/payment/cancel", PaymentCancel.as_view(), name="payment_cancel"),
    path("setting/payment/chage_plan", ChangePlan.as_view(), name="chage_plan"),
    path("setting/payment/create_checkout_session", create_checkout_session, name="create_checkout_session"),

    path("setting/notification", UserNotificationView.as_view(), name="notification"),
    path("setting/notification/update", notification_update, name="notification_update"),
    path("setting/notification/confirmed", notification_confirmed, name="notification_confirmed"),
    path("setting/notification/deleted", notification_deleted, name="notification_deleted"),

    path("menu/userpolicy", UserPolicy.as_view(), name="userpolicy"),
    path("menu/knowledge", Knowledge.as_view(), name="knowledge"),
    path("menu/follower", FollowerList.as_view(), name="follower_list"),
    path("menu/follow", FollowList.as_view(), name="follow_list"),
    path("menu/follow/create/<str:nickname>", follow_create, name="follow_create"),

    path("media/video", VideoList.as_view(), name="video_list"),
    path("media/video/create", VideoCreate.as_view(), name="video_create"),
    path("media/video/detail/<int:pk>/<str:title>", VideoDetail.as_view(), name="video_detail"),

    path("media/music", MusicList.as_view(), name="music_list"),
    path("media/music/create", MusicCreate.as_view(), name="music_create"),
    path("media/music/detail/<int:pk>/<str:title>", MusicDetail.as_view(), name="music_detail"),

    path("media/comic", ComicList.as_view(), name="comic_list"),
    path("media/comic/create", ComicCreate.as_view(), name="comic_create"),
    path("media/comic/detail/<int:pk>/<str:title>", ComicDetail.as_view(), name="comic_detail"),

    path("media/picture", PictureList.as_view(), name="picture_list"),
    path("media/picture/create", PictureCreate.as_view(), name="picture_create"),
    path("media/picture/detail/<int:pk>/<str:title>", PictureDetail.as_view(), name="picture_detail"),

    path("media/blog", BlogList.as_view(), name="blog_list"),
    path("media/blog/create", BlogCreate.as_view(), name="blog_create"),
    path("media/blog/detail/<int:pk>/<str:title>", BlogDetail.as_view(), name="blog_detail"),

    path("media/chat", ChatList.as_view(), name="chat_list"),
    path("media/chat/create", ChatCreate.as_view(), name="chat_create"),
    path("media/chat/detail/<int:pk>", ChatDetail.as_view(), name="chat_detail"),
    path("media/chat/detail/<int:pk>/thread/<int:message_id>", ChatThread.as_view(), name="chat_thread"),
    path("media/chat/detail/thread", chat_thread_button, name="chat_thread_button"),

    path("searchtag/create", searchtag_create, name="searchtag_create"),
    path("url/read", advertise_read, name="advertise_read"),
    path("like/form", like_form, name="like_form"),
    path("like/form/comment", like_form_comment, name="like_form_comment"),

    path("comment/form", comment_form, name="comment_form"),
    path("comment/update/<int:comment_id>", comment_update, name="comment_update"),
    path("comment/delete/<int:comment_id>", comment_delete, name="comment_delete"),
    path("reply/form", reply_form, name="reply_form"),
    path("reply/delete/<int:comment_id>", reply_delete, name="reply_delete"),
]
