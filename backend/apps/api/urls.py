from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from apps.api.views import UserAPI, SignUpAPI, LoginAPI, LogoutAPI
from apps.api.views import IndexAPI


app_name = 'myus'

urlpatterns = [
    path('user', UserAPI.as_view()),
    path('signup', SignUpAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('logout', LogoutAPI.as_view()),
    path('verify', TokenVerifyView.as_view()),
    path('refresh', TokenRefreshView.as_view()),
]
