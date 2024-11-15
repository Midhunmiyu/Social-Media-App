from django.urls import path
from chat.consumers import *

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', MyChatConsumer.as_asgi()),
]