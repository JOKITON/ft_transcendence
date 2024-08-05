from . import views
from django.urls import path

urlpatterns = [
    path(
        "rounds/", views.RoundViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "rounds/<int:pk>/",
        views.RoundViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
]
