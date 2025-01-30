from django.urls import path

from users.api import auth, users

urlpatterns = [
    path("", users.UserRegistrationAPI.as_view()),
    path("login/", auth.UserLoginAPI.as_view()),
]
