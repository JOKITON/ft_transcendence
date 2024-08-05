from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data) -> User:
        # de esta manera puedo sacar datos de la solicitud
        ip = self.context["request"].META.get("REMOTE_ADDR")
        # Create user instance
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            ip=ip,
            ip_last_login=ip,
        )
        return user
