from rest_framework_simplejwt.tokens import (
    RefreshToken,
    Token,
)
from .serializers import (
    UserSerializerRegister,
    UserSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Request
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework import status
from UserModel.models import User
from typing import Dict, Any


class RegisterUserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializerRegister(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            valid = serializer.save()
            if valid:
                response: Dict[str, Any] = {
                    "message": "User created successfully",
                    "status": status.HTTP_201_CREATED,
                }
                return Response(response, status=status.HTTP_201_CREATED)

        return Response(
            {
                "message": "User not created",
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


class WhoAmIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user: User = request.user
        if user.is_authenticated:
            return Response({"username": user.username}, status=status.HTTP_200_OK)

        return Response(
            {"error": "User is not authenticated"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        username: str = request.data.get("user")
        old_password: str = request.data.get("old_password")
        new_password: str = request.data.get("new_password")

        if not username or not old_password or not new_password:
            return Response(
                {
                    "message": "Username, old password, and new password are required",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        elif request.user.username != username:
            return Response(
                {"message": "You can only change your own password", "status": "error"},
                status=status.HTTP_403_FORBIDDEN,
            )

        elif new_password == old_password:
            return Response(
                {
                    "message": "The new password cannot be the same as the old password",
                    "status": "error",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        elif not request.user.check_password(old_password):
            return Response(
                {"message": "Old password is incorrect", "status": "error"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(new_password)
        request.user.save()

        return Response(
            {"message": "Password changed successfully", "status": "success"},
            status=status.HTTP_200_OK,
        )


class PublicKeyView(APIView):
    def get(self, request: Request) -> Response:
        try:
            with open("/authentication/secrets/public.pem", "r") as f:
                public_key: str = f.read()
            return Response({"public": public_key}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"Error": f"retrieving public key {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
