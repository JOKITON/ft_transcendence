from django.urls import path
from .csrf import get_csrf, check_csrf_token

urlpatterns = [
    path('csrf/', get_csrf, name='api-csrf'),
    path('csrf/check/', check_csrf_token, name='api-csrf-check'),
]