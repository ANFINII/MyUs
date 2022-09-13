from django.urls import path
from apps.myus.api.views import UserAPI
from apps.myus.api.views import LoginAPI, SignUpAPI, CustomAuthToken

app_name = 'myus'

urlpatterns = [
    path('user', UserAPI.as_view(), name='user'),
    path('signupapi', SignUpAPI.as_view(), name='signupapi'),
    path('loginapi', LoginAPI.as_view(), name='loginapi'),
    path('auth/login', CustomAuthToken.as_view()),
]
