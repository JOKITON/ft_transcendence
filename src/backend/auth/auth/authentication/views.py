from rest_framework_simplejwt.tokens import (
    AccessToken,
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
from django.http import HttpResponse


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
                        "message": "User already exists",
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
            """ print('Avatar url: ')
            print(user.avatar.url)
            print(user.avatar) """
            #avatar_url = request.build_absolute_uri(user.avatar.url) if user.avatar else None
            #avatar_url = user.avatar.url if user.avatar else f'{settings.MEDIA_URL}avatars/default_avatar.png'
            user_data = {
                "username": user.username,
                "email": user.email,
                "nickname": user.nickname,
                #"avatar": str(avatar_url),
                # Agrega aquí otros campos que desees mostrar
            }
            return Response(user_data, status=status.HTTP_200_OK)

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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.files.storage import default_storage

""" class UpdateUserAvatarView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        file = request.FILES.get('avatar')

        if file:
            filename = default_storage.save(f'avatars/{user.id}/{file.name}', file)
            user.avatar = filename
            user.save()
            return Response({"message": "Avatar updated successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
 """
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

""" class ChangeUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, requst):
        data = request.data
        username = data.get("user") """

class TokenVerifyView(APIView):
    def post(self, request) -> Response:
        print(str(request.data) + " <-request.data")
        serializer = TokenVerifySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "message": "request no valid",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = serializer.validated_data.get("token")
            AccessToken(token)
            return Response(
                {"message": "Token is valid", "status": status.HTTP_200_OK},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return Response(
                {
                    "message": "Token not invalid",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


"""
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
"""


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
            with open("/auth/secrets/public.pem", "r") as f:
                public_key: str = f.read()
                print(public_key)
            return HttpResponse(public_key, content_type="text/plain")
        except Exception as e:
            return Response(
                {"Error": f"retrieving public key {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
