from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import (
    RegisterUserView,
    LoginUserView,
    LogoutView,
    UpdateUserProfileView,
    # TokenRefreshView,
    WhoAmIView,
    # TokenVerifyView,
)

urlpatterns = [
    path("register", RegisterUserView.as_view(), name="register"),
    path("login", LoginUserView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("whoami", WhoAmIView.as_view(), name="whoami"),
    path('api/update-profile/', UpdateUserProfileView.as_view(), name='update_profile'),
    path("token/refresh", TokenRefreshView.as_view(), name="tokenRefresh"),
    path("token/verify", TokenVerifyView.as_view(), name="tokenVerify"),
]
