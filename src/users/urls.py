from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from users.api import users

urlpatterns = [
    path("", users.UserRegistration.as_view()),
]
