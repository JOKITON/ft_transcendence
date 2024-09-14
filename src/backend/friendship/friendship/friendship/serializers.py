from django.contrib.auth import get_user_model
from django.db.models.base import ModelBase
from friendship.models import Friendship
from rest_framework import serializers
from typing import List, Dict, Any, Type

User: Type[ModelBase] = get_user_model()

"""
cojemos los dos usuarios el usuario que hace la peticion y al usuario que se invita en la amistad
"""


class InviteFriendSerializer(serializers.Serializer):
    friend = serializers.CharField(max_length=50)

    class Meta:
        model: Type[ModelBase] = Friendship
        fields: List[str] = ["friend"]

    """
     aqui se obtiene el usuario que se quiere invitar
     deberia comprobar que el usuario que se invita existe
    """

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user = self.context["request"].user
            friend = User.objects.get(username=attrs.get("friend"))
            if friend.username == user.username:
                raise serializers.ValidationError(
                    "No te puedes invitar a ti mismo")
            elif Friendship.objects.filter(user=user, friend=friend).exists():
                raise serializers.ValidationError("Ya son amigos")
        except Exception as e:
            raise serializers.ValidationError(
                f"Usuario con username '{e}' no existe.")
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Friendship:
        user = self.context["request"].user
        friend = User.objects.get(username=validated_data.get("friend"))
        return Friendship.objects.create(user=user, friend=friend)
