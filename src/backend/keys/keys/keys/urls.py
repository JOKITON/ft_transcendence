from django.urls import path
from .views import KeyView

urlspatterns = [
    path("public", KeyView.as_view()),
    path("private", KeyView.as_view()),
]
