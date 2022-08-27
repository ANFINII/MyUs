from django.urls import path
from apps.myus.consumers import ChatConsumer


websocket_urlpatterns = [
    path('ws/chat/detail/<pk>', ChatConsumer.as_asgi()),
]
