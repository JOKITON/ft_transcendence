from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import (
    RegisterUserView,
    LoginUserView,
    LogoutView,
    UpdateUserProfileView,
    UpdateUserPasswordView,
    WhoAmIView,
    # TokenRefreshView,
    # TokenVerifyView,
)

urlpatterns = [
    path("register", RegisterUserView.as_view(), name="register"),
    path("login", LoginUserView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("whoami", WhoAmIView.as_view(), name="whoami"),
    path("token/refresh", TokenRefreshView.as_view(), name="tokenRefresh"),
    path("token/verify", TokenVerifyView.as_view(), name="tokenVerify"),

    # MOVIDAS DE USUARIOS
    path('update-profile', UpdateUserProfileView.as_view(), name='update_profile'),
    path('change-password', UpdateUserPasswordView.as_view(), name='update_password'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
