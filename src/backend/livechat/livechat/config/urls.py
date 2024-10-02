from django.contrib import admin
from django.urls import include
from django.urls import path
from livechat import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/livechat/", include(urls)),
]
