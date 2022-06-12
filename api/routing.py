from django.urls import path
from api.consumers import ChatConsumer


websocket_urlpatterns = [
    path('ws/chat/detail/<pk>', ChatConsumer.as_asgi()),
]
