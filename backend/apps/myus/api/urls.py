from django.urls import path
from apps.myus.api.views import UserView
from apps.myus.api.views import LoginAPIView, SignUpAPIView

app_name = 'myus'

urlpatterns = [
    path('user', UserView.as_view(), name='user'),
    path('signupview', SignUpAPIView.as_view(), name='signupview'),
    path('login', LoginAPIView.as_view(), name='login'),
]
