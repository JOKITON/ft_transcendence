from django.contrib import admin
from django.urls import path
from LiveGameSession import urls
from django.urls import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1", include(urls.urls_patterns)),
]
