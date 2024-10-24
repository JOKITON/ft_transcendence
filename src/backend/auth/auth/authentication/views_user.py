from typing import Type

from django.contrib.auth import get_user_model
from django.db.models.base import ModelBase
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView, Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from UserModel.models import User

from .serializers import PasswdSerializer
from .serializers import UserDataSerializer
from .serializers import GetUserByIdSerializer
from .serializers import GetUsersSerializer

User: Type[ModelBase] = get_user_model()

class GetUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        query = request.GET.get('q', '')
        serializer = GetUsersSerializer(data={'query': query}, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            user_list = serializer.get_users()
            return Response({"user_list": user_list}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetUserById(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id: int) -> Response:
        serializer = GetUserByIdSerializer(data={'user_id': user_id}, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            user_data = serializer.get_user_data()
            return Response({"user_data": user_data}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdatePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswdSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"Error al actualizar la contraseña"}, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserDataSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User data updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"los datos no pueden repetirse con el de otro usuario"}, status=status.HTTP_400_BAD_REQUEST)
