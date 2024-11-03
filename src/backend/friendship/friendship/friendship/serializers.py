from django.contrib.auth import get_user_model
from django.db.models.base import ModelBase
from friendship.models import Friendship
from rest_framework import serializers
from typing import List, Dict, Any, Type
from django.db import models

User: Type[ModelBase] = get_user_model()


class InviteFriendSerializer(serializers.Serializer):
    friend = serializers.CharField(
        max_length=50,
        min_length=3,
        required=True,
        allow_blank=False,
        trim_whitespace=True,
    )

    class Meta:
        model: Type[ModelBase] = Friendship
        fields: List[str] = ["friend"]

    def create(self, validated_data: Dict[str, Any]) -> Friendship:
        user = self.context["request"].user
        try:
            friend = User.objects.get(username=validated_data["friend"])
        except User.DoesNotExist:
            raise serializers.ValidationError("El usuario no existe")
        return Friendship.objects.create(user=user, friend=friend)


class InviteStatusSerializer(serializers.Serializer):
    friend = serializers.CharField(
        max_length=50,
        min_length=3,
        required=True,
        allow_blank=False,
        trim_whitespace=True,
    )

    status = serializers.ChoiceField(
        choices=Friendship.STATUS_CHOICES, required=True)

    class Meta:
        model: Type[ModelBase] = Friendship
        fields: List[str] = ["friend", "status"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        user = self.context["request"].user
        try:
            friend = User.objects.get(username=attrs["friend"])
            friendship = Friendship.objects.get(user=user, friend=friend)
        except User.DoesNotExist:
            raise serializers.ValidationError("El usuario amigo no existe")
        except Friendship.DoesNotExist:
            raise serializers.ValidationError(
                "No existe una solicitud de amistad con este usuario"
            )
        return attrs

    def update(self, instance, validated_data: Dict[str, Any]) -> Friendship:
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


class DeleteFriendSerializer(serializers.ModelSerializer):
    friend = serializers.CharField(
        max_length=50,
        min_length=3,
        required=True,
        allow_blank=False,
        trim_whitespace=True,
    )

    class Meta:
        model: Type[ModelBase] = Friendship
        fields: List[str] = ["friend"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        user = self.context["request"].user
        try:
            friend = User.objects.get(username=attrs["friend"])
            friendship = Friendship.objects.get(user=user, friend=friend)
        except User.DoesNotExist:
            raise serializers.ValidationError("El usuario amigo no existe")
        except Friendship.DoesNotExist:
            raise serializers.ValidationError(
                "No existe una amistad con este usuario")
        return attrs

    def delete(self, validated_data: Dict[str, Any]) -> Friendship:
        user = self.context["request"].user
        try:
            friend = User.objects.get(username=validated_data["friend"])
            friendship = Friendship.objects.get(user=user, friend=friend)
            friendship.delete()
            return friendship
        except User.DoesNotExist:
            raise serializers.ValidationError("El usuario amigo no existe")
        except Friendship.DoesNotExist:
            raise serializers.ValidationError(
                "No existe una amistad con este usuario")


class FriendRequestSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ["id", "friend"]

    def get_friend(self, obj):
        return {"username": obj.user.username, "email": obj.user.email}


class FriendSerializer(serializers.ModelSerializer):
    is_blocked = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_blocked"]

    def get_is_blocked(self, obj):
        request_user = self.context["request"].user
        friendship = Friendship.objects.filter(
            models.Q(user=request_user, friend=obj)
            | models.Q(user=obj, friend=request_user),
            status=Friendship.BLOCKED,
        ).exists()

        return friendship


class NoDataAllowedSerializer(serializers.Serializer):
    def validate(self, data):
        if data:
            raise serializers.ValidationError(
                "No se permiten datos en esta vista.")
        return data


"""
class GetRoomSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ["id", "friend"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        user = self.context["request"].user
        try:
            friend = User.objects.get(username=attrs["friend"])
            friendship = Friendship.objects.get(user=user, friend=friend)
        except User.DoesNotExist:
            raise serializers.ValidationError("El usuario amigo no existe")
        except Friendship.DoesNotExist:
            raise serializers.ValidationError("No existe una amistad con este usuario")
        return attrs
"""
