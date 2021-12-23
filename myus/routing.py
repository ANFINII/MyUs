from django.urls import path
from myus.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/detail/<pk>', ChatConsumer.as_asgi()),
]
