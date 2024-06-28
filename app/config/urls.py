from django.contrib import admin
from django.urls import include, path
from home.views import register_view  # Adjust based on your view function

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Include home app URLs
	path('api/register', register_view, name='api_register'),
]
