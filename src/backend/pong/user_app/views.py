from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import requests

class SessionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(csrf_protect)
    def get(self, request, format=None):
        return Response({'isAuthenticated': True})


class WhoAmIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # The user should be authenticated and attached to the request
        user = request.user

        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'username': user.username})
    
class RegisterView(APIView):
    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return Response(
                {'message': 'Username, password, and email are required', 'status': 'error'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'message': 'Email already exists', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)

        # Request JWT tokens from the auth service
        auth_response = requests.post(
            'http://auth:8000/api/auth/login/',
            data={'username': username, 'password': password}
        )

        if auth_response.status_code != 200:
            return Response(auth_response.json(), status=auth_response.status_code)

        tokens = auth_response.json()
        access_token = tokens['access']
        refresh_token = tokens['refresh']

        response = Response({
            'message': 'Registration successful',
            'user_id': user.id,
            'access': access_token,
            'refresh': refresh_token
        }, status=status.HTTP_200_OK)

        # Set cookies for the tokens
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=access_token,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=refresh_token,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        return response

class LoginView(APIView):
    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if username is None or password is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)

        # Request JWT tokens from the auth service
        auth_response = requests.post(
            'http://auth:8000/api/auth/login/',
            data={'username': username, 'password': password}
        )

        if auth_response.status_code != 200:
            return Response(auth_response.json(), status=auth_response.status_code)

        tokens = auth_response.json()
        access_token = tokens['access']
        refresh_token = tokens['refresh']

        response = Response({
            'access': access_token,
            'refresh': refresh_token
        }, status=status.HTTP_200_OK)

        # Set cookies for the tokens
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=access_token,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=refresh_token,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        
        # Set CSRF token
        csrf_token = get_token(request)
        response.set_cookie('csrftoken', csrf_token, httponly=True, secure=True, samesite='Lax')
        response['X-CSRFToken'] = csrf_token
        
        return response

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'You\'re not logged in.'}, status=status.HTTP_400_BAD_REQUEST)

        # Blacklist the refresh token if using blacklist strategy
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception as e:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform the logout
        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
