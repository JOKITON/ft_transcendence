from django.urls import path
from .auth import PublicKeyView, PrivateKeyView

urlpatterns = [
    path('key/public-key/', PublicKeyView.as_view(), name='public_key'),
    path('key/private-key/', PrivateKeyView.as_view(), name='private_key'),
]
