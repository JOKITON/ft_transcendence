from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import register_view, login_view  # Adjust according to your view

urlpatterns = [
    path('', views.index),
	path('home', views.index),
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
