from django.urls import path, re_path
from .csrf import get_csrf, check_csrf_token, ProxyView

urlpatterns = [
    path('csrf/', get_csrf, name='api-csrf'),
    path('csrf/check/', check_csrf_token, name='api-csrf-check'),
    re_path(r'^api/.*$', ProxyView.as_view(), name='api-proxy'),
]
