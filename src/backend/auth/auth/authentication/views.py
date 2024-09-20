from rest_framework_simplejwt.tokens import (
    AccessToken,
    RefreshToken,
    Token,
)
from .serializers import (
    UserSerializerRegister,
    UserSerializer,
    PasswdSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Request
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django.core.files.base import ContentFile
from typing import Dict, Any
from UserModel.models import User
import logging, os, base64

logger: logging.Logger = logging.getLogger(__name__)

class RegisterUserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializerRegister(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            # Check if the user already exists
            user_data = serializer.validated_data
            if User.objects.filter(username=user_data['username']).exists():  # Check based on unique field
                return Response(
                    {
                        "message": "Username is not available.",
                        "code": "user_exists",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if User.objects.filter(nickname=user_data['nickname']).exists():  # Check based on unique field
                return Response(
                    {
                        "message": "Nickname is not available.",
                        "code": "nickname_exists",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
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
                "code": "unexpected",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginUserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data, context={"request": request})
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
            # print('Avatar url: ')
            # print(user.avatar.url)
            # print(user.avatar)
            # avatar_url = request.build_absolute_uri(user.avatar.url) if user.avatar else None
            avatar_url = user.avatar if user.avatar else f'{settings.MEDIA_URL}avatars/default_avatar.png'
            # print(avatar_url)
            user_data = {
                "username": user.username,
                "email": user.email,
                "nickname": user.nickname,
                "avatar": str(avatar_url),
                # Agrega aquí otros campos que desees mostrar
            }
            return Response(user_data, status=status.HTTP_200_OK)

class GetUserAvatarView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user

        # Check if the user has an avatar
        if user.avatar:
            avatar_path = user.avatar.path
            if os.path.exists(avatar_path):
                with open(avatar_path, 'rb') as avatar_file:
                    encoded_image = base64.b64encode(avatar_file.read()).decode('utf-8')
                    return Response({"avatar_base64": encoded_image}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Avatar file does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "User has no avatar"}, status=status.HTTP_404_NOT_FOUND)

class PublicKeyView(APIView):
    def get(self, request: Request) -> Response:
        try:
            with open("/auth/secrets/public.pem", "r") as f:
                public_key: str = f.read()
                print(public_key)
            return HttpResponse(public_key, content_type="text/plain")
        except Exception as e:
            return Response(
                {"Error": f"retrieving public key {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

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

""" class ImageView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    print('Pasando por la vista de la imagen')
    def get(self, request, format=None) -> Response:
        user = request.user
        print(user.avatar)
        file_path = os.path.join(settings.MEDIA_ROOT, str(user.avatar))
        print(file_path)
        if not os.path.exists(file_path):
            return Response(
               {"detail": "Imagen no carga"}, status=status.HTTP_400_BAD_REQUEST
            )
        print('Pasando por la vista de la imagen2')
        # Devuelve la respuesta con el archivo
        response = FileResponse(open(file_path, 'rb'))
        
        return response """

from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage

def validate_file(file):
    valid_mime_types = ['image/jpeg', 'image/png', 'image/jpg']
    if file.content_type not in valid_mime_types:
        raise ValidationError('Unsupported file type.')
    if file.size > 5 * 1024 * 1024:  # 5 MB limit
        raise ValidationError('File too large. Size should not exceed 5 MB.')

class UpdateUserAvatarView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.FILES)
        user = request.user
        file = request.FILES.get('image')

        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_file(file)
            if os.path.exists(f'avatars/{file.name}'):
                return Response({"error": 'Avatar already exists in our database'}, status=status.HTTP_400_BAD_REQUEST);
            filename = default_storage.save(f'avatars/{file.name}', file)
            user.avatar = filename
            user.save()
            return Response({"message": "Avatar updated successfully"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



""" class UploadImage(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None) -> Response:
        serializer = AvatarSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            # Save the form and store the image
            user = serializer.save()
            if user:
                response: Dict = {
                    "message": "Avatar uploaded successfully",
                    "status": status.HTTP_201_CREATED,
                }
                return Response(response, status=status.HTTP_201_CREATED)
        return Response(
            {
                "message": "Avatar not uploaded",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
 """