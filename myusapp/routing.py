from django.urls import path
from myusapp.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/Index2/', ChatConsumer.as_asgi()),
]
