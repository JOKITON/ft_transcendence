from django.urls import path
from . import views

urlpatterns = [
    path('/api/register', views.register_view, name='register'),
    path('/api/login', views.login_view, name='login'),
    # Add more API endpoints as needed
]