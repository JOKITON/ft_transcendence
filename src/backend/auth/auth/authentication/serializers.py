from django.db.models.base import ModelBase
from django.contrib.auth import authenticate
from rest_framework import serializers
from typing import List
from .models import User
from django.contrib.auth.hashers import check_password, make_password
import logging

logger = logging.getLogger(__name__)

class UserSerializerRegister(serializers.ModelSerializer):
    username: serializers.CharField = serializers.CharField(required=True)
    password: serializers.CharField = serializers.CharField(required=True)
    email: serializers.EmailField = serializers.EmailField(required=True)
    nickname: serializers.CharField = serializers.CharField(required=False)

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
    username: serializers.CharField = serializers.CharField(required=True)
    password: serializers.CharField = serializers.CharField(required=True)

    def validate(self, attrs) -> User:
        user = authenticate(
            username=attrs.get("username"), password=attrs.get("password")
        )
        if user is not None and user.is_active:
            user.ip_last_login = self.context["request"].META.get("REMOTE_ADDR")
            user.save()
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class TokenVerifySerializer(serializers.Serializer):
    token: serializers.CharField = serializers.CharField(required=True)

    def validate(self, attrs) -> dict:
        return attrs

class PasswdSerializer(serializers.Serializer):
    currentPassword: serializers.CharField = serializers.CharField(required=True)
    newPassword: serializers.CharField = serializers.CharField(required=True)
    confirmPassword: serializers.CharField = serializers.CharField(required=True)

    class Meta:
        model: ModelBase = User
        fields: List = ["currentPasswd", "newPasswd", "confirmPasswd"]

    def validate(self, attrs):
        #
        print(attrs)
        user = self.context['request'].user
        print(self.context['request'])

        # Obtener los campos de la solicitud
        current_password = attrs.get('currentPassword')
        new_password = attrs.get('newPassword')
        confirm_password = attrs.get('confirmPassword')

        # Validar que todos los campos estén presentes
        if not current_password or not new_password or not confirm_password:
            raise serializers.ValidationError({"currentPassword": "Current password is incorrect."})

        # Verificar que la contraseña actual sea correcta
        if not check_password(current_password, user.password):
            raise serializers.ValidationError({"confirmPassword": "New passwords do not match."})

        # Verificar que la nueva contraseña y su confirmación coincidan
        if new_password != confirm_password:
            raise serializers.ValidationError({"newPassword": "New password must be at least 8 characters long."})

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['newPassword']
        user.password = make_password(new_password)
        user.save()
        return user