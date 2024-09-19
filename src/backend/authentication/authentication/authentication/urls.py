from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    LogoutView,
    WhoAmIView,
    PublicKeyView,
    GetUsers,
)

urlpatterns = [
    path("register", RegisterUserView.as_view(), name="register"),
    path("login", LoginUserView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("whoami", WhoAmIView.as_view(), name="whoami"),
    path("token/refresh", TokenRefreshView.as_view(), name="tokenRefresh"),
    path("token/verify", TokenVerifyView.as_view(), name="tokenVerify"),
    path("public", PublicKeyView.as_view(), name="public"),
    path("search-users", GetUsers.as_view(), name="users"),
]
