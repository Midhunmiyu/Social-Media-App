from django.urls import path
from userpost.views import *



urlpatterns = [
    path('posts/',PostCreateView.as_view()),
]