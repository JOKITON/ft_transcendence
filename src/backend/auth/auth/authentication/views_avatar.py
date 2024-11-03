
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from UserModel.models import User
from rest_framework import serializers

from .serializers import UpdateAvatarSerializer, GetAvatarSerializer

class GetAvatarById(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id: int) -> Response:
        serializer = GetAvatarSerializer(context={'user': User.objects.get(id=user_id)})
        
        try:
            avatar_data = serializer.get_avatar()
            return Response(avatar_data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetAvatar(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        serializer = GetAvatarSerializer(context={'user': request.user})
        
        try:
            avatar_data = serializer.get_avatar()
            return Response(avatar_data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateAvatar(APIView):


    def post(self, request):
        user = request.user
        serializer = UpdateAvatarSerializer(data=request.FILES)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response({"message": "Avatar updated successfully"}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
