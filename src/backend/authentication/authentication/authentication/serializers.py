from django.db.models.base import ModelBase
from django.contrib.auth import authenticate
from rest_framework import serializers
from UserModel.models import User
from typing import List
import logging

logger = logging.getLogger(__name__)


class UserSerializerRegister(serializers.ModelSerializer):
    username: serializers.CharField = serializers.CharField(
        required=True,
        max_length=50,
        min_length=5,
        allow_blank=False,
        allow_null=False,
        trim_whitespace=True,
        help_text="Username must be unique and have a length between 5 and 50 characters.",
    )

    password: serializers.CharField = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        max_length=50,
        allow_blank=False,
        allow_null=False,
        trim_whitespace=True,
        help_text="Password must have a length between 8 and 50 characters.",
    )

    email: serializers.EmailField = serializers.EmailField(
        required=True, help_text="Email must be unique."
    )

    nickname: serializers.CharField = serializers.CharField(
        required=True,
        min_length=3,
        max_length=50,
        allow_blank=True,
        allow_null=True,
        trim_whitespace=True,
        help_text="Nickname must have a length between 3 and 50 characters.",
    )

    class Meta:
        model: ModelBase = User
        fields: List = ["username", "password", "email", "nickname"]

    def create(self, validated_data) -> User | serializers.ValidationError:
        user: User = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            ip=self.context["request"].META.get("REMOTE_ADDR"),
            ip_last_login=self.context["request"].META.get("REMOTE_ADDR"),
            nickname=validated_data.get("nickname"),
        )
        return user


class UserSerializer(serializers.Serializer):
    username: serializers.CharField = serializers.CharField(
        required=True,
        max_length=50,
        min_length=5,
        allow_blank=False,
        allow_null=False,
        trim_whitespace=True,
    )
    password: serializers.CharField = serializers.CharField(
        required=True,
    )

    def validate(self, attrs) -> User:
        user: User = authenticate(
            username=attrs.get("username"), password=attrs.get("password")
        )
        if user is not None and user.is_active:
            user.ip_last_login = self.context["request"].META.get(
                "REMOTE_ADDR")
            user.status = True
            user.save()
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class TokenVerifySerializer(serializers.Serializer):
    token: serializers.CharField = serializers.CharField(required=True)

    def validate(self, attrs) -> dict:
        return attrs