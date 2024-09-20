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

User: Type[ModelBase] = get_user_model()
class GetUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        query = request.GET.get('q', '')
        users = User.objects.filter(username__icontains=query)  # Busca usuarios que coincidan
        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "username": user.username
            })
        print(user_list)
        return Response({"user_list": user_list}, status=status.HTTP_200_OK)

class GetUsersId(APIView):
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
                "email": user.email,  # Añade más información si es necesario
            }
            return Response({"user_data": user_data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
# Santi
class UpdateUserPasswordView(APIView):
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

class UpdateUserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        # Obtener los campos que se van a actualizar
        new_email = data.get('email', None)
        new_full_name = data.get('username', None)
        new_nickname = data.get('nickname', None)
        new_mobile = data.get('mobile', None)
        new_address = data.get('address', None)

        print("llega aqui")
        # Validar si el email ya existe
        if new_email and User.objects.filter(email=new_email).exclude(id=user.id).exists():
            return Response({"error": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)

        print("llega aqui2")
        print(new_full_name)
        print("aaaaa")
        # Actualizar los campos del usuario si están presentes en la petición
        if new_email:
            user.email = new_email
        if new_full_name:
            user.username = new_full_name
        if new_nickname:
            user.nickname = new_nickname
        if new_mobile:
            user.mobile = new_mobile
        if new_address:
            user.address = new_address

        user.save()

        return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
