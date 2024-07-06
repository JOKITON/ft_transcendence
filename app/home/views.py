from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
# Rest
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
# CSRF
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST
from .csrf import check_csrf_token, get_csrf
from .auth import refresh_token_view

class SessionView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        return JsonResponse({'isAuthenticated': True})


class WhoAmIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        return JsonResponse({'username': request.user.username})

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return JsonResponse(
                {'message': 'Username, password, and email are required', 'status': 'error'},
                status=400
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already exists', 'status': 'error'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already exists', 'status': 'error'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({'message': 'Registration successful', 'user_id': user.id}, status=200)

    return JsonResponse({'error': 'POST method required', 'status': 'error'}, status=405)

@require_POST
@csrf_protect
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({'detail': 'Please provide username and password.'}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'detail': 'Invalid credentials.'}, status=400)

    login(request, user)
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    
    response = JsonResponse({'detail': 'Login successful'})
    
    # Set JWT tokens as HttpOnly cookies
    response.set_cookie('access_token', str(access_token), httponly=True, secure=True, samesite='Lax')
    response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True, samesite='Lax')
    
    # Set the CSRF token cookie
    csrf_token = get_token(request)
    response.set_cookie('csrftoken', csrf_token, httponly=False, secure=True, samesite='Lax')
    
    return response

@require_POST
@csrf_protect
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)

    logout(request)
    return JsonResponse({'detail': 'Successfully logged out.'})
