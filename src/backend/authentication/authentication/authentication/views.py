from .serializers import UserSerializerRegister, UserSerializerLogin
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from typing import Dict
from .models import User
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
                }
                return Response(response, status=status.HTTP_201_CREATED)
        print(f"serializer.errors ->: {serializer.errors}, {serializer}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    def post(self, request) -> Response:
        serializer = UserSerializerLogin(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user = serializer.validated_data

            refresh = RefreshToken.for_user(user)
            access_token: str = str(refresh.access_token)
            refresh_token: str = str(refresh)
            response: Dict = {
                "access": access_token,
                "refresh": refresh_token,
                "message": "User logged in successfully",
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserSerializerRegister
