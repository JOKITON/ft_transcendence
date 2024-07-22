from rest_framework import viewsets
from .models import round
from .serializers import RoundSerializer


class RoundViewSet(viewsets.ModelViewSet):
    queryset = round.objects.all()
    serializer_class = RoundSerializer
