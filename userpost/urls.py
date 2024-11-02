from django.urls import path
from userpost.views import *



urlpatterns = [
    path('posts/',PostCreateView.as_view()),
    path('likes/',PostLikeView.as_view()),
    path('comments/',CommentView.as_view()),
]