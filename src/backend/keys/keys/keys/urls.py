from django.urls import path
from .views import PublicKeyView, PrivateKeyView

urlpatterns = [
    path("public", PublicKeyView.as_view(), name="public"),
    path("private", PrivateKeyView.as_view(), name="private"),
]
