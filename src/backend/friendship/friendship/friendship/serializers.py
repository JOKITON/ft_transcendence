from django.contrib.auth import get_user_model
from django.db.models.base import ModelBase
from friendship.models import Friendship
from rest_framework import serializers
from typing import List, Dict, Any, Type

User: Type[ModelBase] = get_user_model()


class InviteFriendSerializer(serializers.Serializer):
    friend = serializers.CharField(max_length=50)

    class Meta:
        model: Type[ModelBase] = Friendship
        fields: List[str] = ["friend"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user = self.context["request"].user
            friend = User.objects.get(username=attrs.get("friend"))
            if friend.username == user.username:
                raise serializers.ValidationError("No te puedes invitar a ti mismo")
            elif Friendship.objects.filter(user=user, friend=friend).exists():
                raise serializers.ValidationError("Ya son amigos")
        except Exception as e:
            raise serializers.ValidationError(f"Usuario con username '{e}' no existe.")
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Friendship:
        user = self.context["request"].user
        friend = User.objects.get(username=validated_data.get("friend"))
        return Friendship.objects.create(user=user, friend=friend)


"""
la cosa seria recibir el status de la solicitud, y quien se la envio
con el estado, sabremos si la quiere aceptar, denegar o bloquear,
y el friend seria quien nos envio la solicitud
"""


class InviteStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=50)
    friend = serializers.CharField(max_length=50, Choices=Friendship.status)

    class Meta:
        model: Type[ModelBase] = Friendship
        fields: List[str] = ["friend", "status"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user = self.context["request"].user
            friend = User.objects.get(username=attrs.get("friend"))

            if not friend:
                raise serializers.ValidationError(f"friend not exist {friend.username}")
            friends = Friendship.objects.get(user=user, friend=friend)
            if not friends:
                raise serializers.ValidationError(
                    f"la  amistad entre {user.username} y {friend.username}"
                )
        except Exception as e:
            raise serializers.ValidationError(
                f"error en la validacion del estado de la invitacion {e}"
            )
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        user = self.context["request"].user
        friend = User.objects.get(username=attrs.get("friend"))
        friends = Friendship.objects.get(user=user, friend=friend)

        friends.status = attrs.get("status")
        friends.save()
        return validated_data
