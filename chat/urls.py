from django.urls import path
from chat.views import *


urlpatterns = [
    path('chat-room/', ChatRoomView.as_view()),
]