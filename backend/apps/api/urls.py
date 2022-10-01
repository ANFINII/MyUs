from django.urls import path
from apps.api.views import SignUpAPI, LoginAPI, LogoutAPI, VerifyAPI, RefreshAPI
from apps.api.views import UserAPI, MyPageAPI


app_name = 'api'

urlpatterns = [
    path('user', UserAPI.as_view()),
    path('mypage', MyPageAPI.as_view()),
    path('signup', SignUpAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('logout', LogoutAPI.as_view()),
    path('verify', VerifyAPI.as_view()),
    path('refresh', RefreshAPI.as_view()),
]
