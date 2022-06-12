from django.urls import path
from api.views_api import SignUpAPIView, PingView

app_name = 'myus'

urlpatterns = [
    path('signup', SignUpAPIView.as_view(), name='signup'),
    path('ping/', PingView),
]
