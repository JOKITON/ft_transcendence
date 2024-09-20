from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    LogoutView,
    UpdateUserProfileView,
    UpdateUserPasswordView,
    UpdateUserAvatarView,
    GetUserAvatarView,
    WhoAmIView,
    PublicKeyView,
)

urlpatterns = [
    path("register", RegisterUserView.as_view(), name="register"),
    path("login", LoginUserView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("whoami", WhoAmIView.as_view(), name="whoami"),

    # MOVIDAS DE USUARIOS
    path('update-profile', UpdateUserProfileView.as_view(), name='update_profile'),
    path('change-password', UpdateUserPasswordView.as_view(), name='update_password'),
    # path('avatars2', ImageView.as_view(), name='image_view')
    path('change-avatar', UpdateUserAvatarView.as_view(), name='update_avatar'), #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    path('get-avatar', GetUserAvatarView.as_view(), name='update_avatar'),
    
    path("token/verify", TokenVerifyView.as_view(), name="tokenVerify"),
    path("token/refresh", TokenRefreshView.as_view(), name="tokenRefresh"),
    path("public", PublicKeyView.as_view(), name="public"),
]

""" from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) """
