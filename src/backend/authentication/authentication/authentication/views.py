from sys import exception
from rest_framework_simplejwt.tokens import (
    AccessToken,
    RefreshToken,
    Token,
)
from .serializers import (
    UserSerializerRegister,
    UserSerializerLogin,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework import status
from typing import Dict
import logging


logger: logging.Logger = logging.getLogger(__name__)


class RegisterUserView(APIView):
    def post(self, request) -> Response:
        serializer = UserSerializerRegister(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = serializer.save()
            if user:
                response: Dict = {
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
    def post(self, request) -> Response:
        serializer = UserSerializerLogin(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            refresh: Token = RefreshToken.for_user(user)
            access_token: str = str(refresh.access_token)
            refresh_token: str = str(refresh)
            response: Dict = {
                "message": f"User {user.username} logged in successfully",
                "status": status.HTTP_200_OK,
                "token": {
                    "accessToken": access_token,
                    "refreshToken": refresh_token,
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

    def post(self, request) -> Response:
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Blacklist the refresh token if using blacklist strategy
        try:
            refresh_token = request.data.get("refreshToken")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info(f"Refresh token {refresh_token} blacklisted successfully.")
        except Exception as e:
            logger.error(f"Error blacklisting token: {e}")
            return Response(
                {"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )
        # Perform the logout
        logout(request)
        response = Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )

        return response


class SessionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response({"isAuthenticated": True}, status=status.HTTP_200_OK)


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
            return Response({"username": user.username}, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        username = data.get("user")
        old_password = data.get("old_password")
        new_password = data.get("new_password")

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


class TokenVerifyView(APIView):
    def post(self, request) -> Response:
        serializer = TokenVerifySerializer(data=request.data)

        if not serializer.is_valid():
            print("no paso que no paso que paso")
            return Response(
                {"message": "request no valid", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )

        print("paso que paso")
        token = serializer.validated_data.get("token")
        try:
            print(token)
            token = AccessToken(token)
            token.verify()
            return Response(
                {"message": "Token is valid", "status": status.HTTP_200_OK},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return Response(
                {"message": "Token is invalid", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TokenRefreshView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refreshToken")
            if not refresh_token:
                return Response(
                    {
                        "detail": "Refresh token is required",
                        status: status.HTTP_400_BAD_REQUEST,
                        "permitid": 0,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)
            new_token = token.access_token
            return Response(
                {"accessToken": str(new_token), "refreshToken": str(new_token)},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return Response(
                {
                    "detail": "Refresh token is required",
                    status: status.HTTP_400_BAD_REQUEST,
                    "permitid": 0,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
