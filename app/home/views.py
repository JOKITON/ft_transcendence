from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware.csrf import get_token
from rest_framework_simplejwt.authentication import JWTAuthentication

def some_protected_view(request):
    # JWT Authentication middleware will handle token validation
    authentication = JWTAuthentication()
    user, validated_token = authentication.authenticate(request)
    if user is not None:
        # Proceed with view logic
        pass
    else:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

def csrf_token_view(request):
    csrf_token = get_token(request)
    response = JsonResponse({'csrfToken': csrf_token})
    response.set_cookie('csrftoken', csrf_token, httponly=False, secure=True)  # Adjust settings as needed
    return response

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

def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)

    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        csrf_token = get_token(request)
        
        response = JsonResponse({'message': 'Login successful', 'status': 'success'})

        response.set_cookie('auth_token', str(refresh.access_token), httponly=True, secure=True)
        response.set_cookie('csrf_token', csrf_token, secure=True)
        return response
    else:
        return JsonResponse({'error': 'Invalid username or password', 'status': 'error'}, status=401)

def logout_view(request):
    logout(request)
    response = JsonResponse({'message': 'Logout successful'})
    response.delete_cookie('auth_token')
    response.delete_cookie('csrf_token')
    return response