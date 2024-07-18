from rest_framework import serializers
from .models import round


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = round
        fields = "__all__"
