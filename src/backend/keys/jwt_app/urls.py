from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .auth import CustomTokenRefreshView, PublicKeyView, PrivateKeyView

urlpatterns = [
    path('key/public-key/', PublicKeyView.as_view(), name='public_key'),
    path('key/private-key/', PrivateKeyView.as_view(), name='private_key'),
]