from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer
import logging

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Registration successful',
                'user_id': user.id,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'message': 'Invalid data', 'errors': serializer.errors, 'status': 'error'},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # You may want to use Django's session authentication or JWT
            login(request, user)  # Sets session cookies

            # Generate JWT tokens if you're using JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'access': access_token,
                'refresh': refresh_token
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': 'Invalid credentials', 'errors': serializer.errors, 'status': 'error'},
                status=status.HTTP_400_BAD_REQUEST
            )

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        # Blacklist the refresh token if using blacklist strategy
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info(f'Refresh token {refresh_token} blacklisted successfully.')
        except Exception as e:
            logger.error(f'Error blacklisting token: {e}')
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform the logout
        logout(request)
        response = Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        
        return response


class SessionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response({'isAuthenticated': True})

class WhoAmIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user

        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'username': user.username})

class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        username = data.get('user')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not username or not old_password or not new_password:
            return Response(
                {'message': 'Username, old password, and new password are required', 'status': 'error'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.username != username:
            return Response({'message': 'You can only change your own password', 'status': 'error'}, status=status.HTTP_403_FORBIDDEN)

        if new_password == old_password:
            return Response({'message': 'The new password cannot be the same as the old password', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.check_password(old_password):
            return Response({'message': 'Old password is incorrect', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(new_password)
        request.user.save()

        return Response({'message': 'Password changed successfully', 'status': 'success'}, status=status.HTTP_200_OK)


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Require authentication