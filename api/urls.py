from django.urls import path
from .views import (
    HelloView,
    RegisterView,
    LoginView,
    LogoutView,
    MessageListCreateView,
    CurrentMemberView
)

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("messages/", MessageListCreateView.as_view(), name="messages"),
    path("members/me/", CurrentMemberView.as_view(), name="current-member"),
]
