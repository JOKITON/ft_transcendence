from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/register', views.register_view, name='register'),
    path('api/login', views.login_view, name='login'),
	path('api/csrf-token', views.csrf_token_view, name='csrfToken'),
	path('api/logout', views.logout_view, name='logout'),
	
    # AUTH
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Add more API endpoints as needed
]