from django.urls import path
from .views import (
    TournamentAI,
    Tournament2P,
    Tournament8P
)

urlpatterns = [
    path("ai", TournamentAI.as_view(), name="all-users"),
    path("2p", Tournament2P.as_view(), name="all-users"),
    path("tournament", Tournament8P.as_view(), name="all-users"),
]
