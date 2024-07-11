from django.urls import path
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.middleware.csrf import get_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('api/register/', views.RegisterView.as_view(), name='api-register'),
    path('api/login/', views.LoginView.as_view(), name='api-login'),
	path('api/csrf/', views.get_csrf, name='api-csrf'),
    path('api/csrf/check/', views.check_csrf_token, name='api-csrf-check'),
    path('api/logout/', views.LogoutView.as_view(), name='api-logout'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),

    path('api/session/', views.SessionView.as_view(), name='api-session'),  # new
    path('api/whoami/', views.WhoAmIView.as_view(), name='api-whoami'),  # new
]
