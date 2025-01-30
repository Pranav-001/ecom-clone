from django.urls import path

from users.api import auth, users

urlpatterns = [
    path("", users.UserRegistration.as_view()),
    path("login/", auth.UserLogin.as_view()),
]
