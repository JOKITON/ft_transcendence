from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    LogoutView,
    WhoAmIView,
    PublicKeyView,
    IAm,
    health_check,
)
from .views_user import (
    GetUsers,
    GetUserById,
    UpdateUserData,
    UpdatePassword,
    # ChangePassword,
)
from .views_avatar import (
    UpdateAvatar,
    GetAvatar,
    GetAvatarById,
)

urlpatterns = [
    path('health', health_check),    

    # General User Related
    path("register", RegisterUserView.as_view(), name="register"),
    path("login", LoginUserView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("whoami", WhoAmIView.as_view(), name="whoami"),
    path("iam", IAm.as_view(), name="iam"),
    # User Specific Related
    path("update-profile", UpdateUserData.as_view(), name="update_profile"),
    path("change-password", UpdatePassword.as_view(), name="update_password"),
    # path('change-password', ChangePassword.as_view(), name='update_password'),
    path("update-avatar", UpdateAvatar.as_view(), name="updateAvatar"),  # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    path("get-avatar", GetAvatar.as_view(), name="getAvatar"),
    path("get-avatar-id/<int:user_id>/",
         GetAvatarById.as_view(), name="getAvatarById"),
    # path('avatars2', ImageView.as_view(), name='image_view')
    path("search-users", GetUsers.as_view(), name="getUsers"),
    path("search-user-id/<int:user_id>/",
         GetUserById.as_view(), name="getUserById"),
    # Token & Key Related
    path("token/verify", TokenVerifyView.as_view(), name="tokenVerify"),
    path("token/refresh", TokenRefreshView.as_view(), name="tokenRefresh"),
    path("public", PublicKeyView.as_view(), name="public"),
]

""" from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) """
