from django.contrib.auth import get_user_model
from django.db.models.base import ModelBase
from friendship.models import Friendship
from rest_framework import serializers
from typing import List, Dict, Any, Type

User: Type[ModelBase] = get_user_model()

"""
This serializer is used to invite a friend to be a friend of the user.

Este serializador se utiliza para invitar a un amigo a ser amigo del usuario.
"""


class InviteFriendSerializer(serializers.Serializer):
    friend = serializers.CharField(
        max_length=50,
        min_length=3,
        required=True,
        allow_blank=False,
        allow_null=False,
        trim_whitespace=True,
    )

    class Meta:
        model: Type[ModelBase] = Friendship
        fields: List[str] = ["friend"]

    def create(self, validated_data: Dict[str, Any]) -> Friendship:
        user = self.context["request"].user
        friend = User.objects.get(username=validated_data.get("friend"))
        return Friendship.objects.create(user=user, friend=friend)


"""
This serializer is used to accept or deny a friend request.

Este serializador se utiliza para aceptar o denegar una solicitud de amistad.
"""


class InviteStatusSerializer(serializers.Serializer):
    friend = serializers.CharField(
        max_length=50,
        min_length=3,
        required=True,
        allow_blank=False,
        allow_null=False,
        trim_whitespace=True,
    )

    status = serializers.ChoiceField(
        choices=Friendship.STATUS_CHOICES, required=True)

    class Meta:
        model: Type[ModelBase] = Friendship
        fields: List[str] = ["friend", "status"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user = self.context["request"].user
            friend = User.objects.get(username=attrs.get("friend"))
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

    def create(self, validated_data: Dict[str, Any]) -> Friendship:
        user = self.context["request"].user
        friend = User.objects.get(username=validated_data.get("friend"))
        return Friendship.objects.get(user=user, friend=friend)


class FriendshipDeleteSerializers(serializers.ModelSerializer):
    friend = serializers.CharField(
        max_length=50,
        min_length=3,
        required=True,
        allow_blank=False,
        allow_null=False,
        trim_whitespace=True,
    )

    class Meta:
        model: Type[ModelBase] = Friendship
        fields: list[str] = ["friend"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user = self.context["request"].user
            friend = User.objects.get(username=attrs.get("friend"))
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

    def delete(self, validated_data: Dict[str, Any]) -> Friendship:
        user = self.context["request"].user
        friend = User.objects.get(username=validated_data.get("friend"))
        friends = Friendship.objects.get(user=user, friend=friend)
        friends.delete()
        return friends
