from rest_framework.serializers import ModelSerializer
from django.db.models.base import ModelBase
from rest_framework import serializers
from django.contrib.auth.models import User
from typing import List, Any, Dict
from .models import Room


class ChatSerializer(ModelSerializer):
    room_name = serializers.CharField(
        max_length=50,
        required=True,
        allow_blank=False,
        allow_null=False,
        trim_whitespace=True,
    )

    class Meta:
        model: ModelBase = Room
        fields: List[str] = ["room_name", "friend"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if Room.objects.filter(room_name=attrs["room_name"]).exists():
            raise serializers.ValidationError("Room already exists")
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Room:
        room = Room.objects.create(**validated_data)
        friend = User.objects.filter(username=validated_data["friend"])
        if not friend.exists():
            raise serializers.ValidationError("Friend not exists")
        room.online.add(self.context["request"].user)
        room.online.add(friend)
        return room


class RoomSerializer(ModelSerializer):
    room_name = serializers.CharField(
        max_length=50,
        required=True,
        allow_blank=False,
        allow_null=False,
        trim_whitespace=True,
    )
    users = serializers.ListField(
        child=serializers.CharField(
            max_length=50,
            required=True,
            allow_blank=False,
            allow_null=False,
            trim_whitespace=True,
        ),
        required=True,
    )

    class Meta:
        model: ModelBase = Room
        fields: List[str] = ["room_name", "users"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if Room.objects.filter(room_name=attrs["room_name"]).exists():
            raise serializers.ValidationError("Room already exists")
        if not User.objects.filter(username__in=attrs["users"]).exists():
            raise serializers.ValidationError("Users not exists")
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Room:
        room = Room.objects.create(**validated_data)
        room.online.add(self.context["request"].user)
        return room


class RoomDeleteSerializer(ModelSerializer):
    room_name = serializers.CharField(
        max_length=50,
        required=True,
        allow_blank=False,
        allow_null=False,
        trim_whitespace=True,
    )

    class Meta:
        model: ModelBase = Room
        fields: List[str] = ["room_name"]

    def validate(self, attrs: Dict[str, Any]) -> Room:
        room = Room.objects.filter(room_name=attrs["room_name"])
        if not room.exists():
            raise serializers.ValidationError("Room not exists")
        room.delete()
        return room
