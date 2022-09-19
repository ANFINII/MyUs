from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.myus.api.views import UserAPI
from apps.myus.api.views import SignUpAPI, UserAPI, UserAPIView, LoginView


app_name = 'myus'


urlpatterns = [
    # path('api/login/', TokenObtainPairView.as_view()),
    path('api/refresh/', TokenRefreshView.as_view()),
    path('api/verify/', TokenVerifyView.as_view()),
    path('api/user', UserAPI.as_view(), name='userapi'),
    path('api/UserAPI', UserAPIView.as_view(), name='UserAPIView'),
    path('api/signup', SignUpAPI.as_view(), name='signupapi'),
    path('api/login', LoginView.as_view(), name='login'),
]
