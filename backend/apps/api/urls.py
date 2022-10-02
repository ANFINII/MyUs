from django.urls import path
from apps.api.views import AuthAPI, SignUpAPI, LoginAPI, LogoutAPI, RefreshAPI
from apps.api.views import ProfileAPI, MyPageAPI


app_name = 'api'

urlpatterns = [
    path('auth', AuthAPI.as_view()),
    path('signup', SignUpAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('logout', LogoutAPI.as_view()),
    path('refresh', RefreshAPI.as_view()),

    path('profile', ProfileAPI.as_view()),
    path('mypage', MyPageAPI.as_view()),
]
