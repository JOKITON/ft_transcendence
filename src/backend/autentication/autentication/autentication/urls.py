from django.urls import path
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.middleware.csrf import get_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("register/", views.register_view, name="api-register"),
    path("login/", views.login_view, name="api-login"),
    path("csrf/", views.get_csrf, name="api-csrf"),
    path("logout/", views.logout_view, name="api-logout"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", views.refresh_token_view, name="token_refresh_from_cookie"),
    path("session/", views.SessionView.as_view(), name="api-session"),  # new
    path("whoami/", views.WhoAmIView.as_view(), name="api-whoami"),  # new
]
