from rest_framework import viewsets
from .models import Round
from .serializers import RoundSerializer

class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
