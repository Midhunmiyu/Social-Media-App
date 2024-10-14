from django.urls import include, path
from user.views import *

urlpatterns = [
     path('registration/', RegistrationView.as_view()),
]