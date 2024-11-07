from django.urls import path
from myus.app.consumers import ChatConsumer


websocket_urlpatterns = [
    path('ws/chat/detail/<pk>', ChatConsumer.as_asgi()),
]
