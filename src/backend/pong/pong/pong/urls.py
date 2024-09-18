from django.urls import path
from .views import (
    TournamentAIView,
    Tournament2PView,
    Tournament8P
)

urlpatterns = [
    path("ai", TournamentAIView.as_view(), name="all-users"),
    path("2p", Tournament2PView.as_view(), name="all-users"),
    path("8p", Tournament8P.as_view(), name="all-users"),
]
