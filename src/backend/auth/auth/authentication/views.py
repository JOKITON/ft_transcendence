from .serializers import UserSerializer, UserSerializerRegister
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Request
from django.contrib.auth import login, logout
from rest_framework.response import Response
from django.http import HttpResponse
from UserModel.models import User
from rest_framework import status
from django.conf import settings
from typing import Any, Dict


class RegisterUserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializerRegister(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user_data = serializer.validated_data
            if User.objects.filter(
                username=user_data["username"]
            ).exists():  # Check based on unique field
                return Response(
                    {
                        "message": "Username is not available.",
                        "code": "user_exists",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if User.objects.filter(
                nickname=user_data["nickname"]
            ).exists():  # Check based on unique field
                return Response(
                    {
                        "message": "Nickname is not available.",
                        "code": "nickname_exists",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if User.objects.filter(
                email=user_data["email"]
            ).exists():  # Check based on unique field
                return Response(
                    {
                        "message": "Email is not available.",
                        "code": "email_exists",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            valid = serializer.save()
            if valid:
                response: Dict[str, Any] = {
                    "message": "User created successfully",
                    "id": valid.id,
                    "status": status.HTTP_201_CREATED,
                }
                return Response(response, status=status.HTTP_201_CREATED)
        return Response(
            {
                "message": "User not created, error occurred.",
                "code": "unexpected",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginUserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            user: User = serializer.validated_data
            login(request, user)
            refresh_token: Token = RefreshToken.for_user(user)
            access: str = str(refresh_token.access_token)
            refresh: str = str(refresh_token)
            response: Dict[str, Any] = {
                "message": f"User {user.username} logged in successfully",
                "status": status.HTTP_200_OK,
                "token": {
                    "access": access,
                    "refresh": refresh,
                },
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "message": "Invalid credentials",
                    "status": status.HTTP_400_BAD_REQUEST,
                    "token": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        try:
            user: User = request.user
            user.status = False
            user.save()
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            logout(request)
            return Response(
                {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": f"Invalid token {e}"}, status=status.HTTP_400_BAD_REQUEST
            )


class SessionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response({"isAuthenticated": True}, status=status.HTTP_200_OK)


class IAm(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None) -> Response:
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            user_data = {"username": user.username}
            return Response(user_data, status=status.HTTP_200_OK)


class WhoAmIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None) -> Response:
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            avatar_url = (
                user.avatar
                if user.avatar
                else f"{settings.MEDIA_URL}avatars/default_avatar.png"
            )
            user_data = {
                "username": user.username,
                "email": user.email,
                "nickname": user.nickname,
                "avatar": str(avatar_url),
                "id": user.id,
            }
            return Response(user_data, status=status.HTTP_200_OK)


class PublicKeyView(APIView):
    def get(self, request: Request) -> Response:
        try:
            with open("/auth/secrets/public.pem", "r") as f:
                public_key: str = f.read()
            return HttpResponse(public_key, content_type="text/plain")
        except Exception as e:
            return Response(
                {"Error": f"retrieving public key {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
