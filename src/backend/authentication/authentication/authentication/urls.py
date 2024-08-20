from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import (
    RegisterUserView,
    LoginUserView,
    LogoutView,
    # TokenRefreshView,
    # TokenVerifyView,
)

urlpatterns = [
    path("register", RegisterUserView.as_view(), name="register"),
    path("login", LoginUserView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("token/refresh", TokenRefreshView.as_view(), name="tokenRefresh"),
    path("token/verify", TokenVerifyView.as_view(), name="tokenVerify"),
]
