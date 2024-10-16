from django.urls import include, path
from user.views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
     path('registration/', RegistrationView.as_view()),
     path('login/', LoginView.as_view()),
     path('refresh/', TokenRefreshView.as_view()),
     path('logout/', LogoutView.as_view()),
     path('profile/', ProfileView.as_view()),
     path('change-profile-picture/', ChangeProfilePictureView.as_view()),
     path('follow-request/', FollowRequestView.as_view()),
     path('accept-follow-request/', AcceptFollowRequestView.as_view()),
]