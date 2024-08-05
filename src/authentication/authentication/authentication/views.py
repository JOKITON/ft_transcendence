from rest_framework_simplejwt.tokens import RefreshToken
import logging
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

logger = logging.getLogger(__name__)


class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(
            data=request.data, context={"request": request})

        if serializer.is_valid():
            user = serializer.save()

            # Generar tokens
            # refresh = RefreshToken.for_user(user)
            # access_token = str(refresh.access_token)
            # refresh_token = str(refresh)
            response = {
                "message": "User created successfully",
            }
            logger.info(f"User {user.username} created")
            return Response(response, status=status.HTTP_201_CREATED)
            logger.error(f"Error creating user {user.username}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserSerializer
