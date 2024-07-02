from django.urls import path
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.middleware.csrf import get_token
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/register', views.register_view, name='register'),
    path('api/login', views.login_view, name='login'),
	path('api/logout', views.logout_view, name='logout'),

	path('api/csrf-token/check', views.check_csrf_token, name='checkCsrfToken'),
	path('api/csrf-token', views.csrf_token_view, name='csrfToken'),
	
	
    # AUTH
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/validate-token', views.validate_token_view, name='token_validate'),
    # Add more API endpoints as needed
]