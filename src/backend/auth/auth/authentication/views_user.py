from typing import Type

from django.contrib.auth import get_user_model
from django.db.models.base import ModelBase
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView, Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from UserModel.models import User

from .serializers import PasswdSerializer
from .serializers import UserDataSerializer

User: Type[ModelBase] = get_user_model()
class GetUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        query = request.GET.get('q', '')
        users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)  # Busca usuarios que coincidan
        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "username": user.username
            })
        print(user_list)
        return Response({"user_list": user_list}, status=status.HTTP_200_OK)

class GetUserById(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id: int) -> Response:
        try:
            # Busca el usuario por su ID
            user = User.objects.get(id=user_id)
            # Crea el diccionario con los datos del usuario
            user_data = {
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "email": user.email,
                "avatar": str(user.avatar),
            }
            return Response({"user_data": user_data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

class UpdatePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Pasar los datos de la solicitud al serializador
        serializer = PasswdSerializer(data=request.data, context={"request": request})

        # Validar los datos
        if serializer.is_valid():
            # Guardar la nueva contraseña
            serializer.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        else:
            # Devolver errores de validación
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

""" class ChangePassword(APIView):
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
        ) """