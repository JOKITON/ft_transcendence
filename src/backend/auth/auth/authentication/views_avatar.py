import base64
import os

from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


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