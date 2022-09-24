from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from apps.myus.api.views import UserAPI, SignUpAPI, LogoutAPI


app_name = 'myus'


urlpatterns = [
    path('api/user', UserAPI.as_view()),
    path('api/signup', SignUpAPI.as_view()),
    path('api/login', LogoutAPI.as_view()),
    path('api/verify/', TokenVerifyView.as_view()),
    path('api/refresh/', TokenRefreshView.as_view()),
]
