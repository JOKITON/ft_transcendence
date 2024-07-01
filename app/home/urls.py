from django.urls import path
from . import views

urlpatterns = [
    path('api/register', views.register_view, name='register'),
    path('api/login', views.login_view, name='login'),
	path('api/csrf-token', views.csrf_token_view, name='csrfToken'),
	path('api/logout', views.logout_view, name='logout'),
    # Add more API endpoints as needed
]