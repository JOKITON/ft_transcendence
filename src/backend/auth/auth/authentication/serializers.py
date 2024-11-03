from django.contrib.auth.hashers import check_password, make_password
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate
from django.db.models.base import ModelBase
from rest_framework import serializers
from UserModel.models import User
from typing import List
import base64
import re
import os


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
        fields: List = ["username", "password", "email", "nickname", "avatar"]

    def validate(self, attrs) -> dict:
        username = attrs.get("username")
        if User.objects.filter(username=username):
            raise serializers.ValidationError({"username": "Username already in use."})
        nickname = attrs.get("nickname")
        if User.objects.filter(nickname=nickname):
            raise serializers.ValidationError({"nickname": "nickname already in use."})
        email = attrs.get("email")
        if User.objects.filter(email=email):
            raise serializers.ValidationError({"email": "email already in use."})
        return attrs

    def create(self, validated_data) -> User | serializers.ValidationError:
        user: User = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            ip=self.context["request"].META.get("REMOTE_ADDR"),
            ip_last_login=self.context["request"].META.get("REMOTE_ADDR"),
            nickname=validated_data.get("nickname"),
            avatar=validated_data.get("avatar", "avatars/pepe.png"),
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
            user.ip_last_login = self.context["request"].META.get("REMOTE_ADDR")
            user.status = True
            user.save()
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class UserDataSerializer(serializers.Serializer):
    newUsername: serializers.CharField = serializers.CharField(required=True)
    newNickname: serializers.CharField = serializers.CharField(required=True)
    newEmail: serializers.CharField = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context["request"].user

        newUsername = attrs.get("newUsername")
        if newUsername:
            if User.objects.filter(username=newUsername).exclude(id=user.id).exists():
                raise serializers.ValidationError(
                    {"username": "Username already in use."}
                )

        newNickname = attrs.get("newNickname")
        if newNickname:
            if User.objects.filter(nickname=newNickname).exclude(id=user.id).exists():
                raise serializers.ValidationError(
                    {"nickname": "Nickname already in use."}
                )

        newEmail = attrs.get("newEmail")
        if newEmail:
            if User.objects.filter(email=newEmail).exclude(id=user.id).exists():
                raise serializers.ValidationError({"email": "Email already in use."})

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user

        user.username = self.validated_data.get("newUsername", user.username)
        user.nickname = self.validated_data.get("newNickname", user.nickname)
        user.email = self.validated_data.get("newEmail", user.email)

        user.save()
        return user


class PasswdSerializer(serializers.Serializer):
    currentPassword: serializers.CharField = serializers.CharField(required=True)
    newPassword: serializers.CharField = serializers.CharField(required=True)
    confirmPassword: serializers.CharField = serializers.CharField(required=True)

    class Meta:
        model: ModelBase = User
        fields: List = ["currentPasswd", "newPasswd", "confirmPasswd"]

    def validate(self, attrs):
        user = self.context["request"].user

        # Obtener los campos de la solicitud
        current_password = attrs.get("currentPassword")
        new_password = attrs.get("newPassword")
        confirm_password = attrs.get("confirmPassword")

        # Validar que todos los campos estén presentes
        if not current_password or not new_password or not confirm_password:
            raise serializers.ValidationError(
                {"error": "All fields need to be validate."}
            )

        # Verificar que la contraseña actual sea correcta
        if not check_password(current_password, user.password):
            raise serializers.ValidationError(
                {"currentPassword": "Current password is incorrect."}
            )

        # Verificar que la nueva contraseña y su confirmación coincidan
        if new_password != confirm_password:
            raise serializers.ValidationError(
                {"confirmPassword": "The two password fields didn’t match."}
            )

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        new_password = self.validated_data["newPassword"]
        user.password = make_password(new_password)
        user.save()
        return user


class GetUsersSerializer(serializers.Serializer):
    query = serializers.CharField(required=True)

    def validate_query(self, value):
        if not re.match(r"^[\w\s]+$", value):
            raise serializers.ValidationError(
                "La consulta solo puede contener letras, números y espacios."
            )
        return value

    def get_users(self):
        user = self.context["request"].user
        query = self.validated_data.get("query", "")

        users = User.objects.filter(username__icontains=query).exclude(id=user.id)

        user_list = []
        for user in users:
            user_list.append({"id": user.id, "username": user.username})

        return user_list


class GetUserByIdSerializer(serializers.Serializer):
    user_id: serializers.IntegerField = serializers.IntegerField(required=True)

    def validate_user_id(self, value):
        authenticated_user = self.context["request"].user
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Usuario no encontrado")
        if value == authenticated_user.id:
            raise serializers.ValidationError("No puedes usar tu propio ID.")
        return value

    def get_user_data(self):
        user_id = self.validated_data.get("user_id")
        user = User.objects.get(id=user_id)
        return {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "email": user.email,
            "avatar": str(user.avatar),
        }


class UpdateAvatarSerializer(serializers.Serializer):
    image: serializers.ImageField = serializers.ImageField(required=True)

    def validate_image(self, image):
        valid_mime_types = ["image/jpeg", "image/png", "image/jpg"]
        if image.content_type not in valid_mime_types:
            raise serializers.ValidationError("Unsupported file type.")
        if image.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "File too large. Size should not exceed 5 MB."
            )

        if os.path.exists(f"avatars/{image.name}"):
            raise serializers.ValidationError("Avatar with this name already exists.")

        return image

    def save(self, user):
        image = self.validated_data["image"]

        filename = default_storage.save(f"avatars/{image.name}", image)
        user.avatar = filename
        user.save()

        return user


class GetAvatarSerializer(serializers.Serializer):
    avatar = serializers.CharField(read_only=True)

    def get_avatar(self):
        user = self.context["user"]

        if user.avatar:
            avatar_path = user.avatar.path
            if os.path.exists(avatar_path):
                with open(avatar_path, "rb") as avatar_file:
                    return {
                        "avatar_base64": base64.b64encode(avatar_file.read()).decode(
                            "utf-8"
                        )
                    }
            else:
                raise serializers.ValidationError("Avatar file does not exist.")
        else:
            raise serializers.ValidationError("User has no avatar.")

