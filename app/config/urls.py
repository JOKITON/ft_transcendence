from django.contrib import admin
from django.urls import include, path

from home.views import index

urlpatterns = [
    path('admin/', index),
    path('', index),
]
